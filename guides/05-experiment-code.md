# 05 Experiment Code

## Goal

Create runnable experiment code inside `05_experiment_code/` and track code
changes with the root `research_project/` git repository.

This step writes code. It may run cheap unit tests or smoke tests, but it does
not run full experiments, analyze results, or change the approved plan.

## Folder Contract

- Work only inside `05_experiment_code/`, except for the paper output named
  below.
- Do not initialize `05_experiment_code/` as a nested git repository unless the
  user explicitly asks. The root `research_project/` git repo tracks experiment
  code changes.
- Formal stage output: write exactly one Markdown file in
  `05_experiment_code/`.
- Continuity output: append to `05_experiment_code/README.md` and the root
  `README.md`; these logs do not count as formal stage outputs.
- Code artifacts are allowed inside `05_experiment_code/`: source files,
  configs, tests, scripts, dependency files, environment templates, and small
  fixtures.
- Paper output: write or update exactly one LaTeX file in `07_paper_latex/`.
- Read `00_project_setup.md`, `01_idea/idea.md`,
  `02_knowledge_base/knowledge_base.md`, `03_method/method.md`, and
  `04_experiment_plan/experiment_plan.md`.
- Do not write analysis files, result claims, review notes, or any other paper
  text yet.
- Do not run expensive or full experiment jobs unless the user explicitly
  approves.

## Inputs

- `00_project_setup.md`
- `01_idea/idea.md`
- `02_knowledge_base/knowledge_base.md`
- `03_method/method.md`
- `04_experiment_plan/experiment_plan.md`
- User approval of the Step 4 experiment plan

## Actions

Before the numbered actions, run the continuity resume protocol from
`commands/phd.md`: read the root README first, then every numbered folder
README, and use the logs to reuse existing code, configs, tests, run-storage
contracts, smoke-test status, and known blockers instead of scaffolding from
scratch.

1. Create `05_experiment_code/` if needed and ensure it is tracked by the root
   `research_project/` git repo.
2. Choose the smallest implementation stack that satisfies the experiment plan
   and user constraints.
3. Before writing code or `05_experiment_code/implementation.md`, ask the user
   up to 10 non-trivial, decision-oriented questions to clarify implementation
   stack, runtime constraints, logging needs, and run storage expectations. Ask
   only questions whose answers could change the code architecture,
   dependencies, run-storage contract, validation plan, or next action.
4. Scaffold a runnable code tree with dependency files, source code, configs,
   scripts, tests, and concise usage notes in `implementation.md` or another
   clearly named artifact if needed. Preserve `05_experiment_code/README.md` as
   the append-only continuity log.
5. Implement the approved method, baselines, dataset/task loading, metrics, and
   logging conventions from `04_experiment_plan/experiment_plan.md`.
6. Use predictable paths inside `05_experiment_code/`:
   - `src/` or equivalent for implementation code
   - `configs/` for experiment configs
   - `scripts/` or `bin/` for runnable entrypoints
   - `tests/` for unit, integration, or smoke tests
   - `runs/<run_id>/` for real experiment outputs
   - `runs/<run_id>/logs/` for stdout, stderr, and runtime logs
   - `runs/<run_id>/results/` for metrics, predictions, summaries, and raw
     result files
   - `runs/<run_id>/artifacts/` for checkpoints, cached model outputs, or other
     generated artifacts
7. Each real run should be able to record `command.txt`, `config.json`,
   `metadata.json`, logs, metrics, and result files under its own run folder.
8. Keep large or generated run folders out of git by default. Commit only small
   fixtures or example outputs when useful.
9. Provide clear commands for:
   - installing dependencies
   - running smoke tests
   - running each planned experiment later
   - writing outputs to predictable paths
10. Add tests or dry-run checks for the core pipeline when feasible.
11. Run only cheap checks by default, such as syntax checks, unit tests, or
   smoke tests with tiny fixtures.
12. Record what was implemented, how to run it, and what checks passed in
   `05_experiment_code/implementation.md`.
13. Append completion or blocked-state entries to `05_experiment_code/README.md`
    and the root `README.md`, then commit and push according to the git protocol
    in `commands/phd.md`.

Do not silently change datasets, baselines, metrics, hypotheses, or budget. If
the approved plan cannot be implemented as written, document the blocker in
`implementation.md` and stop.

## Output

Write exactly one formal Markdown output:

- `05_experiment_code/implementation.md`

Use this structure:

```markdown
# Implementation

## Human Pre-Write Clarifications

## Approved Plan Summary

## Code Repository Layout

## Implemented Components

## Install And Environment

## Commands

## Configs And Outputs

## Run Storage Contract

## Smoke Tests And Validation

## Known Gaps Or Blockers

## Step 6 Analysis Handoff
```

Do not create any other formal Markdown report for this step. Code files,
configs, tests, scripts, lockfiles, and small fixtures are implementation
artifacts and may exist inside the `05_experiment_code/` git repo.

## Paper LaTeX Output

Write or update exactly one paper-section output:

- `07_paper_latex/experiments.tex`

Only add implementation or reproducibility details that are already known, such
as software stack, evaluation protocol, planned command structure, or logging
format. Do not report results. Use `% TODO:` comments for details that depend
on full experiment execution.

## Stop Gate

Stop after the code tree is created, the implementation is written, and cheap
checks have been run or explicitly skipped with a reason, the README logs are
updated, and commit/push has been attempted. Summarize:

- where the experiment code directory is
- which components were implemented
- how to run smoke tests
- how to run the planned experiments later
- what blockers remain, if any
- the commit/push status

Do not run full experiments until the user approves.
