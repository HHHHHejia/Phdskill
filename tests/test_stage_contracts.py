from __future__ import annotations

from pathlib import Path

import yaml

from _common import is_within_writable


def test_stage_contracts_parses(fresh_repo: Path):
    contracts_path = fresh_repo / "schemas" / "stage_contracts.yaml"
    with contracts_path.open() as handle:
        contracts = yaml.safe_load(handle)
    assert "stages" in contracts


def test_all_stages_have_required_fields(fresh_repo: Path):
    with (fresh_repo / "schemas" / "stage_contracts.yaml").open() as handle:
        contracts = yaml.safe_load(handle)
    for stage_id, contract in contracts["stages"].items():
        assert "name" in contract, f"stage {stage_id} missing name"
        assert "readable" in contract, f"stage {stage_id} missing readable"
        assert "writable" in contract, f"stage {stage_id} missing writable"
        assert "required_outputs" in contract, f"stage {stage_id} missing required_outputs"


def test_required_outputs_inside_writable_scope(fresh_repo: Path):
    with (fresh_repo / "schemas" / "stage_contracts.yaml").open() as handle:
        contracts = yaml.safe_load(handle)
    for stage_id, contract in contracts["stages"].items():
        writable = contract.get("writable") or []
        for required in contract.get("required_outputs") or []:
            assert is_within_writable(required, writable), (
                f"stage {stage_id} required output {required} is outside writable scope"
            )


def test_all_referenced_gates_exist_in_project_yaml(fresh_repo: Path):
    with (fresh_repo / "schemas" / "stage_contracts.yaml").open() as handle:
        contracts = yaml.safe_load(handle)
    with (fresh_repo / "project.yaml").open() as handle:
        project = yaml.safe_load(handle)
    project_gates = set((project.get("gates") or {}).keys())
    for stage_id, contract in contracts["stages"].items():
        gate = contract.get("gate")
        if gate:
            assert gate in project_gates, (
                f"stage {stage_id} references unknown gate '{gate}'"
            )


def test_stage_indices_are_contiguous(fresh_repo: Path):
    with (fresh_repo / "schemas" / "stage_contracts.yaml").open() as handle:
        contracts = yaml.safe_load(handle)
    keys = sorted(contracts["stages"].keys())
    assert keys == list(range(len(keys))), f"expected 0..N-1 but got {keys}"
