# PhD Paper Skill

This skill helps an agent turn a user's research idea into a complete
PhD-style paper project git repository.

- Input: a rough idea and user constraints.
- Output: a `research_project/` git repo containing the whole project: intake
  notes, literature plan, refined idea, knowledge pack, method specification,
  experiment plan, execution logs, analysis artifacts, writing drafts, review
  notes, and revision artifacts.

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

0. `guides/00-project.md` - create `research_project/`, initialize git there,
   create the step folders, and initialize append-only README logs
1. `guides/01-idea.md` - run preliminary Deep Research, assess feasibility,
   list reference papers, and suggest pivot directions
2. `guides/02-knowledge-base.md` - collect literature into a knowledge base and
   refine the idea
3. `guides/03-method.md` - design the original research method
4. `guides/04-experiment-plan.md` - refine the experiment plan
5. `guides/05-experiment-code.md` - create the runnable experiment-code tree
6. `guides/06-analysis.md` - analyze experimental data and claim support
7. `guides/07-writing.md` - write and refine the LaTeX paper, including
   `main.tex`
8. `guides/08-review.md` - write expert reviewer criticism in `审稿意见.md`

Each research step keeps formal outputs small. Raw Deep Research outputs,
download manifests, PDFs, metadata, download logs, experiment-code files,
raw run folders, analysis scripts, processed tables, generated figures,
analysis logs, LaTeX source files, bibliography files, PDFs, and LaTeX logs are
artifacts rather than extra formal deliverables.

## Continuity And Git

Generated projects are designed for breakpoint resume. The root
`research_project/README.md` and every numbered folder `README.md` are
append-only continuity logs. On resumed runs, the agent reads the root log first
and then all numbered-folder logs before reopening heavy artifacts such as
papers, tool outputs, run folders, or code. Folder logs record reusable state,
artifact paths, decisions, blockers, validation, and the exact next resume
point.

After a stage task completes or reaches a blocked stop point, the agent updates
the relevant folder log and root log, commits the safe changes in the root
`research_project/` git repository, and pushes when an upstream is configured.
The root git repo tracks code, Markdown, configs, scripts, manifests, metadata,
and small reproducibility artifacts. Large raw datasets, large PDFs, model
checkpoints, and large run outputs stay on disk by default and are represented
by manifests, checksums, metadata, and README log references.

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

## Automatic npm Publish

Pushes to `main` run `.github/workflows/npm-publish.yml`. The workflow validates
the package, reads the latest published npm version, bumps the patch version in
CI, and publishes the package to npm. If this GitHub repository becomes public,
the workflow can be changed to use `npm publish --provenance`.

Required GitHub repository secret:

- `NPM_TOKEN` - an npm automation token with publish access to
  `@scienceintelligence/phd`
