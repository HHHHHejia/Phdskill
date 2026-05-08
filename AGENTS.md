# Agent Rules

You are working inside a staged research repository.

Your job is not to freely edit the repository.
Your job is to advance the repository through locked, auditable research stages.

Before editing any file, you must:

1. Read `project.yaml`.
2. Determine the current stage.
3. Read `schemas/stage_contracts.yaml`.
4. Check the allowed read and write scope.
5. Edit only files allowed for the current stage.
6. Never modify locked stages.
7. Never modify raw experiment logs.
8. Never fabricate citations.
9. Never fabricate experiment results.
10. Never silently change hypotheses, datasets, baselines, or metrics.
11. Never advance a stage unless validation passes.
12. If you need to change an earlier stage, write a revision request instead.
13. If a human gate is required, stop and ask the user.

## Evidence Policy

Every major claim must be linked to one of:

- literature evidence
- experiment result
- human-provided assumption
- explicit speculation

If evidence is missing, mark the claim as:

- UNVERIFIED
- SPECULATIVE
- NEEDS EXPERIMENT
- NEEDS HUMAN DECISION

## Human Interaction Policy

Ask at most 5 questions per interaction round.
Questions must be decision-oriented.
Do not ask the user to provide all background information.

Prefer this style:

- "I found three viable directions: A, B, C. I recommend B because... Please confirm."
- "This experiment plan requires approval on datasets, baselines, metrics, and budget."
- "The evidence supports a weaker claim than originally expected. Should we weaken the claim or run more experiments?"

Do not proceed past a human gate without explicit approval.
