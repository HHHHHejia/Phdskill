"""Validate the current (or specified) stage of a PhD Paper Skill repo.

Validation rules implemented in v0:

1. ``project.yaml`` exists and parses.
2. ``schemas/stage_contracts.yaml`` exists and parses.
3. ``current_stage`` is valid.
4. Required outputs for the stage exist.
5. Required outputs are non-empty.
6. Known YAML files parse.
7. Known JSON files parse.
8. Locked previous stages still have matching hashes.
9. If a gate is required, ``project.yaml`` must show that gate approved
   before lock.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Optional

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import (  # noqa: E402
    CONTRACTS_FILE,
    PROJECT_FILE,
    REPO_ROOT,
    gate_approved,
    gate_for_stage,
    is_stage_locked,
    load_contracts,
    load_project,
    required_outputs,
    sha256_file,
    stage_dir,
    stage_lock_file,
)


def _validate_basic(root: Path) -> List[str]:
    errors: List[str] = []
    if not (root / "project.yaml").exists():
        errors.append("project.yaml missing")
    if not (root / "schemas" / "stage_contracts.yaml").exists():
        errors.append("schemas/stage_contracts.yaml missing")
    return errors


def _validate_yaml_parses(root: Path) -> List[str]:
    errors: List[str] = []
    for path in root.rglob("*.yaml"):
        if ".git" in path.parts:
            continue
        try:
            with path.open("r", encoding="utf-8") as handle:
                yaml.safe_load(handle)
        except yaml.YAMLError as exc:
            errors.append(f"YAML parse error in {path.relative_to(root)}: {exc}")
    return errors


def _validate_json_parses(root: Path) -> List[str]:
    errors: List[str] = []
    for path in root.rglob("*.json"):
        if ".git" in path.parts:
            continue
        try:
            with path.open("r", encoding="utf-8") as handle:
                json.load(handle)
        except json.JSONDecodeError as exc:
            errors.append(f"JSON parse error in {path.relative_to(root)}: {exc}")
    return errors


def _validate_required_outputs(root: Path, stage: int) -> List[str]:
    errors: List[str] = []
    for rel in required_outputs(stage, root):
        path = root / rel
        if not path.exists():
            errors.append(f"missing required output: {rel}")
        elif path.stat().st_size == 0:
            errors.append(f"required output is empty: {rel}")
    return errors


def _validate_locked_stages(root: Path) -> List[str]:
    errors: List[str] = []
    contracts = load_contracts(root)
    for stage_id in sorted(contracts.get("stages", {}).keys()):
        stage_id = int(stage_id)
        if not is_stage_locked(stage_id, root):
            continue
        lock_path = stage_lock_file(stage_id, root)
        try:
            with lock_path.open("r", encoding="utf-8") as handle:
                lock = yaml.safe_load(handle) or {}
        except yaml.YAMLError as exc:
            errors.append(f"could not parse lock {lock_path.relative_to(root)}: {exc}")
            continue
        for entry in lock.get("output_hashes") or []:
            file_rel = entry.get("file")
            expected = entry.get("sha256")
            if not file_rel or not expected:
                continue
            target = root / file_rel
            if not target.exists():
                errors.append(
                    f"locked stage {stage_id}: output {file_rel} missing on disk"
                )
                continue
            actual = sha256_file(target)
            if actual != expected:
                errors.append(
                    f"locked stage {stage_id}: hash mismatch on {file_rel}"
                )
    return errors


def _validate_gate(root: Path, stage: int) -> List[str]:
    errors: List[str] = []
    project = load_project(root)
    gate = gate_for_stage(stage, root)
    if gate and not gate_approved(project, gate):
        errors.append(
            f"stage {stage} requires gate '{gate}' but it is not approved in project.yaml"
        )
    return errors


def validate_stage(
    root: Path, stage: Optional[int] = None, *, check_gate: bool = False
) -> Dict[str, List[str]]:
    """Run validation and return a {category: [errors]} dict."""
    results: Dict[str, List[str]] = {
        "basic": [],
        "yaml": [],
        "json": [],
        "required_outputs": [],
        "locked_stages": [],
        "gate": [],
    }

    results["basic"] = _validate_basic(root)
    if results["basic"]:
        return results

    results["yaml"] = _validate_yaml_parses(root)
    results["json"] = _validate_json_parses(root)

    project = load_project(root)
    if stage is None:
        stage = int(project.get("current_stage", 0))

    contracts = load_contracts(root)
    if stage not in contracts.get("stages", {}):
        results["basic"].append(f"current_stage {stage} not in stage_contracts.yaml")
        return results

    results["required_outputs"] = _validate_required_outputs(root, stage)
    results["locked_stages"] = _validate_locked_stages(root)
    if check_gate:
        results["gate"] = _validate_gate(root, stage)
    return results


def has_errors(results: Dict[str, List[str]]) -> bool:
    return any(v for v in results.values())


def render(results: Dict[str, List[str]]) -> str:
    lines = []
    if not has_errors(results):
        lines.append("validate_stage: OK")
        return "\n".join(lines)
    lines.append("validate_stage: FAILED")
    for category, errs in results.items():
        for err in errs:
            lines.append(f"  [{category}] {err}")
    return "\n".join(lines)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Validate the current stage.")
    parser.add_argument("--stage", type=int, default=None)
    parser.add_argument(
        "--check-gate",
        action="store_true",
        help="Also enforce that the gate for the stage is approved.",
    )
    parser.add_argument("--root", default=str(REPO_ROOT))
    args = parser.parse_args(argv)

    results = validate_stage(
        Path(args.root).resolve(), stage=args.stage, check_gate=args.check_gate
    )
    print(render(results))
    return 1 if has_errors(results) else 0


if __name__ == "__main__":
    sys.exit(main())
