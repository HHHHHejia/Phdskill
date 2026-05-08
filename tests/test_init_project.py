from __future__ import annotations

from pathlib import Path

import yaml

import init_project


def test_init_project_creates_project_yaml(fresh_repo: Path):
    project_path = fresh_repo / "project.yaml"
    assert project_path.exists()
    with project_path.open() as handle:
        data = yaml.safe_load(handle)
    assert data["current_stage"] == 0
    assert "gates" in data
    assert "stage_status" in data


def test_init_project_creates_all_stage_folders(fresh_repo: Path):
    expected = [
        "00_inbox",
        "01_intake",
        "02_literature",
        "03_experiment_plan",
        "04_execution",
        "05_analysis",
        "06_figures",
        "07_writing",
        "08_review",
        "experiments",
        "figures",
        "tables",
        "paper",
        "paper/sections",
        "schemas",
    ]
    for rel in expected:
        assert (fresh_repo / rel).exists(), f"missing {rel}"


def test_init_project_creates_required_placeholder_files(fresh_repo: Path):
    expected_files = [
        "00_inbox/idea.md",
        "00_inbox/user_constraints.yaml",
        "01_intake/research_brief.md",
        "01_intake/clarification_questions.md",
        "01_intake/literature_research_plan.md",
        "01_intake/decision_log.md",
        "02_literature/search_queries.yaml",
        "02_literature/paper_cards.yaml",
        "02_literature/knowledge_pack.md",
        "02_literature/related_work_map.md",
        "02_literature/novelty_gap_analysis.md",
        "02_literature/refined_idea_options.md",
        "02_literature/selected_direction.md",
        "03_experiment_plan/experiment_plan.md",
        "03_experiment_plan/experiment_matrix.yaml",
        "03_experiment_plan/datasets.md",
        "03_experiment_plan/baselines.md",
        "03_experiment_plan/metrics.md",
        "03_experiment_plan/cost_risk.md",
        "03_experiment_plan/approval_request.md",
        "04_execution/run_manifest.yaml",
        "04_execution/run_log.md",
        "04_execution/experiment_status.yaml",
        "04_execution/errors.md",
        "04_execution/change_request.md",
        "05_analysis/results_summary.md",
        "05_analysis/finding_cards.yaml",
        "05_analysis/claim_support_matrix.md",
        "05_analysis/statistical_analysis.md",
        "05_analysis/failure_analysis.md",
        "06_figures/figure_plan.md",
        "06_figures/captions.md",
        "07_writing/narrative_options.md",
        "07_writing/outline.md",
        "07_writing/claim_ledger.md",
        "07_writing/weak_spots.md",
        "08_review/review_friendly.md",
        "08_review/review_skeptical.md",
        "08_review/review_hostile.md",
        "08_review/meta_review.md",
        "08_review/revision_plan.md",
        "08_review/final_checklist.md",
        "08_review/required_followup_experiments.md",
        "paper/main.tex",
        "paper/references.bib",
        "paper/sections/01_introduction.tex",
        "paper/sections/02_related_work.tex",
        "paper/sections/03_method.tex",
        "paper/sections/04_experiments.tex",
        "paper/sections/05_results.tex",
        "paper/sections/06_discussion.tex",
        "paper/sections/07_limitations.tex",
    ]
    for rel in expected_files:
        path = fresh_repo / rel
        assert path.exists(), f"missing {rel}"
        assert path.stat().st_size > 0, f"empty {rel}"


def test_init_project_does_not_overwrite_non_empty_files_by_default(fresh_repo: Path):
    idea_path = fresh_repo / "00_inbox" / "idea.md"
    idea_path.write_text("# my custom idea\n\nThis must not be overwritten.\n")
    init_project.init_project(root=fresh_repo, force=False)
    assert "my custom idea" in idea_path.read_text()


def test_init_project_force_overwrites(fresh_repo: Path):
    idea_path = fresh_repo / "00_inbox" / "idea.md"
    idea_path.write_text("# custom\n")
    init_project.init_project(root=fresh_repo, force=True)
    assert idea_path.read_text().startswith("# Raw Research Idea")


def test_init_project_seeds_idea_text(tmp_path: Path):
    target = tmp_path / "repo"
    target.mkdir()
    (target / "schemas").mkdir(parents=True, exist_ok=True)
    import shutil
    from conftest import REPO_ROOT
    shutil.copy(
        REPO_ROOT / "schemas" / "stage_contracts.yaml",
        target / "schemas" / "stage_contracts.yaml",
    )
    init_project.init_project(root=target, idea="study skill induction in LLMs", force=True)
    idea = (target / "00_inbox" / "idea.md").read_text()
    assert "skill induction in LLMs" in idea
