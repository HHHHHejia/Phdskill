# 00 Project Setup

## Goal

Create the output git repository and the numbered folder structure for the
paper project.

This step only prepares the workspace. It does not do research, design methods,
write experiment plans, run code, analyze results, or draft paper sections.

## Folder Contract

- Create or use the output research repo.
- Initialize git if the output repo is not already a git repo.
- Create only the project scaffold and the single setup record.
- Formal output for this step is `00_project_setup.md`.
- The root `README.md`, `.gitignore`, and numbered folders are setup artifacts,
  not research-stage outputs.

## Inputs

- User's initial research idea, even if rough.
- User constraints: target venue, deadline, compute/API budget, data/privacy
  limits, collaboration constraints, preferred paper type, and output path.

## Actions

1. Decide the output repository path.
   - Use the user's path if provided.
   - If no path is provided, create a concise folder name from the idea.
   - Ask before creating files if the location is ambiguous or risky.
2. Create the output directory.
3. Initialize git in the output directory if needed.
4. Create these numbered folders:
   - `01_idea/`
   - `02_knowledge_base/`
   - `03_method/`
   - `04_experiment_plan/`
   - `05_experiment_code/`
   - `06_analysis/`
   - `07_paper_latex/`
   - `08_review/`
5. Create a minimal root `README.md`.
6. Create a minimal `.gitignore`.
7. Before writing `00_project_setup.md`, ask the user exactly 10
   decision-oriented questions to clarify setup requirements.
8. Create `00_project_setup.md`.
9. After writing `00_project_setup.md`, ask the user exactly 10 calibration
   questions before moving to Step 1.

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
written, and the 10 post-write calibration questions have been asked. Tell the
user where the repo is and that the next step is `01_idea`.
