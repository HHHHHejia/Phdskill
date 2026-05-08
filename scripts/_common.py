"""Shared helpers for the PhD Paper Skill scripts.

Keep this module dependency-light: only the Python standard library plus
PyYAML, since v0 deliberately avoids heavy dependencies.
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

import yaml


REPO_ROOT = Path(__file__).resolve().parent.parent
PROJECT_FILE = REPO_ROOT / "project.yaml"
CONTRACTS_FILE = REPO_ROOT / "schemas" / "stage_contracts.yaml"

STAGE_NAMES = [
    "inbox",
    "intake",
    "literature",
    "experiment_plan",
    "execution",
    "analysis",
    "figures",
    "writing",
    "review",
]

STAGE_DIRS = {
    0: "00_inbox",
    1: "01_intake",
    2: "02_literature",
    3: "03_experiment_plan",
    4: "04_execution",
    5: "05_analysis",
    6: "06_figures",
    7: "07_writing",
    8: "08_review",
}


def load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def dump_yaml(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.safe_dump(data, handle, sort_keys=False, allow_unicode=True)


def load_project(root: Path = REPO_ROOT) -> Dict[str, Any]:
    return load_yaml(root / "project.yaml")


def save_project(data: Dict[str, Any], root: Path = REPO_ROOT) -> None:
    dump_yaml(root / "project.yaml", data)


def load_contracts(root: Path = REPO_ROOT) -> Dict[str, Any]:
    return load_yaml(root / "schemas" / "stage_contracts.yaml")


def stage_contract(stage: int, root: Path = REPO_ROOT) -> Dict[str, Any]:
    contracts = load_contracts(root)
    stages = contracts.get("stages") or {}
    if stage not in stages:
        raise KeyError(f"Stage {stage} not defined in stage_contracts.yaml")
    return stages[stage]


def stage_dir(stage: int, root: Path = REPO_ROOT) -> Path:
    return root / STAGE_DIRS[stage]


def stage_lock_file(stage: int, root: Path = REPO_ROOT) -> Path:
    return stage_dir(stage, root) / ".stage.lock"


def is_stage_locked(stage: int, root: Path = REPO_ROOT) -> bool:
    return stage_lock_file(stage, root).exists()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def required_outputs(stage: int, root: Path = REPO_ROOT) -> List[str]:
    contract = stage_contract(stage, root)
    return list(contract.get("required_outputs") or [])


def expand_writable(stage: int, root: Path = REPO_ROOT) -> List[str]:
    contract = stage_contract(stage, root)
    return list(contract.get("writable") or [])


def expand_readable(stage: int, root: Path = REPO_ROOT) -> List[str]:
    contract = stage_contract(stage, root)
    return list(contract.get("readable") or [])


def is_within_writable(target: str, writable_patterns: Iterable[str]) -> bool:
    """Check whether `target` (a repo-relative path) is covered by any glob.

    Patterns may end with `**` (recursive) or be exact paths.
    """
    target = target.strip("/")
    for pattern in writable_patterns:
        pattern = pattern.strip("/")
        if pattern == target:
            return True
        if pattern.endswith("/**"):
            prefix = pattern[:-3]
            if target == prefix.rstrip("/") or target.startswith(prefix):
                return True
        if pattern.endswith("**"):
            prefix = pattern[:-2]
            if target.startswith(prefix):
                return True
    return False


def gate_for_stage(stage: int, root: Path = REPO_ROOT) -> Optional[str]:
    return stage_contract(stage, root).get("gate")


def gate_approved(project: Dict[str, Any], gate_name: str) -> bool:
    gates = project.get("gates") or {}
    gate = gates.get(gate_name) or {}
    return bool(gate.get("approved"))


def repo_relative(path: Path, root: Path = REPO_ROOT) -> str:
    return str(path.resolve().relative_to(root.resolve()))


def file_nonempty(path: Path) -> bool:
    if not path.exists():
        return False
    if path.is_dir():
        # treat a non-empty directory as non-empty
        return any(p for p in path.iterdir() if p.name != ".gitkeep")
    return path.stat().st_size > 0


def find_repo_root(start: Optional[Path] = None) -> Path:
    """Walk upwards looking for project.yaml. Falls back to REPO_ROOT."""
    cur = (start or Path.cwd()).resolve()
    for candidate in [cur, *cur.parents]:
        if (candidate / "project.yaml").exists() and (candidate / "schemas" / "stage_contracts.yaml").exists():
            return candidate
    return REPO_ROOT
