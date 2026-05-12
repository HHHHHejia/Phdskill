# 07 Writing

## Goal

Polish the paper writing and complete the LaTeX paper project under
`07_paper_latex/`.

This step turns the accumulated section drafts into a coherent paper. It may
edit LaTeX source, bibliography, captions, macros, and build files, but it must
not change the research idea, method, experiment plan, code, raw results, or
analysis evidence.

## Folder Contract

- Work only inside `07_paper_latex/`.
- Formal stage output: write exactly one Markdown file in `07_paper_latex/`.
- Paper artifacts are allowed inside `07_paper_latex/`: `.tex`, `.bib`, style
  files, figure/table references, build scripts, generated PDFs, and LaTeX logs.
- Read `00_project_setup.md`, `01_idea/idea.md`,
  `02_knowledge_base/knowledge_base.md`, `03_method/method.md`,
  `04_experiment_plan/experiment_plan.md`,
  `05_experiment_code/implementation.md`, and `06_analysis/analysis.md`.
- Read figures/tables from `06_analysis/figures/` and `06_analysis/results/`.
- Do not modify earlier step folders.
- Do not fabricate citations, claims, experimental results, limitations, or
  comparisons.

## Inputs

- `07_paper_latex/intro.tex`
- `07_paper_latex/relatedwork.tex`
- `07_paper_latex/method.tex`
- `07_paper_latex/experiments.tex`
- `07_paper_latex/results.tex`
- `06_analysis/analysis.md`
- `06_analysis/figures/`
- `06_analysis/results/`
- all earlier formal stage Markdown files

## Actions

1. Create or update the LaTeX project structure under `07_paper_latex/`.
2. Before writing `07_paper_latex/writing.md` or polishing the final LaTeX
   draft, ask the user exactly 10 decision-oriented questions to clarify target
   venue, tone, claim strength, narrative emphasis, and formatting needs.
3. Create or update the required paper entrypoint:
   - `07_paper_latex/main.tex`
4. Make `main.tex` import section modules with `\input{...}` rather than
   pasting all section text into one file.
5. Organize section files consistently, reusing existing section drafts when
   present.
6. Create or update bibliography files from sources already recorded in the
   project. Do not invent citation keys or bibliographic metadata.
7. Polish the narrative:
   - sharpen the problem statement
   - align contributions with actual evidence
   - connect related work to the method
   - make the experiment setup readable
   - present results without overclaiming
   - state limitations honestly
8. Ensure every major claim is traceable to literature, analysis, result
   artifacts, human assumptions, or an explicit TODO label.
9. Add or repair figure/table includes only for artifacts that exist under
   `06_analysis/`.
10. Run a LaTeX compile check if a TeX toolchain is available. If not, record
   the missing toolchain in `writing.md`.
11. Fix obvious LaTeX errors, missing includes, broken references, and undefined
   citations when the fix is evidence-preserving.
12. After writing `07_paper_latex/writing.md` and polishing the LaTeX paper,
    ask the user exactly 10 calibration questions before moving to Step 8.

## Output

Write exactly one formal Markdown output:

- `07_paper_latex/writing.md`

Also create or update the required LaTeX entrypoint:

- `07_paper_latex/main.tex`

Use this structure:

```markdown
# Writing

## Human Pre-Write Clarifications

## Paper Structure

## LaTeX Project Layout

## Narrative Changes

## Claim Evidence Check

## Citation Check

## Figure And Table Integration

## Build Check

## Remaining TODOs

## Step 8 Review Handoff

## Post-Write Calibration Questions
```

Do not create any other formal Markdown report for this step. LaTeX source
files, bibliography files, build files, PDFs, and LaTeX logs are paper artifacts
and may exist under `07_paper_latex/`.

## Paper LaTeX Output

Complete and polish the LaTeX paper under `07_paper_latex/`. The required
entrypoint is:

- `main.tex`

`main.tex` should use `\input{...}` to include section modules. A typical
structure is:

```tex
\input{intro}
\input{relatedwork}
\input{method}
\input{experiments}
\input{results}
\input{discussion}
\input{limitations}
\input{conclusion}
```

Expected section and support files may include:

- `intro.tex`
- `relatedwork.tex`
- `method.tex`
- `experiments.tex`
- `results.tex`
- `discussion.tex`
- `limitations.tex`
- `conclusion.tex`
- `references.bib`

Only create section files that are useful for the paper. Keep section names
simple and consistent. Use `% TODO:` comments for missing evidence, unresolved
citations, or claims that need user approval.

## Stop Gate

Stop after the LaTeX paper is polished and `07_paper_latex/writing.md` is
written, then ask the 10 post-write calibration questions. Summarize:

- the paper structure
- which LaTeX files were created or updated
- whether the paper compiled
- unresolved citation, figure, table, or evidence TODOs
- what Step 8 should review most critically

Do not move to review until the user approves the written draft.
