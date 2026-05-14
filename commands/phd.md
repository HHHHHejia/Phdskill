# /phd

Create a complete PhD-style paper project git repository from an initial
research idea. This command has the same behavior in Codex (`$phd`) and Claude
Code (`/phd`).

## Contract

- Input: the user's rough research idea plus any constraints they provide.
- Output: a git repository containing the full paper project: intake notes,
  literature plan, refined idea, knowledge pack, method specification,
  experiment plan, execution logs, analysis artifacts, writing drafts, review
  notes, and revision artifacts.

Start with Step 0. The output project root is a directory named
`research_project/` unless the user explicitly points to an existing equivalent
project root. That directory is the git repository root and must contain all
numbered workflow folders. If the current directory is already the target
`research_project/` repo, use it. If the current directory contains an existing
`research_project/`, use that. Otherwise ask for or choose a sensible parent
path, create `research_project/`, initialize git there, and create the project
structure. Do not create the paper project inside this skill repository.

Blank-start preflight is mandatory. If the user invokes the command with no
research idea, no constraints, no output path, and there is no existing
resumable `research_project/` with a root README or `00_project_setup.md`, stop
before creating any directory, git repository, README, Markdown file, or log.
The command name itself (`Phd`, `$phd`, or `/phd`) is not research input. Ask the
user for the rough research idea and whether they want to create
`research_project/` in the current location. This preflight does not count as
the formal 10-question Step 0 checkpoint. Continue Step 0 only after the user
provides enough intent to create or resume a project.

After Step 0, each step edits only its corresponding output folder plus any
explicit paper-draft side effect named in that step guide. It reads only earlier
step folders unless the user explicitly approves a revision.

For each research step, keep formal outputs to two files:

- one stage Markdown file in the step folder
- one LaTeX section file in `07_paper_latex/`

Artifacts are exceptions: Deep Research raw reports/JSON, source annotations,
paper-download manifests, downloaded PDFs, metadata, download logs,
experiment-code files, raw run folders, analysis scripts, processed
tables, generated figures, analysis logs, LaTeX source files, bibliography
files, PDFs, and LaTeX logs may live under their designated artifact folders.
Required append-only `README.md` continuity logs are also artifacts and do not
count as formal stage Markdown outputs.

Human-in-the-loop checkpoints are required for every formal stage Markdown file:

- Before creating or finalizing the stage Markdown file, ask the user exactly 10
  decision-oriented questions to clarify requirements, assumptions, constraints,
  and success criteria. Wait for the user's answers when possible.
- Record those questions and answers in the stage Markdown under
  `Human Pre-Write Clarifications`.
- After the stage Markdown and any allowed LaTeX/artifact outputs are complete,
  ask the user exactly 10 calibration questions to confirm direction, scope,
  risks, and next-step readiness.
- Record those post-write questions, and the user's answers if provided, under
  `Post-Write Calibration Questions`.
- Do not advance to the next step until the user has had a chance to respond.

Ask checkpoint questions one at a time. When the environment provides a
user-question tool such as Codex's "Ask User Question" / `request_user_input`,
use that tool for each checkpoint question, with one question per tool call, and
wait for the user's answer before asking the next question. Do not dump all 10
questions into one assistant message, one Markdown list, or one multi-question
tool call. Record each question and answer as it arrives. If no user-question
tool is available, ask exactly one concise question in normal chat and wait
before continuing.

Use progressive disclosure. The skill body is only the routing layer: identify
the active step, then load only that step's guide and only the helper script you
actually need to run or debug. Do not read all guides or all bundled scripts at
skill-load time. In Codex, guides and helper scripts are installed under
`~/.codex/skills/phd/`. In Claude Code, guides are installed under
`~/.claude/commands/phd-guides/` and helper scripts under
`~/.claude/commands/phd-scripts/`.

## Progressive Disclosure

On each invocation:

1. Read this command file first to identify the project root, continuity state,
   and active workflow step.
2. Read the root and numbered-folder README logs required by the continuity
   protocol.
3. Load exactly one current-step guide from `guides/`, unless the user
   explicitly asks for cross-step redesign or review.
4. Read earlier formal stage Markdown files only when the current guide lists
   them as inputs. Prefer README logs first to decide which heavy artifacts are
   worth reopening.
5. Open bundled helper scripts only when the current step calls for running,
   debugging, or modifying that script. Prefer `--help` and targeted `rg`/`sed`
   reads over loading whole scripts when possible.
6. Do not pre-read future-step guides, all PDFs, all raw tool outputs, all run
   folders, or the whole experiment code tree. Load them lazily when a specific
   decision or artifact path requires it.

## Deep Research Execution

All Deep Research runs must be started through
`scripts/run-deep-research-tmux.js`, which launches `deep-research-idea.js` in a
detached tmux session and returns immediately. Do not run Deep Research in the
foreground. Record the tmux session name, metadata file, log file, and status
file in the relevant folder README so a future run can resume monitoring. If
tmux is unavailable or the session cannot start, write a tool failure note and
ask the user how to proceed instead of blocking the foreground process.

| Step | Output folder | Guide | Main deliverable |
|---|---|---|---|
| 0 | repo root | `guides/00-project.md` | `00_project_setup.md` + project structure |
| 1 | `01_idea/` | `guides/01-idea.md` | `idea.md` + `intro.tex` |
| 2 | `02_knowledge_base/` | `guides/02-knowledge-base.md` | `knowledge_base.md` + `relatedwork.tex` |
| 3 | `03_method/` | `guides/03-method.md` | `method.md` + `method.tex` |
| 4 | `04_experiment_plan/` | `guides/04-experiment-plan.md` | `experiment_plan.md` + `experiments.tex` |
| 5 | `05_experiment_code/` | `guides/05-experiment-code.md` | code tree + `implementation.md` + `experiments.tex` |
| 6 | `06_analysis/` | `guides/06-analysis.md` | `analysis.md` + `results.tex` |
| 7 | `07_paper_latex/` | `guides/07-writing.md` | `writing.md` + `main.tex` + polished sections |
| 8 | `08_review/` | `guides/08-review.md` | `审稿意见.md` |

These numbered output folders live inside the generated `research_project/`
repo. They do not belong in this skill package.

## Continuity, Logs, And Git

This workflow must support resume-from-checkpoint behavior. On every invocation:

1. Identify the target `research_project/` root before doing research work.
2. If `research_project/README.md` already exists, treat the run as a resumed
   run. Read the root README first, then read every numbered folder README:
   `01_idea/README.md` through `08_review/README.md`, if present.
3. Use those logs to locate reusable artifacts, unfinished tasks, user
   decisions, blockers, and the next resume point before reading heavy artifacts
   such as PDFs, raw tool outputs, run folders, or code.
4. If a README log conflicts with the filesystem or git history, inspect
   `git status`, `git log`, and the relevant artifacts, then append a correction
   log entry. Do not rewrite old log entries.

The root README and every numbered folder README are append-only continuity
logs. Create missing README logs as soon as the folder exists. Prior entries
must not be deleted or edited unless the user explicitly asks for a correction;
even then, prefer appending a correction entry.

Root README entries should be concise and cross-stage:

```markdown
### <ISO-8601 timestamp> | <stage-id> | <task name>
- Status: <in-progress | complete | blocked | needs-human>
- Summary: <what changed>
- Changed paths: `<path>`, `<path>`
- Reusable state: <papers, code, runs, figures, decisions, or artifacts to reuse>
- Next resume point: <exact next action>
- Validation: <checks run or skipped>
- Git: commit `<hash-or-pending>`, push `<pushed | pending | unavailable>`
```

Folder README entries should be stage-local:

```markdown
### <ISO-8601 timestamp> | <task name>
- Status: <in-progress | complete | blocked | needs-human>
- Decisions: <user choices or assumptions>
- Artifacts: `<relative/path>`, `<relative/path>`
- Reusable state: <what a future run should read or reuse first>
- Next resume point: <exact next action inside this stage>
- Validation: <checks run or skipped>
- Git: commit `<hash-or-pending>`, push `<pushed | pending | unavailable>`
```

After any stage task reaches a stop gate, or after any meaningful approved
subtask changes project files, update the relevant folder README and the root
README before committing. Then run `git status`, stage the relevant safe files,
commit with a message such as `stage 02: update knowledge base`, and push to the
configured upstream. If no remote/upstream exists, or push fails because of
auth/network limits, keep the local commit, record `push pending` in both README
logs, and tell the user. Track code, Markdown, configs, scripts, manifests, and
small reproducibility artifacts in git. Do not commit secrets, credentials,
private keys, large raw datasets, large PDFs, model checkpoints, or large run
outputs unless the user explicitly approves; preserve them on disk and track
their manifests, metadata, checksums, and README log references instead.

## Hard Rules

- Do not fabricate citations, results, datasets, baselines, metrics, or logs.
- Do not cite papers that were not actually inspected.
- Preserve raw experiment logs and failed runs.
- Do not silently change hypotheses, datasets, baselines, metrics, or budget.
- Label unsupported claims as `SPECULATIVE`, `UNVERIFIED`,
  `NEEDS_VERIFICATION`, `NEEDS_EXPERIMENT`, or `NEEDS_HUMAN_DECISION`.
- Stop for explicit user approval before finalizing the refined direction,
  running experiments, accepting paper claims, or submitting.

For the required human checkpoints, ask exactly 10 questions, one at a time
using the user-question protocol above. For any other ad-hoc clarification, keep
questions concise and decision-oriented.
