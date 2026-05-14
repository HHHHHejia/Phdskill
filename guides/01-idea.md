# 01 Idea

## Goal

Turn the user's vague initial idea into a feasibility assessment, preliminary
reference map, and recommended research direction.

This step is not for making a final paper claim. Many initial ideas are already
done, too broad, underspecified, or hard to evaluate. Use preliminary literature
research to help the user choose a sharper direction.

## Folder Contract

- Formal stage output: write exactly one Markdown file in `01_idea/`.
- Paper output: write exactly one LaTeX file in `07_paper_latex/`.
- Continuity output: append to `01_idea/README.md` and the root `README.md`;
  these logs do not count as formal stage outputs.
- Allowed tool artifacts: `01_idea/tool_outputs/` may contain raw Deep Research
  reports, raw JSON, source annotations, and tool failure notes.
- Read `00_project_setup.md` and root project metadata.
- Do not write to `02_knowledge_base/` yet.

## Inputs

- `00_project_setup.md`
- User answers or clarifications provided after Step 0

## Actions

Before the numbered actions, run the continuity resume protocol from
`commands/phd.md`: read the root README first, then every numbered folder
README, and use the logs to continue from the latest recorded state rather than
starting over.

1. Read the raw idea and constraints from `00_project_setup.md`.
2. Run the bundled Deep Research helper:

   ```bash
   node <path-to-phd-skill>/scripts/deep-research-idea.js \
     --project-root <output-repo>
   ```

3. Read the raw tool outputs in `01_idea/tool_outputs/`.
4. Before writing `01_idea/idea.md`, ask the user exactly 10
   decision-oriented questions to clarify the research direction, constraints,
   and success criteria.
5. Synthesize the evidence into the single formal output `01_idea/idea.md`.
6. After writing `01_idea/idea.md` and `07_paper_latex/intro.tex`, add exactly
   10 post-write calibration questions to `01_idea/idea.md`.
7. Recommend one next direction if the evidence supports it; otherwise mark the
   uncertainty directly.
8. Append completion or blocked-state entries to `01_idea/README.md` and the
   root `README.md`, then commit and push according to the git protocol in
   `commands/phd.md`.
9. Ask the user those exact 10 calibration questions before moving to Step 2.

If the helper cannot run, write the failure note in
`01_idea/tool_outputs/tool_failure.md` and ask before continuing without Deep
Research.

## Output

Write exactly one formal Markdown output:

- `01_idea/idea.md`

Use this structure:

```markdown
# Idea

## Human Pre-Write Clarifications

## Raw Input

## Feasibility Assessment

## Prior Work Snapshot

## Reference Papers And Source Leads

## Novelty Risks

## Evaluation Possibilities

## Pivot Options

## Recommended Direction

## Step 2 Literature Plan

## Post-Write Calibration Questions
```

Do not create any other formal Markdown files for this step; fold all sections
into `idea.md`.

## Paper LaTeX Output

Write exactly one paper-section output:

- `07_paper_latex/intro.tex`

This should be an early introduction draft. It must:

- motivate the problem using only Step 1 evidence
- mark uncertain statements with `% TODO: verify`
- present the contribution as a tentative direction, not a proven result
- cite only sources listed in `01_idea/idea.md`
- leave TODOs for claims needing Step 2 literature or later experiments

## Stop Gate

Stop after `01_idea/idea.md` and `07_paper_latex/intro.tex` are written and the
README logs are updated, commit/push has been attempted, and the 10 post-write
calibration questions have been asked. Ask which direction the user wants to
pursue before building the knowledge base, and report the commit/push status.
