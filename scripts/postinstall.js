#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const os = require("os");

const ROOT = path.join(__dirname, "..");
const COMMAND = path.join(ROOT, "commands", "phd.md");
const GUIDES = path.join(ROOT, "guides");
const TOOL_SCRIPTS = ["deep-research-idea.js", "run-deep-research-tmux.js", "download-papers.js"];

function rmrf(target) {
  if (!fs.existsSync(target)) return;
  const stat = fs.lstatSync(target);
  if (!stat.isDirectory() || stat.isSymbolicLink()) {
    fs.unlinkSync(target);
    return;
  }
  for (const entry of fs.readdirSync(target)) {
    rmrf(path.join(target, entry));
  }
  fs.rmdirSync(target);
}

function copyDir(src, dst) {
  fs.mkdirSync(dst, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const s = path.join(src, entry.name);
    const d = path.join(dst, entry.name);
    if (entry.isDirectory()) copyDir(s, d);
    else if (entry.isFile()) fs.copyFileSync(s, d);
  }
}

function readCommand() {
  return fs.readFileSync(COMMAND, "utf-8");
}

// Claude Code
try {
  const ccCommands = path.join(os.homedir(), ".claude", "commands");
  fs.mkdirSync(ccCommands, { recursive: true });
  fs.copyFileSync(COMMAND, path.join(ccCommands, "phd.md"));
  const ccGuides = path.join(ccCommands, "phd-guides");
  rmrf(ccGuides);
  copyDir(GUIDES, ccGuides);
  const ccScripts = path.join(ccCommands, "phd-scripts");
  rmrf(ccScripts);
  fs.mkdirSync(ccScripts, { recursive: true });
  for (const script of TOOL_SCRIPTS) {
    fs.copyFileSync(path.join(__dirname, script), path.join(ccScripts, script));
  }
  console.log("✓ Claude Code: /phd installed");
} catch (err) {
  console.error("⚠ Claude Code: could not install /phd —", err.message);
}

// Codex
try {
  const skillDir = path.join(os.homedir(), ".codex", "skills", "phd");
  rmrf(skillDir);
  fs.mkdirSync(skillDir, { recursive: true });
  const skill = [
    "---",
    'name: "phd"',
    'description: "Create a complete PhD-style paper project git repository from a research idea. Use when asked to turn an idea into a full research repo with literature planning, idea refinement, method design, experiments, analysis, writing, and review."',
    "---",
    readCommand(),
  ].join("\n");
  fs.writeFileSync(path.join(skillDir, "SKILL.md"), skill, "utf-8");
  copyDir(GUIDES, path.join(skillDir, "guides"));
  const codexScripts = path.join(skillDir, "scripts");
  fs.mkdirSync(codexScripts, { recursive: true });
  for (const script of TOOL_SCRIPTS) {
    fs.copyFileSync(path.join(__dirname, script), path.join(codexScripts, script));
  }
  console.log("✓ Codex: $phd installed");
} catch (err) {
  console.error("⚠ Codex: could not install $phd —", err.message);
}

console.log("\nUsage: /phd (Claude Code) or $phd (Codex)");
