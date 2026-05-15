# 02 Knowledge Base

## Goal

After the user narrows the idea, build a project-local literature knowledge
base and paper library for the selected field.

This step should produce a serious survey, taxonomy, source list, and organized
downloaded references when public downloads are available.

## Folder Contract

- Formal stage output: write exactly one Markdown file in
  `02_knowledge_base/`.
- Paper output: write exactly one LaTeX file in `07_paper_latex/`.
- Continuity output: append to `02_knowledge_base/README.md` and the root
  `README.md`; these logs do not count as formal stage outputs.
- Allowed tool artifacts: `02_knowledge_base/tool_outputs/` may contain raw
  Deep Research reports, raw JSON, taxonomy JSON, paper-download manifests, and
  tool failure notes.
- Allowed download artifacts: `02_knowledge_base/related_works/` may contain
  taxonomy folders, public PDFs, metadata JSON, and download logs.
- Read `00_project_setup.md` and `01_idea/idea.md`.
- Do not write method specs, experiment plans, code, analysis, or any other
  paper text yet.

## Inputs

- `00_project_setup.md`
- `01_idea/idea.md`
- `01_idea/tool_outputs/` raw Deep Research artifacts
- User direction choice from Step 1

## Actions

Before the numbered actions, run the continuity resume protocol from
`commands/phd.md`: read the root README first, then every numbered folder
README, and use the logs to reuse prior survey outputs, downloaded papers,
metadata, taxonomy folders, and unfinished download batches instead of
rediscovering them.

1. Start the Deep Research helper in knowledge-base mode in a detached tmux
   session:

   ```bash
   node <path-to-phd-skill>/scripts/run-deep-research-tmux.js \
     --mode knowledge-base \
     --project-root <output-repo>
   ```

   Do not run `deep-research-idea.js` directly in the foreground. The tmux
   wrapper returns immediately and writes session metadata, logs, and completion
   status under `02_knowledge_base/tool_outputs/`.
2. Record the tmux session name and log path in `02_knowledge_base/README.md`.
   Check progress with `tmux capture-pane -pt <session>` or the log file. After
   the tmux job finishes successfully, read
   `02_knowledge_base/tool_outputs/deep_research_survey.md`, `taxonomy.json`,
   and `papers_to_download.json`.
3. Create taxonomy folders under `02_knowledge_base/related_works/`.
4. Download public papers with:

   ```bash
   node <path-to-phd-skill>/scripts/download-papers.js \
     --project-root <output-repo>
   ```

5. Record paywalled, failed, or non-PDF sources as metadata only. Do not bypass
   access controls.
6. Before writing `02_knowledge_base/knowledge_base.md`, ask the user up to 10
   non-trivial, decision-oriented questions to clarify field scope,
   inclusion/exclusion criteria, source priorities, and novelty concerns. Ask
   only questions whose answers could change the literature scope, taxonomy,
   source handling, novelty assessment, or next action.
7. Synthesize the survey, taxonomy, downloads, and metadata into the single
   formal output `02_knowledge_base/knowledge_base.md`.
8. Append completion or blocked-state entries to `02_knowledge_base/README.md`
   and the root `README.md`, then commit and push according to the git protocol
   in `commands/phd.md`.

If tmux is unavailable or the helper cannot start, write the failure note in
`02_knowledge_base/tool_outputs/tool_failure.md` and ask before continuing
without Deep Research. Do not fall back to a foreground Deep Research run.

## Output

Write exactly one formal Markdown output:

- `02_knowledge_base/knowledge_base.md`

Use this structure:

```markdown
# Knowledge Base

## Human Pre-Write Clarifications

## Selected Idea And Scope

## Field Taxonomy

## Literature Survey

## Core Papers And Source Status

## Downloaded Library Summary

## Datasets Benchmarks And Official Resources

## Methods Baselines And Metrics

## Novelty Opportunities

## Risks And Missing Evidence

## Step 3 Method Design Brief
```

Do not create any other formal Markdown files for this step; fold all sections
into `knowledge_base.md`. Machine-readable manifests and raw reports belong in
`tool_outputs/`.

## Paper LaTeX Output

Write exactly one paper-section output:

- `07_paper_latex/relatedwork.tex`

This should be an evidence-grounded related-work draft. It must:

- organize prior work by the taxonomy in `knowledge_base.md`
- cite only papers recorded in `02_knowledge_base/`
- distinguish downloaded papers from metadata-only leads when confidence differs
- explain novelty risks and positioning honestly
- leave `% TODO:` comments for papers needing closer reading or verification
- avoid claiming the proposed method outperforms anything before experiments

## Stop Gate

Stop after `02_knowledge_base/knowledge_base.md` and
`07_paper_latex/relatedwork.tex` are written, the README logs are updated,
and commit/push has been attempted. Summarize downloaded papers, metadata-only
sources, taxonomy categories, novelty risks, what Step 3 should design the
method around, and the commit/push status.

Do not move to method design until the user approves the selected direction and
knowledge base.
