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
2. Start the bundled Deep Research helper in a detached tmux session:

   ```bash
   node <path-to-phd-skill>/scripts/run-deep-research-tmux.js \
     --project-root <output-repo>
   ```

   Do not run `deep-research-idea.js` directly in the foreground. The tmux
   wrapper returns immediately and writes session metadata, logs, and completion
   status under `01_idea/tool_outputs/`.
3. Record the tmux session name and log path in `01_idea/README.md`. Check
   progress with `tmux capture-pane -pt <session>` or the log file. After the
   tmux job finishes successfully, read the raw tool outputs in
   `01_idea/tool_outputs/`.
4. Before writing `01_idea/idea.md`, ask the user up to 10 non-trivial,
   decision-oriented questions to clarify the research direction, constraints,
   and success criteria. Ask only questions whose answers could change the
   selected direction, evidence needs, scope, feasibility judgment, or next
   action.
5. Synthesize the evidence into the single formal output `01_idea/idea.md`.
6. Recommend one next direction if the evidence supports it; otherwise mark the
   uncertainty directly.
7. Append completion or blocked-state entries to `01_idea/README.md` and the
   root `README.md`, then commit and push according to the git protocol in
   `commands/phd.md`.

If tmux is unavailable or the helper cannot start, write the failure note in
`01_idea/tool_outputs/tool_failure.md` and ask before continuing without Deep
Research. Do not fall back to a foreground Deep Research run.

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
README logs are updated and commit/push has been attempted. Ask which direction
the user wants to pursue before building the knowledge base, and report the
commit/push status.
