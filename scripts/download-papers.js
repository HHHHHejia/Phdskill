#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");

function usage() {
  console.log(`Usage:
  node scripts/download-papers.js [options]

Options:
  --project-root <dir>  Output project repo. Default: current directory.
  --manifest <path>     Paper manifest JSON. Default: <project-root>/02_knowledge_base/tool_outputs/papers_to_download.json.
  --out-dir <dir>       Related works dir. Default: <project-root>/02_knowledge_base/related_works.
  --help                Show this help.

Downloads public arXiv/OpenReview/direct-PDF sources when possible. Paywalled
or non-PDF sources are recorded as metadata only.
`);
}

function parseArgs(argv) {
  const args = { projectRoot: process.cwd() };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--help" || a === "-h") args.help = true;
    else if (a === "--project-root") args.projectRoot = argv[++i];
    else if (a === "--manifest") args.manifest = argv[++i];
    else if (a === "--out-dir") args.outDir = argv[++i];
    else throw new Error(`unknown argument: ${a}`);
  }
  args.projectRoot = path.resolve(args.projectRoot);
  const defaultManifest = path.join(
    args.projectRoot,
    "02_knowledge_base",
    "tool_outputs",
    "papers_to_download.json"
  );
  const legacyManifest = path.join(args.projectRoot, "02_knowledge_base", "papers_to_download.json");
  args.manifest = path.resolve(
    args.manifest || (fs.existsSync(defaultManifest) ? defaultManifest : legacyManifest)
  );
  args.outDir = path.resolve(
    args.outDir || path.join(args.projectRoot, "02_knowledge_base", "related_works")
  );
  return args;
}

function slugify(s) {
  return String(s || "uncategorized")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "")
    .slice(0, 80) || "uncategorized";
}

function paperSlug(paper, index) {
  const year = paper.year ? `${paper.year}-` : "";
  return `${String(index + 1).padStart(3, "0")}-${year}${slugify(paper.title || "paper")}`;
}

function normalizeArxivId(raw) {
  if (!raw) return "";
  let s = String(raw).trim();
  s = s.replace(/^arxiv:/i, "");
  s = s.replace(/^https?:\/\/arxiv\.org\/(?:abs|pdf)\//i, "");
  s = s.replace(/\.pdf$/i, "");
  return s;
}

function inferPdfUrl(paper) {
  if (paper.pdf_url) return paper.pdf_url;
  const arxiv = normalizeArxivId(paper.arxiv_id || paper.url);
  if (/^\d{4}\.\d{4,5}(v\d+)?$/i.test(arxiv) || /^[a-z-]+\/\d{7}(v\d+)?$/i.test(arxiv)) {
    return `https://arxiv.org/pdf/${arxiv}.pdf`;
  }
  const url = paper.url || "";
  if (/\.pdf($|\?)/i.test(url)) return url;
  if (/openreview\.net\/forum\?id=/i.test(url)) {
    const id = new URL(url).searchParams.get("id");
    if (id) return `https://openreview.net/pdf?id=${encodeURIComponent(id)}`;
  }
  return "";
}

async function download(url, dest) {
  const resp = await fetch(url, {
    headers: {
      "User-Agent": "phd-skill-paper-downloader/0.1",
    },
  });
  if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
  const contentType = resp.headers.get("content-type") || "";
  const buf = Buffer.from(await resp.arrayBuffer());
  if (!/pdf/i.test(contentType) && !buf.subarray(0, 5).equals(Buffer.from("%PDF-"))) {
    throw new Error(`not a PDF response (${contentType || "unknown content-type"})`);
  }
  fs.writeFileSync(dest, buf);
}

function loadManifest(file) {
  const data = JSON.parse(fs.readFileSync(file, "utf-8"));
  if (Array.isArray(data)) return data;
  if (Array.isArray(data.papers)) return data.papers;
  throw new Error("manifest must be an array or an object with a papers array");
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) {
    usage();
    return 0;
  }

  const papers = loadManifest(args.manifest);
  fs.mkdirSync(args.outDir, { recursive: true });

  const log = ["# Paper Download Log", ""];
  for (let i = 0; i < papers.length; i++) {
    const paper = papers[i];
    const category = slugify(paper.category || "uncategorized");
    const dir = path.join(args.outDir, category);
    fs.mkdirSync(dir, { recursive: true });

    const base = paperSlug(paper, i);
    const metadataPath = path.join(dir, `${base}.json`);
    const pdfPath = path.join(dir, `${base}.pdf`);
    const pdfUrl = inferPdfUrl(paper);
    const metadata = { ...paper, inferred_pdf_url: pdfUrl || "" };

    if (!pdfUrl) {
      metadata.download_status = "metadata-only";
      metadata.download_error = "no public PDF URL inferred";
      fs.writeFileSync(metadataPath, JSON.stringify(metadata, null, 2) + "\n", "utf-8");
      log.push(`- metadata only: ${paper.title || "(untitled)"} (${category})`);
      continue;
    }

    try {
      await download(pdfUrl, pdfPath);
      metadata.download_status = "downloaded";
      metadata.local_pdf = path.relative(args.projectRoot, pdfPath);
      fs.writeFileSync(metadataPath, JSON.stringify(metadata, null, 2) + "\n", "utf-8");
      log.push(`- downloaded: ${paper.title || "(untitled)"} -> ${metadata.local_pdf}`);
    } catch (err) {
      metadata.download_status = "failed";
      metadata.download_error = err.message;
      fs.writeFileSync(metadataPath, JSON.stringify(metadata, null, 2) + "\n", "utf-8");
      log.push(`- failed: ${paper.title || "(untitled)"} (${pdfUrl}) - ${err.message}`);
    }
  }

  fs.writeFileSync(path.join(args.outDir, "download_log.md"), log.join("\n") + "\n", "utf-8");
  console.log(`processed ${papers.length} papers into ${args.outDir}`);
  return 0;
}

main().then(
  (code) => process.exit(code),
  (err) => {
    console.error(err.message);
    process.exit(1);
  }
);
