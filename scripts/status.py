"""Print the current status of a PhD Paper Skill repository."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (  # noqa: E402
    REPO_ROOT,
    STAGE_NAMES,
    is_stage_locked,
    load_contracts,
    load_project,
    required_outputs,
    stage_dir,
)


def collect_status(root: Path) -> dict:
    project = load_project(root)
    contracts = load_contracts(root)

    current = int(project.get("current_stage", 0))
    stage_status = project.get("stage_status") or {}
    gates = project.get("gates") or {}

    locked = []
    for stage in sorted(contracts.get("stages", {}).keys()):
        if is_stage_locked(int(stage), root):
            locked.append(int(stage))

    missing = []
    for path in required_outputs(current, root):
        full = root / path
        if not full.exists() or full.stat().st_size == 0:
            missing.append(path)

    return {
        "project": project.get("project") or {},
        "current_stage": current,
        "stage_status": stage_status,
        "gates": gates,
        "locked_stages": locked,
        "missing_required_outputs_for_current_stage": missing,
        "stage_dir_for_current": str(stage_dir(current, root).relative_to(root)),
    }


def render(status: dict) -> str:
    lines = []
    title = status["project"].get("title")
    venue = status["project"].get("target_venue")
    lines.append("=== PhD Paper Skill — Project Status ===")
    if title or venue:
        lines.append(f"Project: {title or '(untitled)'}  Venue: {venue or '(unset)'}")
    cur = status["current_stage"]
    name = STAGE_NAMES[cur] if 0 <= cur < len(STAGE_NAMES) else f"unknown({cur})"
    lines.append(f"Current stage: {cur} ({name})  dir: {status['stage_dir_for_current']}")
    lines.append("")
    lines.append("Stage status:")
    for stage_name in STAGE_NAMES:
        flag = status["stage_status"].get(stage_name, "?")
        lines.append(f"  - {stage_name}: {flag}")
    lines.append("")
    lines.append("Gates:")
    for gate_name, gate_data in (status["gates"] or {}).items():
        approved = gate_data.get("approved")
        approved_at = gate_data.get("approved_at")
        lines.append(
            f"  - {gate_name}: approved={approved} approved_at={approved_at}"
        )
    lines.append("")
    lines.append("Locked stages: " + (", ".join(map(str, status["locked_stages"])) or "(none)"))
    lines.append("")
    missing = status["missing_required_outputs_for_current_stage"]
    if missing:
        lines.append("Missing required outputs for current stage:")
        for m in missing:
            lines.append(f"  - {m}")
    else:
        lines.append("Missing required outputs for current stage: (none)")
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Show PhD Paper Skill status.")
    parser.add_argument("--root", default=str(REPO_ROOT))
    args = parser.parse_args(argv)

    status = collect_status(Path(args.root).resolve())
    print(render(status))
    return 0


if __name__ == "__main__":
    sys.exit(main())
