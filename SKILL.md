# PhD Paper Skill

This skill helps a researcher turn an initial research idea into an evidence-grounded paper draft.

The skill follows eight stages:

1. Idea intake and clarification
2. Literature research and idea refinement
3. Experiment plan refinement
4. Experiment execution
5. Experimental data analysis
6. Figure and table generation
7. Paper writing and refinement
8. Critical review and revision

The skill must be simple, but not simpler.
It must maximize automation after approval, but must stop and ask the human at high-uncertainty or high-impact decision points.

The AI must never:

- fabricate citations
- fabricate results
- hide failed experiments
- silently change metrics
- silently change hypotheses
- overclaim beyond evidence
- delete raw logs
- treat simulated reviews as real reviews
- submit a paper without explicit user approval
- make authorship decisions
- use private or sensitive data without approval
- run expensive experiments without approval

Every stage is a transaction:

1. read allowed inputs
2. write allowed outputs
3. validate outputs
4. request human approval if needed
5. lock the stage after approval
6. advance to the next stage

The repository is the source of truth.
