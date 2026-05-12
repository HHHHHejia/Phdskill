#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const cp = require("child_process");

const ROOT = path.join(__dirname, "..");

const requiredFiles = [
  "README.md",
  "package.json",
  "commands/phd.md",
  "guides/00-project.md",
  "guides/01-idea.md",
  "guides/02-knowledge-base.md",
  "guides/03-method.md",
  "guides/04-experiment-plan.md",
  "guides/05-experiment-code.md",
  "guides/06-analysis.md",
  "guides/07-writing.md",
  "guides/08-review.md",
  "scripts/deep-research-idea.js",
  "scripts/download-papers.js",
  "scripts/postinstall.js",
  "scripts/postuninstall.js",
];

const guideFiles = requiredFiles.filter((file) => file.startsWith("guides/"));
const requiredGuideHeadings = [
  "## Goal",
  "## Folder Contract",
  "## Inputs",
  "## Actions",
  "## Output",
  "## Stop Gate",
];

function read(file) {
  return fs.readFileSync(path.join(ROOT, file), "utf-8");
}

function fail(message) {
  console.error(`validate-package: ${message}`);
  process.exitCode = 1;
}

for (const file of requiredFiles) {
  if (!fs.existsSync(path.join(ROOT, file))) fail(`missing ${file}`);
}

for (const file of guideFiles) {
  if (!fs.existsSync(path.join(ROOT, file))) continue;
  const text = read(file);
  for (const heading of requiredGuideHeadings) {
    if (!text.includes(heading)) fail(`${file} missing ${heading}`);
  }
  if (!text.includes("## Human Pre-Write Clarifications")) {
    fail(`${file} missing human pre-write checkpoint`);
  }
  if (!text.includes("## Post-Write Calibration Questions")) {
    fail(`${file} missing post-write calibration checkpoint`);
  }
}

const command = read("commands/phd.md");
for (const guide of guideFiles) {
  if (!command.includes(guide)) fail(`commands/phd.md does not reference ${guide}`);
}

const pkg = JSON.parse(read("package.json"));
for (const include of ["commands/", "guides/", "scripts/", "README.md"]) {
  if (!pkg.files || !pkg.files.includes(include)) {
    fail(`package.json files[] missing ${include}`);
  }
}

if (!process.exitCode) {
  for (const file of requiredFiles.filter((item) => item.endsWith(".js"))) {
    const result = cp.spawnSync(process.execPath, ["--check", path.join(ROOT, file)], {
      encoding: "utf-8",
    });
    if (result.status !== 0) {
      fail(`${file} failed node --check`);
      if (result.stderr) console.error(result.stderr.trim());
    }
  }
}

if (!process.exitCode) {
  console.log("validate-package: ok");
}
