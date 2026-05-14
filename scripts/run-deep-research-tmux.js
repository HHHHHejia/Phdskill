#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const cp = require("child_process");

function usage() {
  console.log(`Usage:
  node scripts/run-deep-research-tmux.js [wrapper options] [deep research options]

Wrapper options:
  --session <name>       tmux session name. Default: generated from mode/time.
  --script <path>        Deep Research script. Default: sibling deep-research-idea.js.
  --help                 Show this help.

Common deep research options passed through:
  --mode <mode>          idea or knowledge-base. Default: idea.
  --project-root <dir>   Output project repo. Default: current directory.
  --out-dir <dir>        Output dir. Default follows deep-research-idea.js.

This wrapper starts deep-research-idea.js in a detached tmux session and returns
immediately. It never falls back to foreground execution.
`);
}

function shellQuote(value) {
  return `'${String(value).replace(/'/g, `'\\''`)}'`;
}

function sanitizeSessionName(value) {
  return String(value)
    .replace(/[^A-Za-z0-9_.:-]+/g, "_")
    .replace(/^[:.-]+|[:.-]+$/g, "")
    .slice(0, 80) || "phd_deep_research";
}

function parseArgs(argv) {
  const wrapper = {
    mode: "idea",
    projectRoot: process.cwd(),
    script: path.join(__dirname, "deep-research-idea.js"),
    outDir: "",
    session: "",
  };
  const passthrough = [];

  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === "--help" || arg === "-h") {
      wrapper.help = true;
    } else if (arg === "--session") {
      wrapper.session = argv[++i];
    } else if (arg === "--script") {
      wrapper.script = argv[++i];
    } else if (arg === "--mode") {
      wrapper.mode = argv[++i];
      passthrough.push(arg, wrapper.mode);
    } else if (arg === "--project-root") {
      wrapper.projectRoot = argv[++i];
      passthrough.push(arg, wrapper.projectRoot);
    } else if (arg === "--out-dir") {
      wrapper.outDir = argv[++i];
      passthrough.push(arg, wrapper.outDir);
    } else {
      passthrough.push(arg);
    }
  }

  if (!["idea", "knowledge-base"].includes(wrapper.mode)) {
    throw new Error("--mode must be one of: idea, knowledge-base");
  }

  wrapper.projectRoot = path.resolve(wrapper.projectRoot);
  wrapper.script = path.resolve(wrapper.script);
  wrapper.outDir = path.resolve(
    wrapper.outDir ||
      path.join(wrapper.projectRoot, wrapper.mode === "knowledge-base" ? "02_knowledge_base" : "01_idea")
  );
  wrapper.session = sanitizeSessionName(
    wrapper.session || `phd_deep_${wrapper.mode}_${new Date().toISOString().replace(/[-:.TZ]/g, "")}`
  );

  return { wrapper, passthrough };
}

function requireTmux() {
  const found = cp.spawnSync("tmux", ["-V"], { encoding: "utf-8" });
  if (found.status !== 0) {
    throw new Error("tmux is required for Deep Research runs; install tmux or ask the user how to proceed");
  }
}

function ensureSessionFree(session) {
  const found = cp.spawnSync("tmux", ["has-session", "-t", session], {
    encoding: "utf-8",
    stdio: "ignore",
  });
  if (found.status === 0) {
    throw new Error(`tmux session already exists: ${session}`);
  }
}

function main() {
  const { wrapper, passthrough } = parseArgs(process.argv.slice(2));
  if (wrapper.help) {
    usage();
    return 0;
  }

  requireTmux();
  ensureSessionFree(wrapper.session);
  if (!fs.existsSync(wrapper.script)) {
    throw new Error(`deep research script not found: ${wrapper.script}`);
  }

  const toolDir = path.join(wrapper.outDir, "tool_outputs");
  fs.mkdirSync(toolDir, { recursive: true });

  const logPath = path.join(toolDir, "deep_research_tmux.log");
  const statusPath = path.join(toolDir, "deep_research_tmux_status.txt");
  const sessionPath = path.join(toolDir, "deep_research_tmux_session.json");

  const commandArgs = [process.execPath, wrapper.script, ...passthrough];
  const deepCommand = commandArgs.map(shellQuote).join(" ");
  const startedAt = new Date().toISOString();
  const metadata = {
    session: wrapper.session,
    mode: wrapper.mode,
    project_root: wrapper.projectRoot,
    out_dir: wrapper.outDir,
    command: commandArgs,
    log_path: logPath,
    status_path: statusPath,
    started_at: startedAt,
  };
  fs.writeFileSync(sessionPath, `${JSON.stringify(metadata, null, 2)}\n`, "utf-8");

  const shellCommand = [
    `cd ${shellQuote(process.cwd())}`,
    `printf ${shellQuote(`started_at=${startedAt}\nsession=${wrapper.session}\n\n`)} > ${shellQuote(logPath)}`,
    `${deepCommand} >> ${shellQuote(logPath)} 2>&1`,
    "exit_code=$?",
    `printf 'session=%s\\nexit_code=%s\\nfinished_at=%s\\nlog=%s\\n' ${shellQuote(wrapper.session)} "$exit_code" "$(date -u '+%Y-%m-%dT%H:%M:%SZ')" ${shellQuote(logPath)} > ${shellQuote(statusPath)}`,
  ].join("; ");

  const started = cp.spawnSync("tmux", ["new-session", "-d", "-s", wrapper.session, shellCommand], {
    encoding: "utf-8",
  });
  if (started.status !== 0) {
    throw new Error((started.stderr || started.stdout || "failed to start tmux session").trim());
  }

  console.log(`started tmux session: ${wrapper.session}`);
  console.log(`session metadata: ${sessionPath}`);
  console.log(`log: ${logPath}`);
  console.log(`status: ${statusPath}`);
  console.log(`attach: tmux attach -t ${wrapper.session}`);
  console.log(`check: tmux capture-pane -pt ${wrapper.session}`);
  return 0;
}

try {
  process.exit(main());
} catch (err) {
  console.error(err.message);
  process.exit(1);
}
