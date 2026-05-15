# 04 Experiment Plan

## Goal

Turn the approved method into a concrete, auditable experiment plan.

This step designs experiments. It does not write implementation code, run
experiments, analyze results, or change the selected method. If the method
cannot be tested under the user's constraints, write the issue inside
`experiment_plan.md` and stop.

## Folder Contract

- Formal stage output: write exactly one Markdown file in
  `04_experiment_plan/`.
- Paper output: write exactly one LaTeX file in `07_paper_latex/`.
- Continuity output: append to `04_experiment_plan/README.md` and the root
  `README.md`; these logs do not count as formal stage outputs.
- Read `00_project_setup.md`, `01_idea/idea.md`,
  `02_knowledge_base/knowledge_base.md`, and `03_method/method.md`.
- Do not write experiment code, run logs, analysis, review notes, or any other
  paper text yet.
- Do not silently change the method, hypotheses, datasets, baselines, metrics,
  budget, or evaluation protocol.

## Inputs

- `00_project_setup.md`
- `01_idea/idea.md`
- `02_knowledge_base/knowledge_base.md`
- `03_method/method.md`
- User approval of the Step 3 method direction

## Actions

Before the numbered actions, run the continuity resume protocol from
`commands/phd.md`: read the root README first, then every numbered folder
README, and use the logs to reuse approved hypotheses, method constraints,
dataset or baseline decisions, and unresolved experiment-planning blockers.

1. Convert each method hypothesis into one or more experiments.
2. Define datasets, tasks, environments, or evaluation cases. Mark anything not
   supported by the knowledge base as `NEEDS_HUMAN_DECISION` or
   `NEEDS_VERIFICATION`.
3. Choose baselines from the knowledge base and method positioning, including a
   strong prior-work baseline, a simple baseline, and ablations.
4. Define metrics and success criteria. Specify what each metric measures and
   which claim it supports.
5. Specify ablations, robustness checks, negative controls, and failure cases.
6. Build a run matrix detailed enough for Step 5 implementation. If structured
   data is useful, embed it as fenced JSON inside `experiment_plan.md` rather
   than creating a separate JSON file.
7. Identify data, compute, privacy, ethics, cost, and reproducibility risks.
8. Before writing `04_experiment_plan/experiment_plan.md`, ask the user up to 5
   non-trivial, decision-oriented questions to clarify datasets, baselines,
   metrics, ablations, budget, and approval constraints. Ask only questions
   whose answers could change the run matrix, evaluation protocol, cost,
   privacy constraints, or next action.
9. State what the user must approve before code or experiments begin.
10. Ask up to 5 non-trivial post-write calibration questions whose answers
    could change datasets, baselines, metrics, run matrix, budget, approval
    request, or Step 5 readiness. Record them in
    `04_experiment_plan/experiment_plan.md`.
11. Apply any needed Step 4 revisions before logging or committing.
12. Append completion or blocked-state entries to
    `04_experiment_plan/README.md` and the root `README.md`, then commit and
    push according to the git protocol in `commands/phd.md`.

## Output

Write exactly one formal Markdown output:

- `04_experiment_plan/experiment_plan.md`

Use this structure:

```markdown
# Experiment Plan

## Human Pre-Write Clarifications

## Approved Method Summary

## Claims And Hypotheses To Test

## Datasets Tasks And Environments

## Baselines

## Metrics And Success Criteria

## Ablations Controls And Robustness Checks

## Run Matrix

## Budget And Risks

## Implementation Requirements For Step 5

## Approval Request

## Method Revision Needed

## Post-Write Calibration Questions
```

Do not create any other formal Markdown or JSON files for this step; fold all
sections into `experiment_plan.md`.

## Paper LaTeX Output

Write exactly one paper-section output:

- `07_paper_latex/experiments.tex`

This should be an experimental-setup draft, not a results section. It must:

- describe datasets, tasks, baselines, metrics, and protocol
- cite only datasets, benchmarks, and baselines recorded in the project
- avoid reporting any result before experiments are run
- use `% TODO:` comments for values that depend on Step 5 execution, such as
  number of runs, exact hyperparameters, hardware, runtime, and sample counts
- keep the evaluation logic clear enough that Step 5 can implement it without
  changing the scientific question

## Stop Gate

Stop after `04_experiment_plan/experiment_plan.md` and
`07_paper_latex/experiments.tex` are written, the post-write checkpoint is
handled, the README logs are updated, and commit/push has been attempted. Ask
the user to approve or modify datasets, baselines, metrics, ablations, budget,
and any privacy or data-access constraints, and report the commit/push status.

Do not move to experiment code or run any experiment until the user approves
the plan.
