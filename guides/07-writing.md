# 07 Writing

## Goal

Polish the paper writing and complete the LaTeX paper project under
`07_paper_latex/`.

This step turns the accumulated section drafts into a coherent paper. It may
edit LaTeX source, bibliography, captions, macros, and build files, but it must
not change the research idea, method, experiment plan, code, raw results, or
analysis evidence.

## Folder Contract

- Work only inside `07_paper_latex/`, except for the required root README log
  update.
- Formal stage output: write exactly one Markdown file in `07_paper_latex/`.
- Continuity output: append to `07_paper_latex/README.md` and the root
  `README.md`; these logs do not count as formal stage outputs.
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

Before the numbered actions, run the continuity resume protocol from
`commands/phd.md`: read the root README first, then every numbered folder
README, and use the logs to reuse existing section drafts, citation decisions,
figures, tables, build status, and unresolved paper TODOs.

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
7. Write and revise the LaTeX paper with the four-pass writing protocol below.
   Do the passes in order and record the outcome of each pass in `writing.md`.
8. Ensure every major claim is traceable to literature, analysis, result
   artifacts, human assumptions, or an explicit TODO label.
9. Add or repair figure/table includes only for artifacts that exist under
   `06_analysis/`.
10. Run a LaTeX compile check if a TeX toolchain is available. If not, record
   the missing toolchain in `writing.md`.
11. Fix obvious LaTeX errors, missing includes, broken references, and undefined
   citations when the fix is evidence-preserving.
12. After writing `07_paper_latex/writing.md` and polishing the LaTeX paper,
    add exactly 10 post-write calibration questions to
    `07_paper_latex/writing.md`.
13. Append completion or blocked-state entries to `07_paper_latex/README.md`
    and the root `README.md`, then commit and push according to the git protocol
    in `commands/phd.md`.
14. Ask the user those exact 10 calibration questions before moving to Step 8.

## Four-Pass Writing Protocol

Use this protocol for every substantial LaTeX writing or revision task:

1. Fix the logical structure.
   - Decide the paper-level argument before polishing sentences.
   - Make section order, subsection order, figure/table placement, and claim
     dependencies explicit.
   - Ensure each section has one job and hands off cleanly to the next section.
   - Remove or mark paragraphs that do not support the central argument.
2. Draft the content.
   - Fill each section with evidence-grounded content using the existing stage
     files, figures, tables, and bibliography.
   - Keep claims provisional when evidence is incomplete.
   - Use `% TODO:` comments for missing citations, missing results, unclear
     notation, unresolved venue requirements, or decisions needing the user.
3. Increase information density.
   - Replace vague motivation, generic background, and filler transitions with
     concrete claims, mechanisms, comparisons, numbers, or evidence paths.
   - Merge repetitive paragraphs and move low-value detail to appendix-style
     material only when appropriate.
   - Make every sentence either establish context, state a claim, support a
     claim, explain the method, report evidence, qualify uncertainty, or guide
     the reader through the argument.
4. Polish grammar and style.
   - Improve clarity, grammar, transitions, terminology consistency, and
     LaTeX readability without changing the scientific meaning.
   - Preserve citations, claim strength, evidence labels, and TODOs.
   - Do not make the prose sound more certain than the evidence allows.

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

## Four-Pass Writing Log

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
written, the README logs are updated, and commit/push has been attempted, then
ask the 10 post-write calibration questions. Summarize:

- the paper structure
- which LaTeX files were created or updated
- whether the paper compiled
- unresolved citation, figure, table, or evidence TODOs
- what Step 8 should review most critically
- the commit/push status

Do not move to review until the user approves the written draft.
