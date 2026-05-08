"""Lock a stage after validation and (where required) gate approval.

Writes a ``.stage.lock`` file inside the stage directory containing SHA-256
hashes of every required output. Updates ``project.yaml`` to mark the stage
``locked`` and advances ``current_stage`` if the locked stage was the current
one and the next stage exists.
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (  # noqa: E402
    REPO_ROOT,
    STAGE_NAMES,
    gate_approved,
    gate_for_stage,
    is_stage_locked,
    load_contracts,
    load_project,
    required_outputs,
    save_project,
    sha256_file,
    stage_lock_file,
)
from validate_stage import has_errors, render, validate_stage  # noqa: E402


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _input_hashes(stage: int, root: Path) -> list:
    """Hash readable, file-shaped previous-stage outputs.

    We hash ``required_outputs`` of every previous stage that still exists,
    because those are the inputs the current stage logically depends on.
    """
    contracts = load_contracts(root)
    stages = contracts.get("stages") or {}
    inputs = []
    for prev in sorted(stages.keys()):
        prev = int(prev)
        if prev >= stage:
            continue
        for rel in required_outputs(prev, root):
            target = root / rel
            if target.exists() and target.is_file():
                inputs.append({"file": rel, "sha256": sha256_file(target)})
    return inputs


def lock_stage(
    root: Path,
    stage: Optional[int] = None,
    *,
    human_approved: Optional[bool] = None,
    force: bool = False,
) -> Path:
    project = load_project(root)
    if stage is None:
        stage = int(project.get("current_stage", 0))

    if is_stage_locked(stage, root) and not force:
        raise RuntimeError(
            f"stage {stage} is already locked. Pass --force to re-lock."
        )

    results = validate_stage(root, stage=stage, check_gate=True)
    if has_errors(results):
        raise RuntimeError("validation failed:\n" + render(results))

    gate = gate_for_stage(stage, root)
    if gate is not None and not gate_approved(project, gate):
        raise RuntimeError(
            f"gate '{gate}' for stage {stage} is not approved in project.yaml"
        )

    output_hashes = []
    for rel in required_outputs(stage, root):
        target = root / rel
        if target.exists() and target.is_file():
            output_hashes.append({"file": rel, "sha256": sha256_file(target)})

    lock_doc = {
        "stage": f"{stage:02d}_{STAGE_NAMES[stage]}",
        "stage_index": stage,
        "status": "locked",
        "locked_at": now_iso(),
        "locked_by": "ai",
        "human_approved": (
            human_approved if human_approved is not None else (gate is not None)
        ),
        "input_hashes": _input_hashes(stage, root),
        "output_hashes": output_hashes,
    }

    lock_path = stage_lock_file(stage, root)
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(lock_doc, handle, sort_keys=False, allow_unicode=True)

    stage_status = project.setdefault("stage_status", {})
    stage_status[STAGE_NAMES[stage]] = "locked"
    if int(project.get("current_stage", 0)) == stage:
        contracts = load_contracts(root)
        if (stage + 1) in (contracts.get("stages") or {}):
            project["current_stage"] = stage + 1
            stage_status[STAGE_NAMES[stage + 1]] = "in_progress"
    save_project(project, root)

    return lock_path


def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Lock a stage.")
    parser.add_argument("--stage", type=int, default=None)
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--root", default=str(REPO_ROOT))
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    try:
        path = lock_stage(
            Path(args.root).resolve(), stage=args.stage, force=args.force
        )
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    print(f"stage locked: {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
