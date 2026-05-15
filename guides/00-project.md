# 00 Project Setup

## Goal

Create the `research_project/` git repository and the numbered folder structure
for the paper project.

This step only prepares the workspace. It does not do research, design methods,
write experiment plans, run code, analyze results, or draft paper sections.

## Folder Contract

- Create or use `research_project/` as the output research repo unless the user
  explicitly points to an existing equivalent project root.
- Initialize git in `research_project/` if it is not already a git repo.
- Create only the project scaffold and the single setup record.
- Formal output for this step is `00_project_setup.md`.
- The root `README.md`, numbered-folder `README.md` logs, `.gitignore`, and
  numbered folders are setup artifacts, not research-stage outputs.

## Inputs

- User's initial research idea, even if rough.
- User constraints: target venue, deadline, compute/API budget, data/privacy
  limits, collaboration constraints, preferred paper type, and output path.

## Blank-Start Preflight

If there is no existing resumable `research_project/` and the user provided no
rough research idea, constraints, or output path beyond the command name itself,
do not create anything. Do not make directories, initialize git, write
`README.md`, write `.gitignore`, or create `00_project_setup.md`.

Ask the user for enough intent to begin:

- the rough research idea or topic
- whether to create `research_project/` in the current location
- any critical constraints such as venue, deadline, budget, data/privacy, or
  collaboration requirements

This preflight is separate from the required Step 0 pre-write questions. After
the user provides a rough idea or explicitly asks for a blank scaffold, continue
with the normal Step 0 actions.

## Actions

0. Run the blank-start preflight above before any filesystem writes.
1. Decide the output project root.
   - If the current directory already is a valid `research_project/` repo, use
     it.
   - If the current directory contains `research_project/`, use that existing
     directory.
   - If the user provided a parent path, create or use
     `<parent>/research_project/`.
   - If no path is provided but the user did provide a research idea or
     explicitly approved a blank scaffold, choose a sensible parent path and
     create `research_project/` there.
   - Ask before creating files if the location is ambiguous or risky.
2. Create the `research_project/` directory.
3. Initialize git in `research_project/` if needed.
4. Create these numbered folders inside `research_project/`:
   - `01_idea/`
   - `02_knowledge_base/`
   - `03_method/`
   - `04_experiment_plan/`
   - `05_experiment_code/`
   - `06_analysis/`
   - `07_paper_latex/`
   - `08_review/`
5. Create a root `README.md` with the append-only continuity log structure
   from `commands/phd.md`.
6. Create an append-only `README.md` continuity log in every numbered folder.
7. Create a minimal `.gitignore` that protects secrets and large/generated
   artifacts while allowing git to track code, Markdown, configs, scripts,
   manifests, metadata, and small reproducibility artifacts.
8. Before writing `00_project_setup.md`, ask the user up to 5 non-trivial,
   decision-oriented questions to clarify setup requirements. Ask only
   questions whose answers could change the repository location, project scope,
   constraints, or next action.
9. Create `00_project_setup.md`.
10. Ask up to 5 non-trivial post-write calibration questions whose answers
    could change the setup record, repository path, log scaffold, commit scope,
    or Step 1 readiness. Record them in `00_project_setup.md`.
11. Apply any needed setup revisions inside the Step 0 contract.
12. Append setup-complete entries to the root README and each folder README
    that now has an initialized status.
13. Commit the setup files in the `research_project/` git repo and push to the
    configured upstream when available. If push is unavailable, record
    `push pending` in the README logs.

## Output

Write exactly one formal Markdown output for this step:

- `00_project_setup.md`

Use this structure:

```markdown
# Project Setup

## Human Pre-Write Clarifications

## Raw Idea

## User Constraints

## Output Repository

## Folder Map

## Current Status

## Next Step

## Post-Write Calibration Questions
```

The raw idea and constraints should live in `00_project_setup.md`; do not split
them into separate stage files unless the user explicitly asks.

## Stop Gate

Stop after the repository and folder structure exist, `00_project_setup.md` is
written, the post-write checkpoint is handled, the README logs are updated, the
setup commit has been created and push has been attempted. Tell the user where
`research_project/` is, the commit/push status, and that the next step is
`01_idea`.
