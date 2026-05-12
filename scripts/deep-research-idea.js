#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

const DEFAULT_MODEL = process.env.OPENAI_DEEP_RESEARCH_MODEL || "o4-mini-deep-research";

function usage() {
  console.log(`Usage:
  node scripts/deep-research-idea.js [options]

Options:
  --mode <mode>             idea or knowledge-base. Default: idea.
  --project-root <dir>       Output project repo. Default: current directory.
  --idea-file <path>         Idea file. Default: <project-root>/00_project_setup.md.
  --constraints-file <path>  Optional extra constraints file. Default: legacy <project-root>/01_idea/user_constraints.md if present.
  --out-dir <dir>            Output dir. Default: <project-root>/01_idea.
  --model <model>            Deep research model. Default: ${DEFAULT_MODEL}.
  --max-wait-minutes <n>     Poll timeout for background responses. Default: 20.
  --poll-seconds <n>         Poll interval. Default: 15.
  --no-background            Disable Responses API background mode.
  --help                     Show this help.

Environment:
  OPENAI_API_KEY must be set in the environment or in a .env file.
  OPENAI_DEEP_RESEARCH_MODEL optionally overrides the default model.
`);
}

function parseArgs(argv) {
  const args = {
    mode: "idea",
    projectRoot: process.cwd(),
    model: DEFAULT_MODEL,
    background: true,
    maxWaitMinutes: 20,
    pollSeconds: 15,
  };

  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--help" || a === "-h") {
      args.help = true;
    } else if (a === "--mode") {
      args.mode = argv[++i];
    } else if (a === "--no-background") {
      args.background = false;
    } else if (a === "--project-root") {
      args.projectRoot = argv[++i];
    } else if (a === "--idea-file") {
      args.ideaFile = argv[++i];
    } else if (a === "--constraints-file") {
      args.constraintsFile = argv[++i];
    } else if (a === "--out-dir") {
      args.outDir = argv[++i];
    } else if (a === "--model") {
      args.model = argv[++i];
    } else if (a === "--max-wait-minutes") {
      args.maxWaitMinutes = Number(argv[++i]);
    } else if (a === "--poll-seconds") {
      args.pollSeconds = Number(argv[++i]);
    } else {
      throw new Error(`unknown argument: ${a}`);
    }
  }

  if (!["idea", "knowledge-base"].includes(args.mode)) {
    throw new Error("--mode must be one of: idea, knowledge-base");
  }
  args.projectRoot = path.resolve(args.projectRoot);
  args.outDir = path.resolve(
    args.outDir ||
      path.join(args.projectRoot, args.mode === "knowledge-base" ? "02_knowledge_base" : "01_idea")
  );
  args.ideaFile = path.resolve(args.ideaFile || path.join(args.projectRoot, "00_project_setup.md"));
  args.constraintsFile = path.resolve(
    args.constraintsFile || path.join(args.outDir, "user_constraints.md")
  );
  return args;
}

function parseDotenv(content) {
  const out = {};
  for (const raw of content.split(/\r?\n/)) {
    const line = raw.trim();
    if (!line || line.startsWith("#")) continue;
    const m = line.match(/^([A-Za-z_][A-Za-z0-9_]*)=(.*)$/);
    if (!m) continue;
    let value = m[2].trim();
    if (
      (value.startsWith('"') && value.endsWith('"')) ||
      (value.startsWith("'") && value.endsWith("'"))
    ) {
      value = value.slice(1, -1);
    }
    out[m[1]] = value;
  }
  return out;
}

function findDotenv(startDirs) {
  const seen = new Set();
  for (const start of startDirs) {
    let cur = path.resolve(start);
    while (!seen.has(cur)) {
      seen.add(cur);
      const p = path.join(cur, ".env");
      if (fs.existsSync(p)) return p;
      const parent = path.dirname(cur);
      if (parent === cur) break;
      cur = parent;
    }
  }
  return null;
}

function loadApiKey(args) {
  if (process.env.OPENAI_API_KEY) return process.env.OPENAI_API_KEY;
  const dotenv = findDotenv([process.cwd(), args.projectRoot, path.join(__dirname, "..")]);
  if (!dotenv) return null;
  const env = parseDotenv(fs.readFileSync(dotenv, "utf-8"));
  return env.OPENAI_API_KEY || null;
}

function readOptional(file) {
  if (!fs.existsSync(file)) return "";
  return fs.readFileSync(file, "utf-8").trim();
}

function buildIdeaPrompt({ idea, constraints }) {
  return `You are doing preliminary scientific literature research for Step 1 of a PhD paper project.

The user's idea is rough and may be flawed. Your job is to search the literature, assess feasibility, surface reference papers, and suggest pivots.

Initial idea:
${idea || "(missing)"}

Known constraints:
${constraints || "(none provided)"}

Research requirements:
- Use web search and prioritize primary scientific sources, original papers, benchmark pages, dataset documentation, and official project pages.
- Do not fabricate citations, venues, authors, dates, numbers, datasets, baselines, or results.
- If a source is only a lead and you did not inspect enough detail, label it as a lead rather than evidence.
- Be honest when the idea appears already done, too broad, weakly motivated, or hard to evaluate.
- Prefer concrete pivots that can become publishable research directions.

Return a Markdown report with these exact sections:

# Preliminary Idea Research Report

## 1. One-sentence restatement

## 2. Initial feasibility assessment
Include feasibility rating: High / Medium / Low / Unknown, and explain why.

## 3. What the literature seems to already cover

## 4. Reference papers and sources
Use a table with: title, authors/year if available, venue/source if available, URL/DOI, why it matters, evidence vs lead.

## 5. Novelty risks

## 6. Evaluation possibilities
Mention possible datasets, baselines, metrics, and experimental setups if visible from the preliminary search.

## 7. Suggested pivot directions
Give 3-5 options. For each: short name, research question, why it may be publishable, required evidence, main risk.

## 8. Recommended next direction
Recommend one direction or say that more clarification is needed.

## 9. Questions for the user
List 10 candidate decision-oriented questions that could help the agent run the Step 1 human checkpoint.

## 10. Literature research plan for Step 2
Give concrete search queries, source types, inclusion/exclusion criteria, and what should be downloaded into 02_knowledge_base/.`;
}

function readStep1Context(projectRoot) {
  const dir = path.join(projectRoot, "01_idea");
  const names = [
    "idea.md",
    "tool_outputs/deep_research_report.md",
    "tool_outputs/source_annotations.md",
    "tool_outputs/tool_failure.md",
  ];
  const chunks = [];
  for (const name of names) {
    const p = path.join(dir, name);
    const text = readOptional(p);
    if (text) chunks.push(`\n\n--- ${name} ---\n${text}`);
  }
  return chunks.join("\n");
}

function buildKnowledgeBasePrompt({ step1Context }) {
  return `You are doing Step 2 of a PhD paper project: build a literature knowledge base after the user has selected or narrowed the research idea.

Use the Step 1 materials below: the formal idea report, preliminary research artifacts, literature plan, and any user answers. Your job is to produce a field survey that can guide a real research project.

Step 1 context:
${step1Context || "(missing)"}

Research requirements:
- Use web search and prioritize primary scientific sources, original papers, benchmark pages, dataset documentation, and official project pages.
- Do not fabricate citations, venues, authors, dates, numbers, datasets, baselines, URLs, or results.
- Include only papers/sources that are relevant to the selected or most promising idea.
- Distinguish between must-read core papers, useful background papers, datasets/benchmarks, and source leads.
- Prefer sources with public URLs, arXiv IDs, DOI links, OpenReview pages, official PDF links, or project pages.

Return a Markdown report with these exact sections:

# Knowledge Base Survey

## 1. Selected idea and scope

## 2. Field taxonomy
Describe the categories that should become folders under 02_knowledge_base/related_works/.

## 3. Complete survey
Write a structured survey of the area, organized by taxonomy category.

## 4. Core papers to download
Use a table with: category, title, authors/year if available, venue/source if available, URL/DOI/arXiv, why needed, priority.

## 5. Datasets, benchmarks, and official resources

## 6. Methods, baselines, and metrics likely needed later

## 7. Open problems and novelty opportunities

## 8. Risks and missing evidence

## 9. Step 3 method-design implications

## Machine-readable taxonomy JSON
Return one fenced JSON block with this shape:
\`\`\`json
{
  "categories": [
    {
      "id": "short-folder-safe-id",
      "name": "Readable category name",
      "description": "What belongs here"
    }
  ]
}
\`\`\`

## Machine-readable paper download manifest JSON
Return one fenced JSON block with this shape:
\`\`\`json
{
  "papers": [
    {
      "title": "Paper title",
      "authors": "Authors if known",
      "year": "Year if known",
      "category": "short-folder-safe-id from taxonomy",
      "url": "landing page, DOI, arXiv, OpenReview, or PDF URL",
      "pdf_url": "direct public PDF URL if known, otherwise empty string",
      "doi": "DOI if known, otherwise empty string",
      "arxiv_id": "arXiv id if known, otherwise empty string",
      "priority": "core/background/dataset/lead",
      "why_needed": "Why this source belongs in the knowledge base"
    }
  ]
}
\`\`\``;
}

async function openaiRequest(apiKey, method, endpoint, body) {
  const resp = await fetch(`https://api.openai.com/v1${endpoint}`, {
    method,
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json",
    },
    body: body ? JSON.stringify(body) : undefined,
  });
  const text = await resp.text();
  let data;
  try {
    data = text ? JSON.parse(text) : {};
  } catch (_) {
    data = { raw: text };
  }
  if (!resp.ok) {
    const msg = data && data.error && data.error.message ? data.error.message : text;
    throw new Error(`OpenAI API ${resp.status}: ${msg}`);
  }
  return data;
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function waitForCompletion(apiKey, response, args) {
  if (!args.background) return response;
  if (response.status === "completed") return response;
  if (!response.id) return response;

  const deadline = Date.now() + args.maxWaitMinutes * 60 * 1000;
  let current = response;
  while (Date.now() < deadline) {
    if (["completed", "failed", "cancelled", "incomplete"].includes(current.status)) {
      return current;
    }
    await sleep(args.pollSeconds * 1000);
    current = await openaiRequest(apiKey, "GET", `/responses/${response.id}`);
    process.stderr.write(`poll ${current.id}: ${current.status}\n`);
  }
  return current;
}

function extractText(response) {
  if (typeof response.output_text === "string" && response.output_text.trim()) {
    return response.output_text;
  }
  const chunks = [];
  for (const item of response.output || []) {
    if (item.type !== "message") continue;
    for (const part of item.content || []) {
      if (part.type === "output_text" && part.text) chunks.push(part.text);
    }
  }
  return chunks.join("\n\n").trim();
}

function collectAnnotations(response) {
  const annotations = [];
  for (const item of response.output || []) {
    if (item.type !== "message") continue;
    for (const part of item.content || []) {
      for (const ann of part.annotations || []) {
        if (ann.url || ann.title) annotations.push(ann);
      }
    }
  }
  return annotations;
}

function extractSection(markdown, headingPattern) {
  const lines = markdown.split(/\r?\n/);
  const start = lines.findIndex((line) => /^##\s+/.test(line) && headingPattern.test(line));
  if (start === -1) return "";
  let end = lines.length;
  for (let i = start + 1; i < lines.length; i++) {
    if (/^##\s+/.test(lines[i])) {
      end = i;
      break;
    }
  }
  return lines.slice(start, end).join("\n").trim() + "\n";
}

function writeIdeaOutputs(args, response, report) {
  fs.mkdirSync(args.outDir, { recursive: true });
  const toolDir = path.join(args.outDir, "tool_outputs");
  fs.mkdirSync(toolDir, { recursive: true });
  fs.writeFileSync(path.join(toolDir, "deep_research_report.md"), report + "\n", "utf-8");
  fs.writeFileSync(
    path.join(toolDir, "deep_research_raw.json"),
    JSON.stringify(response, null, 2),
    "utf-8"
  );

  const refs = collectAnnotations(response);
  const refLines = ["# Reference Sources", ""];
  if (refs.length === 0) {
    refLines.push("No structured citation annotations were returned. See `deep_research_report.md`.");
  } else {
    const seen = new Set();
    for (const ann of refs) {
      const key = `${ann.title || ""}|${ann.url || ""}`;
      if (seen.has(key)) continue;
      seen.add(key);
      refLines.push(`- ${ann.title || "(untitled)"}${ann.url ? ` — ${ann.url}` : ""}`);
    }
  }
  fs.writeFileSync(path.join(toolDir, "source_annotations.md"), refLines.join("\n") + "\n", "utf-8");
}

function parseJsonBlockAfterHeading(markdown, headingPattern) {
  const heading = markdown.search(headingPattern);
  if (heading === -1) return null;
  const tail = markdown.slice(heading);
  const block = tail.match(/```json\s*([\s\S]*?)```/i);
  if (!block) return null;
  try {
    return JSON.parse(block[1]);
  } catch (_) {
    return null;
  }
}

function writeKnowledgeBaseOutputs(args, response, report) {
  fs.mkdirSync(args.outDir, { recursive: true });
  fs.mkdirSync(path.join(args.outDir, "related_works"), { recursive: true });
  const toolDir = path.join(args.outDir, "tool_outputs");
  fs.mkdirSync(toolDir, { recursive: true });

  fs.writeFileSync(path.join(toolDir, "deep_research_survey.md"), report + "\n", "utf-8");
  fs.writeFileSync(
    path.join(toolDir, "deep_research_survey_raw.json"),
    JSON.stringify(response, null, 2),
    "utf-8"
  );

  const taxonomy = parseJsonBlockAfterHeading(report, /Machine-readable taxonomy JSON/i) || {
    categories: [],
  };
  const manifest = parseJsonBlockAfterHeading(report, /Machine-readable paper download manifest JSON/i) || {
    papers: [],
  };

  fs.writeFileSync(
    path.join(toolDir, "taxonomy.json"),
    JSON.stringify(taxonomy, null, 2) + "\n",
    "utf-8"
  );
  fs.writeFileSync(
    path.join(toolDir, "papers_to_download.json"),
    JSON.stringify(manifest, null, 2) + "\n",
    "utf-8"
  );

  for (const cat of taxonomy.categories || []) {
    if (cat.id) fs.mkdirSync(path.join(args.outDir, "related_works", cat.id), { recursive: true });
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    usage();
    return 0;
  }

  const apiKey = loadApiKey(args);
  if (!apiKey) {
    throw new Error("OPENAI_API_KEY not found in environment or .env");
  }

  let input;
  if (args.mode === "knowledge-base") {
    const step1Context = readStep1Context(args.projectRoot);
    if (!step1Context) {
      throw new Error(`Step 1 context is missing or empty under ${path.join(args.projectRoot, "01_idea")}`);
    }
    input = buildKnowledgeBasePrompt({ step1Context });
  } else {
    const idea = readOptional(args.ideaFile);
    const legacyIdea = readOptional(path.join(args.projectRoot, "01_idea", "initial_idea.md"));
    const constraints = readOptional(args.constraintsFile);
    if (!idea && !legacyIdea) {
      throw new Error(`idea file is missing or empty: ${args.ideaFile}`);
    }
    input = buildIdeaPrompt({ idea: idea || legacyIdea, constraints });
  }
  const body = {
    model: args.model,
    input,
    background: args.background,
    tools: [{ type: "web_search_preview" }],
  };

  process.stderr.write(`starting deep research with ${args.model}\n`);
  let response = await openaiRequest(apiKey, "POST", "/responses", body);
  response = await waitForCompletion(apiKey, response, args);
  if (response.status && response.status !== "completed") {
    throw new Error(`deep research did not complete: ${response.status}`);
  }

  const report = extractText(response);
  if (!report) {
    throw new Error("deep research completed but returned no output text");
  }

  if (args.mode === "knowledge-base") {
    writeKnowledgeBaseOutputs(args, response, report);
    console.log(`wrote knowledge-base tool outputs to ${path.join(args.outDir, "tool_outputs")}`);
  } else {
    writeIdeaOutputs(args, response, report);
    console.log(`wrote preliminary research tool outputs to ${path.join(args.outDir, "tool_outputs")}`);
  }
  return 0;
}

main().then(
  (code) => process.exit(code),
  (err) => {
    console.error(err.message);
    process.exit(1);
  }
);
