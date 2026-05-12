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

Start with Step 0. If the user is already inside a target research repo, use it.
If not, ask for or choose a sensible output repo path, create it, initialize
git, and create the project structure. Do not create the paper project inside
this skill repository.

After Step 0, each step edits only its corresponding output folder plus any
explicit paper-draft side effect named in that step guide. It reads only earlier
step folders unless the user explicitly approves a revision.

For each research step, keep formal outputs to two files:

- one stage Markdown file in the step folder
- one LaTeX section file in `07_paper_latex/`

Artifacts are exceptions: Deep Research raw reports/JSON, source annotations,
paper-download manifests, downloaded PDFs, metadata, download logs,
experiment-code repository files, raw run folders, analysis scripts, processed
tables, generated figures, analysis logs, LaTeX source files, bibliography
files, PDFs, and LaTeX logs may live under their designated artifact folders.

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

Load only the guide needed for the current step. In Codex, guides and helper
scripts are installed under `~/.codex/skills/phd/`. In Claude Code, guides are
installed under `~/.claude/commands/phd-guides/` and helper scripts under
`~/.claude/commands/phd-scripts/`.

| Step | Output folder | Guide | Main deliverable |
|---|---|---|---|
| 0 | repo root | `guides/00-project.md` | `00_project_setup.md` + project structure |
| 1 | `01_idea/` | `guides/01-idea.md` | `idea.md` + `intro.tex` |
| 2 | `02_knowledge_base/` | `guides/02-knowledge-base.md` | `knowledge_base.md` + `relatedwork.tex` |
| 3 | `03_method/` | `guides/03-method.md` | `method.md` + `method.tex` |
| 4 | `04_experiment_plan/` | `guides/04-experiment-plan.md` | `experiment_plan.md` + `experiments.tex` |
| 5 | `05_experiment_code/` | `guides/05-experiment-code.md` | code repo + `implementation.md` + `experiments.tex` |
| 6 | `06_analysis/` | `guides/06-analysis.md` | `analysis.md` + `results.tex` |
| 7 | `07_paper_latex/` | `guides/07-writing.md` | `writing.md` + `main.tex` + polished sections |
| 8 | `08_review/` | `guides/08-review.md` | `审稿意见.md` |

These numbered output folders are outputs of the workflow in the generated project
repo. They do not belong in this skill package.

## Hard Rules

- Do not fabricate citations, results, datasets, baselines, metrics, or logs.
- Do not cite papers that were not actually inspected.
- Preserve raw experiment logs and failed runs.
- Do not silently change hypotheses, datasets, baselines, metrics, or budget.
- Label unsupported claims as `SPECULATIVE`, `UNVERIFIED`,
  `NEEDS_VERIFICATION`, `NEEDS_EXPERIMENT`, or `NEEDS_HUMAN_DECISION`.
- Stop for explicit user approval before finalizing the refined direction,
  running experiments, accepting paper claims, or submitting.

For the required human checkpoints, ask exactly 10 questions. For any other
ad-hoc clarification, keep questions concise and decision-oriented.
