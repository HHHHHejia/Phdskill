"""Pytest fixtures: build an isolated PhD Paper Skill repo for each test.

The skill is a repo-template, so every test runs against a freshly-initialised
copy under ``tmp_path`` to avoid coupling tests to the in-tree state.
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = REPO_ROOT / "scripts"

# Make scripts/ importable from any test.
sys.path.insert(0, str(SCRIPTS_DIR))


@pytest.fixture
def fresh_repo(tmp_path: Path) -> Path:
    """Run init_project.py against a tmp dir and return the path."""
    target = tmp_path / "repo"
    target.mkdir()
    # Always need stage_contracts.yaml — copy it across since templates only
    # cover the user-facing surface.
    (target / "schemas").mkdir(parents=True, exist_ok=True)
    shutil.copy(
        REPO_ROOT / "schemas" / "stage_contracts.yaml",
        target / "schemas" / "stage_contracts.yaml",
    )

    import init_project

    init_project.init_project(root=target, force=True)
    return target
