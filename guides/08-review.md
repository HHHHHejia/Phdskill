# 08 Review

## Goal

Review the completed paper as a critical domain expert and write reviewer-style
comments.

This step is read-only with respect to research artifacts outside `08_review/`
and the required root README log. It identifies weaknesses, missing evidence,
overclaims, unclear writing, invalid comparisons, and likely reviewer
objections. It does not modify code, experiments, analysis, or LaTeX paper
files.

## Folder Contract

- Write only in `08_review/`, except for the required root README log update.
- Formal stage output: write exactly one Markdown file in `08_review/`.
- Continuity output: append to `08_review/README.md` and the root `README.md`;
  these logs do not count as formal stage outputs.
- Read the completed paper under `07_paper_latex/`.
- Read all earlier formal stage outputs and evidence artifacts as needed.
- Do not modify `05_experiment_code/`, `06_analysis/`, `07_paper_latex/`, or
  any earlier step folder.
- Do not fabricate additional experiments, citations, results, or reviewer
  praise.

## Inputs

- `07_paper_latex/main.tex`
- section files under `07_paper_latex/`
- `07_paper_latex/references.bib`
- `07_paper_latex/writing.md`
- `06_analysis/analysis.md`
- `06_analysis/figures/`
- `06_analysis/results/`
- all earlier formal stage Markdown files

## Actions

Before the numbered actions, run the continuity resume protocol from
`commands/phd.md`: read the root README first, then every numbered folder
README, and use the logs to reuse prior review criteria, paper build status,
known evidence gaps, and unresolved revision priorities.

1. Read the paper as if reviewing for a serious venue in the relevant field.
2. Check whether the problem, novelty, method, experiments, and claims are
   aligned.
3. Compare claims against available evidence from literature, experiments, and
   analysis. Mark unsupported claims directly.
4. Identify missing baselines, weak metrics, confounds, failed or incomplete
   ablations, dataset limitations, statistical issues, and reproducibility
   concerns.
5. Identify writing problems: unclear motivation, weak positioning, ambiguous
   method description, missing limitations, unsupported conclusion, or broken
   narrative flow.
6. Before writing `08_review/审稿意见.md`, ask the user up to 10 non-trivial,
   decision-oriented questions to clarify review strictness, target venue,
   reviewer persona, and preferred criticism depth. Ask only questions whose
   answers could change the review standard, severity, venue assumptions,
   critique format, or next action.
7. Produce reviewer-style criticism with severity and actionable fixes.
8. Recommend a verdict such as strong reject, reject, borderline, weak accept,
   or accept, with honest justification.
9. Append completion or blocked-state entries to `08_review/README.md` and the
    root `README.md`, then commit and push according to the git protocol in
    `commands/phd.md`.

## Output

Write exactly one formal Markdown output:

- `08_review/审稿意见.md`

Use this structure:

```markdown
# 审稿意见

## Human Pre-Write Clarifications

## Overall Summary

## Main Strengths

## Major Weaknesses

## Required Revisions

## Missing Evidence Or Experiments

## Method And Experiment Concerns

## Writing And Presentation Concerns

## Reproducibility Concerns

## Claim-By-Claim Check

## Suggested Verdict

## Priority Fix List
```

Be specific. Reference paper sections, figures, tables, claims, and evidence
paths when possible. Do not create other formal review files.

## Paper LaTeX Output

None.

Do not edit `07_paper_latex/` in this step. The output is criticism only.

## Stop Gate

Stop after `08_review/审稿意见.md` is written, the README logs are updated, and
commit/push has been attempted. Summarize:

- suggested verdict
- top 3-5 blocking issues
- strongest missing evidence
- highest-impact revisions
- the commit/push status

Do not modify code, analysis, experiments, or LaTeX files.
