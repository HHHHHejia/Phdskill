# PhD Paper Skill

This skill helps an agent turn a user's research idea into a complete
PhD-style paper project git repository.

- Input: a rough idea and user constraints.
- Output: a git repo containing the whole project: intake notes, literature
  plan, refined idea, knowledge pack, method specification, experiment plan,
  execution logs, analysis artifacts, writing drafts, review notes, and
  revision artifacts.

The package source contains:

- `README.md` - this entrypoint
- `commands/phd.md` - the agent command
- `guides/` - per-step instructions
- `scripts/deep-research-idea.js` - Step 1/2 OpenAI Deep Research helper
- `scripts/download-papers.js` - Step 2 public-paper downloader
- `scripts/postinstall.js` - installs the command for Claude Code and Codex
- `scripts/postuninstall.js` - removes installed command files

Generated paper artifacts, experiment logs, figures, tables, schemas, and
claim ledgers belong in the output project repo, not in this skill repo.

## Workflow

Invoke the same workflow as:

- Codex: `$phd`
- Claude Code: `/phd`

Use only the guide needed for the current task:

0. `guides/00-project.md` - create the output repo, initialize git, and create
   the step folders
1. `guides/01-idea.md` - run preliminary Deep Research, assess feasibility,
   list reference papers, and suggest pivot directions
2. `guides/02-knowledge-base.md` - collect literature into a knowledge base and
   refine the idea
3. `guides/03-method.md` - design the original research method
4. `guides/04-experiment-plan.md` - refine the experiment plan
5. `guides/05-experiment-code.md` - create the runnable experiment-code repo
6. `guides/06-analysis.md` - analyze experimental data and claim support
7. `guides/07-writing.md` - write and refine the LaTeX paper, including
   `main.tex`
8. `guides/08-review.md` - write expert reviewer criticism in `审稿意见.md`

Each research step keeps formal outputs small. Raw Deep Research outputs,
download manifests, PDFs, metadata, download logs, experiment-code repo files,
raw run folders, analysis scripts, processed tables, generated figures,
analysis logs, LaTeX source files, bibliography files, PDFs, and LaTeX logs are
artifacts rather than extra formal deliverables.

Every formal stage Markdown file uses human-in-the-loop checkpoints: before
writing, the agent asks 10 questions to clarify requirements; after writing, it
asks 10 calibration questions to confirm the direction before the next step.

## Hard Rules

- Do not fabricate citations.
- Do not fabricate experiment results.
- Do not hide failed experiments.
- Do not silently change hypotheses, datasets, baselines, or metrics.
- Do not delete or rewrite raw logs.
- Stop for human approval before finalizing direction, spending budget, running
  experiments, accepting claims, or submitting.

## Evidence Labels

Use these labels for major claims:

- `LITERATURE:<citation-key>`
- `RESULT:<run-id-or-path>`
- `HUMAN_ASSUMPTION`
- `SPECULATIVE`
- `UNVERIFIED`
- `NEEDS_VERIFICATION`
- `NEEDS_EXPERIMENT`
- `NEEDS_HUMAN_DECISION`

## Install

```bash
npm install -g @scienceintelligence/phd
```

The install step copies:

- Claude Code command: `~/.claude/commands/phd.md`
- Claude Code guides: `~/.claude/commands/phd-guides/`
- Claude Code scripts: `~/.claude/commands/phd-scripts/`
- Codex skill: `~/.codex/skills/phd/SKILL.md`
- Codex guides: `~/.codex/skills/phd/guides/`
- Codex scripts: `~/.codex/skills/phd/scripts/`

## Publish Check

```bash
npm run validate
npm pack --dry-run
```
