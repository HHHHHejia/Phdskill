from __future__ import annotations

from pathlib import Path

import pytest
import yaml

import gate as gate_mod
import lock_stage
import validate_stage as vs


def _project(repo: Path) -> dict:
    with (repo / "project.yaml").open() as h:
        return yaml.safe_load(h)


def test_cannot_lock_with_missing_outputs(fresh_repo: Path):
    # Stage 1 (intake) is not seeded by init_project as required outputs by
    # default — its placeholders are non-empty, so we delete one to simulate
    # a missing output.
    (fresh_repo / "01_intake" / "research_brief.md").unlink()
    # Approve the gate so the gate isn't the failing reason.
    gate_mod.approve_gate(fresh_repo, "research_direction", notes="ok")
    with pytest.raises(RuntimeError) as exc:
        lock_stage.lock_stage(fresh_repo, stage=1)
    assert "validation failed" in str(exc.value)


def test_cannot_lock_gate_required_stage_without_approval(fresh_repo: Path):
    # Stage 1 has a required gate (research_direction); without approval lock
    # must fail.
    with pytest.raises(RuntimeError) as exc:
        lock_stage.lock_stage(fresh_repo, stage=1)
    msg = str(exc.value)
    assert "research_direction" in msg or "not approved" in msg


def test_can_lock_stage_after_outputs_and_gate(fresh_repo: Path):
    gate_mod.approve_gate(fresh_repo, "research_direction", notes="ok")
    lock_path = lock_stage.lock_stage(fresh_repo, stage=1)
    assert lock_path.exists()

    with lock_path.open() as h:
        lock_doc = yaml.safe_load(h)
    assert lock_doc["status"] == "locked"
    assert lock_doc["stage_index"] == 1
    assert lock_doc["output_hashes"], "lock file should contain output hashes"
    for entry in lock_doc["output_hashes"]:
        assert "sha256" in entry and len(entry["sha256"]) == 64

    proj = _project(fresh_repo)
    assert proj["stage_status"]["intake"] == "locked"


def test_modifying_locked_output_causes_validation_failure(fresh_repo: Path):
    gate_mod.approve_gate(fresh_repo, "research_direction", notes="ok")
    lock_stage.lock_stage(fresh_repo, stage=1)

    # Tamper with a locked output.
    brief = fresh_repo / "01_intake" / "research_brief.md"
    brief.write_text(brief.read_text() + "\n\ntampered\n")

    results = vs.validate_stage(fresh_repo)
    assert vs.has_errors(results)
    assert any(
        "hash mismatch" in err for err in results["locked_stages"]
    ), results


def test_lock_stage_advances_current_stage(fresh_repo: Path):
    # Lock stage 0 (no gate) first so current_stage advances.
    lock_stage.lock_stage(fresh_repo, stage=0)
    proj = _project(fresh_repo)
    assert proj["current_stage"] == 1
    assert proj["stage_status"]["inbox"] == "locked"
    assert proj["stage_status"]["intake"] == "in_progress"


def test_double_lock_without_force_fails(fresh_repo: Path):
    lock_stage.lock_stage(fresh_repo, stage=0)
    with pytest.raises(RuntimeError):
        lock_stage.lock_stage(fresh_repo, stage=0)
    # With force, succeeds.
    lock_stage.lock_stage(fresh_repo, stage=0, force=True)
