#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const os = require("os");

function rmrf(p) {
  if (!fs.existsSync(p)) return;
  const stat = fs.lstatSync(p);
  if (!stat.isDirectory() || stat.isSymbolicLink()) {
    fs.unlinkSync(p);
    return;
  }
  for (const entry of fs.readdirSync(p)) {
    rmrf(path.join(p, entry));
  }
  fs.rmdirSync(p);
}

try {
  rmrf(path.join(os.homedir(), ".claude", "commands", "phd.md"));
  rmrf(path.join(os.homedir(), ".claude", "commands", "phd-guides"));
  rmrf(path.join(os.homedir(), ".claude", "commands", "phd-scripts"));
  console.log("✓ Claude Code: /phd removed");
} catch (_) {
  // best effort
}

try {
  rmrf(path.join(os.homedir(), ".codex", "skills", "phd"));
  console.log("✓ Codex: $phd removed");
} catch (_) {
  // best effort
}
