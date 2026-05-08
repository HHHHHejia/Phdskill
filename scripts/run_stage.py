"""Print stage instructions for a Claude Code / Codex agent.

This is a guided command. v0 deliberately does not perform research — it only
prints the contract and behaviour rules so the agent stays inside the stage.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (  # noqa: E402
    REPO_ROOT,
    STAGE_NAMES,
    expand_readable,
    expand_writable,
    gate_for_stage,
    is_stage_locked,
    required_outputs,
    stage_contract,
    stage_dir,
)


STAGE_BEHAVIOUR = {
    0: (
        "- Capture the raw idea and user constraints in 00_inbox/.\n"
        "- Do not start literature review or planning yet.\n"
    ),
    1: (
        "- Read 00_inbox/idea.md and 00_inbox/user_constraints.yaml.\n"
        "- Ask at most 5 decision-oriented clarification questions.\n"
        "- Produce research brief and literature research plan.\n"
        "- Do not start literature review, do not write paper.\n"
    ),
    2: (
        "- Search/read/summarise literature.\n"
        "- Build paper cards, knowledge pack, related-work map.\n"
        "- Propose 2-3 refined idea options and recommend one.\n"
        "- Do not write paper sections, do not run experiments.\n"
    ),
    3: (
        "- Design datasets, baselines, metrics, experiment matrix.\n"
        "- Estimate cost and risk; create approval_request.md.\n"
        "- Do not run experiments, do not change selected direction silently.\n"
    ),
    4: (
        "- Run only experiments approved in stage 3.\n"
        "- Log every command, save outputs, save metrics, record failures.\n"
        "- Do not change the experiment plan, do not delete logs.\n"
        "- If the plan must change, write 04_execution/change_request.md.\n"
    ),
    5: (
        "- Aggregate metrics; write finding cards.\n"
        "- Build claim_support_matrix.md; flag unsupported claims.\n"
        "- Do not change raw metrics, do not overstate findings.\n"
    ),
    6: (
        "- Generate figures and tables from approved analysis only.\n"
        "- Write captions; bind every figure to source data and supported claim.\n"
        "- Do not invent results, do not modify analysis.\n"
    ),
    7: (
        "- Draft narrative options, outline, claim ledger, weak spots.\n"
        "- Compile LaTeX; never write unsupported claims.\n"
        "- Do not modify experiment logs or analysis.\n"
    ),
    8: (
        "- Produce friendly, skeptical, hostile reviews and a meta review.\n"
        "- Write revision_plan.md and final_checklist.md.\n"
        "- Revisions may touch paper/ and 07_writing/claim_ledger.md only.\n"
        "- Required new experiments must go via revision_request to stage 3.\n"
        "- Do not pretend simulated reviews are real reviews.\n"
        "- Do not submit a paper without explicit final_submission gate approval.\n"
    ),
}


def render_stage(stage: int, root: Path) -> str:
    if stage not in range(len(STAGE_NAMES)):
        raise ValueError(f"unknown stage {stage}")
    contract = stage_contract(stage, root)
    name = STAGE_NAMES[stage]
    locked = is_stage_locked(stage, root)
    gate = gate_for_stage(stage, root)

    lines = []
    lines.append(f"=== Stage {stage}: {name} ===")
    lines.append(f"directory: {stage_dir(stage, root).relative_to(root)}")
    lines.append(f"locked: {locked}")
    lines.append(f"gate: {gate or '(none)'}")
    lines.append("")
    lines.append("Allowed read scope:")
    for r in expand_readable(stage, root):
        lines.append(f"  - {r}")
    lines.append("")
    lines.append("Allowed write scope:")
    for w in expand_writable(stage, root):
        lines.append(f"  - {w}")
    forbidden = contract.get("forbidden") or []
    if forbidden:
        lines.append("")
        lines.append("Forbidden in this stage:")
        for f in forbidden:
            lines.append(f"  - {f}")
    lines.append("")
    lines.append("Required outputs:")
    for r in required_outputs(stage, root):
        lines.append(f"  - {r}")
    lines.append("")
    lines.append("Behaviour rules:")
    behaviour = STAGE_BEHAVIOUR.get(stage, "(none)")
    for line in behaviour.rstrip("\n").splitlines():
        lines.append(line)
    lines.append("")
    lines.append(
        "Reminder: read AGENTS.md and SKILL.md before editing. v0 does not "
        "perform research automatically — your job is to advance the repo through "
        "this stage's contract."
    )
    return "\n".join(lines)


def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Print stage instructions.")
    parser.add_argument("stage", type=int, choices=list(range(len(STAGE_NAMES))))
    parser.add_argument("--root", default=str(REPO_ROOT))
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    print(render_stage(args.stage, Path(args.root).resolve()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
