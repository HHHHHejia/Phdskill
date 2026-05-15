# 03 Method

## Goal

Turn the approved idea and knowledge base into an original, testable research
method.

This step designs the method. It does not design the full experiment plan,
write code, run experiments, analyze results, or make performance claims.

## Folder Contract

- Formal stage output: write exactly one Markdown file in `03_method/`.
- Paper output: write exactly one LaTeX file in `07_paper_latex/`.
- Continuity output: append to `03_method/README.md` and the root `README.md`;
  these logs do not count as formal stage outputs.
- Read `00_project_setup.md`, `01_idea/idea.md`, and
  `02_knowledge_base/knowledge_base.md`.
- Read paper originals and metadata under `02_knowledge_base/related_works/`
  when needed for method positioning.
- Do not write experiment plans, code, analysis, review notes, or any other
  paper text yet.

## Inputs

- `00_project_setup.md`
- `01_idea/idea.md`
- `02_knowledge_base/knowledge_base.md`
- `02_knowledge_base/related_works/` paper originals and metadata
- User approval of the Step 2 direction and knowledge base

## Actions

Before the numbered actions, run the continuity resume protocol from
`commands/phd.md`: read the root README first, then every numbered folder
README, and use the logs to reuse the approved direction, literature library,
nearest prior methods, and any unresolved method-design decisions.

1. Identify the precise research gap the method should address.
2. Inspect original text of the most relevant prior papers whenever available.
   Do not rely only on survey summaries for nearest-neighbor methods.
3. Generate 2-3 plausible method candidates.
4. Select one recommended method, or ask the user to choose if the tradeoff is
   genuinely ambiguous.
5. Before writing `03_method/method.md`, ask the user up to 10 non-trivial,
   decision-oriented questions to clarify method preferences, risk tolerance,
   feasibility constraints, and novelty priorities. Ask only questions whose
   answers could change the selected method, assumptions, hypotheses, risks, or
   next action.
6. Specify the selected method concretely enough for Step 4 experiment planning:
   inputs, outputs, mechanism, assumptions, tunable parts, baselines, ablations,
   and expected failure modes.
7. Write falsifiable hypotheses. Avoid vague claims such as "better
   performance"; specify what should improve, against what baseline, and under
   what condition.
8. Mark unsupported design claims as `SPECULATIVE`, `NEEDS_VERIFICATION`,
   `NEEDS_EXPERIMENT`, or `NEEDS_HUMAN_DECISION`.
9. Append completion or blocked-state entries to `03_method/README.md` and the
    root `README.md`, then commit and push according to the git protocol in
    `commands/phd.md`.

## Output

Write exactly one formal Markdown output:

- `03_method/method.md`

Use this structure:

```markdown
# Method

## Human Pre-Write Clarifications

## Research Gap

## Relevant Prior Methods

## Method Candidates

## Selected Method

## Method Specification

## Novelty Positioning

## Assumptions And Risks

## Testable Hypotheses

## Step 4 Experiment Planning Brief
```

Do not create any other formal Markdown files for this step; fold all sections
into `method.md`.

## Paper LaTeX Output

Write exactly one paper-section output:

- `07_paper_latex/method.tex`

This should be a method-section draft, not a results section. It must:

- explain the proposed mechanism or procedure clearly
- cite only prior work recorded in `02_knowledge_base/`
- avoid fabricated equations, algorithms, modules, datasets, or citations
- use `% TODO:` comments where details depend on Step 4 or Step 5
- avoid claiming the method outperforms baselines before experiments exist
- include placeholders for algorithm boxes, diagrams, or notation only when
  genuinely needed

## Stop Gate

Stop after `03_method/method.md` and `07_paper_latex/method.tex` are written,
the README logs are updated, and commit/push has been attempted. Summarize the
selected method, why it is plausibly novel, the strongest risks, the hypotheses
Step 4 should test, and the commit/push status.

Do not move to experiment planning until the user approves the method.
