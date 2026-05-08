"""Approve human gates for the PhD Paper Skill.

Usage examples:

    python scripts/gate.py approve research_direction --notes "Approved direction"
    python scripts/gate.py approve refined_idea --selected-option A
    python scripts/gate.py approve experiment_plan --max-compute-budget "200 GPU-hours"
    python scripts/gate.py approve claims --approved-claims claim001 claim003
    python scripts/gate.py approve final_submission

Approving a gate is recorded in ``project.yaml`` with an ISO-8601 UTC timestamp.
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import REPO_ROOT, load_project, save_project  # noqa: E402

GATE_NAMES = [
    "research_direction",
    "refined_idea",
    "experiment_plan",
    "claims",
    "final_submission",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def approve_gate(
    root: Path,
    name: str,
    notes: Optional[str] = None,
    selected_option: Optional[str] = None,
    max_compute_budget: Optional[str] = None,
    max_api_budget: Optional[str] = None,
    approved_claims: Optional[List[str]] = None,
    rejected_claims: Optional[List[str]] = None,
) -> dict:
    if name not in GATE_NAMES:
        raise ValueError(f"unknown gate '{name}'. Known: {GATE_NAMES}")

    project = load_project(root)
    gates = project.setdefault("gates", {})
    gate = gates.setdefault(name, {})
    gate["approved"] = True
    gate["approved_at"] = now_iso()
    if notes is not None:
        gate["notes"] = notes
    if name == "refined_idea" and selected_option is not None:
        gate["selected_option"] = selected_option
    if name == "experiment_plan":
        if max_compute_budget is not None:
            gate["max_compute_budget"] = max_compute_budget
        if max_api_budget is not None:
            gate["max_api_budget"] = max_api_budget
    if name == "claims":
        if approved_claims is not None:
            gate["approved_claims"] = list(approved_claims)
        if rejected_claims is not None:
            gate["rejected_claims"] = list(rejected_claims)

    save_project(project, root)
    return gate


def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Approve human gates.")
    sub = parser.add_subparsers(dest="action", required=True)

    approve = sub.add_parser("approve", help="Approve a gate.")
    approve.add_argument("name", choices=GATE_NAMES)
    approve.add_argument("--notes")
    approve.add_argument("--selected-option")
    approve.add_argument("--max-compute-budget")
    approve.add_argument("--max-api-budget")
    approve.add_argument("--approved-claims", nargs="*")
    approve.add_argument("--rejected-claims", nargs="*")
    approve.add_argument("--root", default=str(REPO_ROOT))

    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    if args.action == "approve":
        gate = approve_gate(
            Path(args.root).resolve(),
            args.name,
            notes=args.notes,
            selected_option=args.selected_option,
            max_compute_budget=args.max_compute_budget,
            max_api_budget=args.max_api_budget,
            approved_claims=args.approved_claims,
            rejected_claims=args.rejected_claims,
        )
        print(f"gate '{args.name}' approved at {gate['approved_at']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
