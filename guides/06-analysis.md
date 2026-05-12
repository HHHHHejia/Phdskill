# 06 Analysis

## Goal

Analyze completed experiment outputs, write reusable analysis and plotting
scripts, store analysis artifacts, and draft the paper results section.

This step turns raw run outputs into evidence. It does not change the method,
experiment plan, code, datasets, baselines, or metrics after seeing results.

## Folder Contract

- Work only inside `06_analysis/`, except for the paper output named below.
- Formal stage output: write exactly one Markdown file in `06_analysis/`.
- Analysis artifacts are allowed inside `06_analysis/`: scripts, small helper
  modules, processed result tables, generated figures, plot logs, and cached
  intermediate files.
- Paper output: write or update exactly one LaTeX file in `07_paper_latex/`.
- Read `00_project_setup.md`, `01_idea/idea.md`,
  `02_knowledge_base/knowledge_base.md`, `03_method/method.md`,
  `04_experiment_plan/experiment_plan.md`, and
  `05_experiment_code/implementation.md`.
- Read experiment outputs from `05_experiment_code/runs/<run_id>/` or from
  explicit external result paths listed in `05_experiment_code/implementation.md`.
- Never modify raw experiment logs, raw result files, configs, or code in
  `05_experiment_code/`.

## Inputs

- `04_experiment_plan/experiment_plan.md`
- `05_experiment_code/implementation.md`
- `05_experiment_code/runs/<run_id>/` raw outputs, logs, configs, metrics, and
  result files
- any user-provided location of external run outputs

## Actions

1. Locate completed run folders and verify each has enough metadata to identify
   command, config, method variant, baseline, dataset/task, seed, and metrics.
2. Refuse to analyze missing or ambiguous runs as if they were real evidence.
   Mark gaps as `NEEDS_EXPERIMENT` or `NEEDS_VERIFICATION`.
3. Before writing analysis scripts or `06_analysis/analysis.md`, ask the user
   exactly 10 decision-oriented questions to clarify analysis priorities,
   statistical expectations, plotting needs, and claim boundaries.
4. Write analysis scripts in `06_analysis/scripts/`.
5. Write plotting scripts in `06_analysis/plots/` or another clearly named
   scripts folder under `06_analysis/`.
6. Store processed tables under `06_analysis/results/`.
7. Store generated figures under `06_analysis/figures/`.
8. Store analysis logs under `06_analysis/logs/`.
9. Compute metrics exactly as defined in `04_experiment_plan/experiment_plan.md`.
   If the planned metric cannot be computed, document why and do not substitute
   another metric silently.
10. Compare against planned baselines and ablations. Separate confirmed findings
   from weak, failed, or inconclusive evidence.
11. Produce publication-ready figure/table artifacts when possible, with source
   data paths recorded in `analysis.md`.
12. After writing `06_analysis/analysis.md` and `07_paper_latex/results.tex`,
    ask the user exactly 10 calibration questions before moving to Step 7.

## Output

Write exactly one formal Markdown output:

- `06_analysis/analysis.md`

Use this structure:

```markdown
# Analysis

## Human Pre-Write Clarifications

## Run Inventory

## Data Integrity Checks

## Metric Computation

## Main Results

## Baseline And Ablation Comparisons

## Robustness And Failure Cases

## Figures And Tables

## Claim Support

## Limitations

## Step 7 Writing Handoff

## Post-Write Calibration Questions
```

Do not create any other formal Markdown report for this step. Analysis scripts,
plot scripts, processed tables, generated figures, and logs are analysis
artifacts and may exist under `06_analysis/`.

## Paper LaTeX Output

Write or update exactly one paper-section output:

- `07_paper_latex/results.tex`

This should be a results-section draft grounded only in analyzed experiment
outputs. It must:

- cite figure/table files from `06_analysis/figures/` and
  `06_analysis/results/`
- report only metrics that were actually computed
- distinguish confirmed, inconclusive, and failed results
- avoid overstating unsupported claims
- use `% TODO:` comments for missing runs, unresolved statistics, or claims
  requiring more experiments

## Stop Gate

Stop after `06_analysis/analysis.md` and `07_paper_latex/results.tex` are
written and the 10 post-write calibration questions have been asked. Summarize:

- which runs were analyzed
- where processed results, figures, tables, and logs were stored
- which claims are supported
- which claims are weak, failed, or still need experiments
- what Step 7 should write or soften in the paper

Do not move to writing refinement until the user approves the analysis.
