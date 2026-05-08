"""Default templates for the PhD Paper Skill repository skeleton.

These are used by ``scripts/init_project.py`` when seeding a fresh project.
They mirror the placeholder files committed to the repository so a freshly
initialised checkout matches the contract.
"""
from __future__ import annotations

from typing import Dict


def _project_yaml() -> str:
    return (
        "project:\n"
        "  title: null\n"
        "  field: null\n"
        "  target_venue: null\n"
        "  paper_type: null\n"
        "current_stage: 0\n"
        "stage_status:\n"
        "  inbox: in_progress\n"
        "  intake: not_started\n"
        "  literature: not_started\n"
        "  experiment_plan: not_started\n"
        "  execution: not_started\n"
        "  analysis: not_started\n"
        "  figures: not_started\n"
        "  writing: not_started\n"
        "  review: not_started\n"
        "gates:\n"
        "  research_direction:\n"
        "    approved: false\n"
        "    approved_at: null\n"
        "    notes: null\n"
        "  refined_idea:\n"
        "    approved: false\n"
        "    approved_at: null\n"
        "    selected_option: null\n"
        "    notes: null\n"
        "  experiment_plan:\n"
        "    approved: false\n"
        "    approved_at: null\n"
        "    max_compute_budget: null\n"
        "    max_api_budget: null\n"
        "    notes: null\n"
        "  claims:\n"
        "    approved: false\n"
        "    approved_at: null\n"
        "    approved_claims: []\n"
        "    rejected_claims: []\n"
        "    notes: null\n"
        "  final_submission:\n"
        "    approved: false\n"
        "    approved_at: null\n"
        "    notes: null\n"
        "permissions:\n"
        "  enforce_write_scopes: true\n"
        "  require_stage_validation: true\n"
        "  allow_backtracking_only_by_revision_request: true\n"
        "evidence_policy:\n"
        "  no_fabricated_citations: true\n"
        "  no_fabricated_results: true\n"
        "  claim_requires_evidence: true\n"
        "  preserve_raw_logs: true\n"
        "budget:\n"
        "  compute_budget: null\n"
        "  api_budget: null\n"
        "  external_api_allowed: false\n"
        "  sensitive_data_allowed: false\n"
        "human_preferences:\n"
        "  max_questions_per_round: 5\n"
        "  prefer_autonomy_after_approval: true\n"
        "  writing_style: top-conference concise\n"
        "  risk_tolerance: conservative claims\n"
        "open_questions: []\n"
        "decisions: []\n"
        "risks: []\n"
    )


TEMPLATES: Dict[str, str] = {
    "project.yaml": _project_yaml(),
    "00_inbox/idea.md": (
        "# Raw Research Idea\n\n"
        "## User Idea\n\n"
        "## User Context\n\n"
        "## Known Constraints\n\n"
        "## Open Ambiguities\n"
    ),
    "00_inbox/user_constraints.yaml": (
        "target_venue: null\n"
        "deadline: null\n"
        "compute_budget: null\n"
        "api_budget: null\n"
        "external_api_allowed: false\n"
        "sensitive_data_allowed: false\n"
        "collaboration_constraints: null\n"
        "ethics_constraints: null\n"
        "preferred_writing_style: null\n"
        "preferred_paper_type: null\n"
        "risk_tolerance: null\n"
        "notes: null\n"
    ),
    "01_intake/research_brief.md": (
        "# Research Brief\n\n"
        "## Working Title\n\n"
        "## One-sentence Idea\n\n"
        "## Problem\n\n"
        "## Why It Matters\n\n"
        "## Object of Study\n\n"
        "## Candidate Paper Type\n\n"
        "## Candidate Target Venue\n\n"
        "## Initial Hypothesis\n\n"
        "## What Would Count as Success?\n\n"
        "## Main Uncertainties\n\n"
        "## AI Recommendation\n"
    ),
    "01_intake/clarification_questions.md": (
        "# Clarification Questions\n\n"
        "The AI must ask at most 5 questions.\n\n"
        "## Questions\n\n"
        "1.\n"
        "2.\n"
        "3.\n"
        "4.\n"
        "5.\n\n"
        "## Why These Questions Matter\n\n"
        "## Decisions Blocked by These Questions\n"
    ),
    "01_intake/literature_research_plan.md": (
        "# Literature Research Plan\n\n"
        "## Scope\n\n"
        "## Search Themes\n\n"
        "## Candidate Sources\n\n"
        "## Inclusion Criteria\n\n"
        "## Exclusion Criteria\n\n"
        "## Expected Outputs\n\n"
        "## Time Budget\n"
    ),
    "01_intake/decision_log.md": (
        "# Decision Log\n\n"
        "| Date | Decision | Rationale | Approved By |\n"
        "|---|---|---|---|\n"
    ),
    "02_literature/search_queries.yaml": (
        "queries:\n"
        "  - id: q001\n"
        "    query: null\n"
        "    source: null\n"
        "    rationale: null\n"
        "    expected_paper_count: null\n"
    ),
    "02_literature/paper_cards.yaml": (
        "papers:\n"
        "  - id: paper001\n"
        "    title: null\n"
        "    authors: []\n"
        "    year: null\n"
        "    venue: null\n"
        "    url: null\n"
        "    bibtex_key: null\n"
        "    problem: null\n"
        "    method: null\n"
        "    dataset: null\n"
        "    evaluation: null\n"
        "    main_claim: null\n"
        "    limitations: null\n"
        "    relevance_to_project: null\n"
        "    threat_to_novelty: null\n"
        "    useful_for: null\n"
        "    confidence: null\n"
    ),
    "02_literature/knowledge_pack.md": (
        "# Knowledge Pack\n\n"
        "## Field Background\n\n"
        "## Core Concepts\n\n"
        "## Key Methods\n\n"
        "## Major Datasets\n\n"
        "## Open Problems\n\n"
        "## How This Project Fits\n"
    ),
    "02_literature/related_work_map.md": (
        "# Related Work Map\n\n"
        "## Clusters\n\n"
        "## Cluster A\n\n"
        "## Cluster B\n\n"
        "## Cluster C\n\n"
        "## Project Position Within Map\n"
    ),
    "02_literature/novelty_gap_analysis.md": (
        "# Novelty Gap Analysis\n\n"
        "## What Has Been Done\n\n"
        "## What Has Not Been Done\n\n"
        "## Why The Gap Exists\n\n"
        "## Risk That The Gap Is Closed Soon\n\n"
        "## Defensible Novel Contribution Candidates\n"
    ),
    "02_literature/refined_idea_options.md": (
        "# Refined Idea Options\n\n"
        "## Option A\n\n"
        "### One-sentence Idea\n\n"
        "### Hypothesis\n\n"
        "### Required Evidence\n\n"
        "### Risks\n\n"
        "### Estimated Cost\n\n"
        "## Option B\n\n"
        "### One-sentence Idea\n\n"
        "### Hypothesis\n\n"
        "### Required Evidence\n\n"
        "### Risks\n\n"
        "### Estimated Cost\n\n"
        "## Option C\n\n"
        "### One-sentence Idea\n\n"
        "### Hypothesis\n\n"
        "### Required Evidence\n\n"
        "### Risks\n\n"
        "### Estimated Cost\n\n"
        "## AI Recommendation\n"
    ),
    "02_literature/selected_direction.md": (
        "# Selected Direction\n\n"
        "## Selected Option\n\n"
        "## Final One-sentence Idea\n\n"
        "## Final Hypothesis\n\n"
        "## Why This Was Chosen\n\n"
        "## Approval\n"
    ),
    "03_experiment_plan/experiment_plan.md": (
        "# Experiment Plan\n\n"
        "## Hypothesis\n\n"
        "## Experimental Tiers\n\n"
        "### Tier 1 — Sanity\n\n"
        "### Tier 2 — Core\n\n"
        "### Tier 3 — Stretch\n\n"
        "## Open Risks\n\n"
        "## Pre-registration Notes\n"
    ),
    "03_experiment_plan/experiment_matrix.yaml": (
        "hypothesis:\n"
        "  primary: \"\"\n"
        "  secondary: []\n"
        "datasets:\n"
        "  - id: dataset001\n"
        "    name: null\n"
        "    source: null\n"
        "    license: null\n"
        "    size: null\n"
        "    reason: null\n"
        "    approved: false\n"
        "baselines:\n"
        "  - id: baseline001\n"
        "    name: null\n"
        "    repo: null\n"
        "    paper: null\n"
        "    reason: null\n"
        "    risk: null\n"
        "    approved: false\n"
        "metrics:\n"
        "  - id: metric001\n"
        "    name: null\n"
        "    definition: null\n"
        "    reason: null\n"
        "    failure_mode: null\n"
        "    approved: false\n"
        "experiments:\n"
        "  - id: exp001\n"
        "    tier: sanity\n"
        "    purpose: null\n"
        "    dataset: null\n"
        "    baseline: null\n"
        "    command: null\n"
        "    expected_runtime: null\n"
        "    expected_cost: null\n"
        "    success_criterion: null\n"
        "    required: true\n"
        "approval:\n"
        "  required: true\n"
        "  approved_by_user: false\n"
        "  approved_at: null\n"
    ),
    "03_experiment_plan/datasets.md": (
        "# Datasets\n\n"
        "## Selected Datasets\n\n"
        "## Justification\n\n"
        "## Licenses\n\n"
        "## Preprocessing\n\n"
        "## Splits\n\n"
        "## Risks\n"
    ),
    "03_experiment_plan/baselines.md": (
        "# Baselines\n\n"
        "## Selected Baselines\n\n"
        "## Justification\n\n"
        "## Reproducibility Notes\n\n"
        "## Known Issues\n\n"
        "## Risks\n"
    ),
    "03_experiment_plan/metrics.md": (
        "# Metrics\n\n"
        "## Primary Metrics\n\n"
        "## Secondary Metrics\n\n"
        "## Definition\n\n"
        "## Failure Modes\n\n"
        "## Statistical Tests Planned\n"
    ),
    "03_experiment_plan/cost_risk.md": (
        "# Cost and Risk\n\n"
        "## Compute Estimate\n\n"
        "## API Cost Estimate\n\n"
        "## Wall-clock Estimate\n\n"
        "## Failure Modes\n\n"
        "## Mitigation Plan\n"
    ),
    "03_experiment_plan/approval_request.md": (
        "# Approval Request\n\n"
        "## Summary\n\n"
        "## Requested Approvals\n\n"
        "- [ ] Datasets\n"
        "- [ ] Baselines\n"
        "- [ ] Metrics\n"
        "- [ ] Experiment matrix\n"
        "- [ ] Compute budget\n"
        "- [ ] API budget\n"
        "- [ ] External API usage (if any)\n"
        "- [ ] Sensitive data usage (if any)\n\n"
        "## Why This Plan\n\n"
        "## What Could Go Wrong\n"
    ),
    "04_execution/run_manifest.yaml": "runs: []\n",
    "04_execution/run_log.md": (
        "# Run Log\n\n"
        "| Timestamp | Experiment ID | Command | Status | Notes |\n"
        "|---|---|---|---|---|\n"
    ),
    "04_execution/experiment_status.yaml": "experiments: []\n",
    "04_execution/errors.md": (
        "# Errors\n\n"
        "| Timestamp | Experiment ID | Error | Resolution |\n"
        "|---|---|---|---|\n"
    ),
    "04_execution/change_request.md": (
        "# Change Request\n\n"
        "## Affected Stage\n\n"
        "## Reason\n\n"
        "## Proposed Change\n\n"
        "## Human Approval Needed\n"
    ),
    "05_analysis/results_summary.md": (
        "# Results Summary\n\n"
        "## Headline Numbers\n\n"
        "## Per-experiment Results\n\n"
        "## Comparisons Against Baselines\n\n"
        "## Notable Failures\n\n"
        "## Surprises\n"
    ),
    "05_analysis/finding_cards.yaml": (
        "findings:\n"
        "  - id: finding001\n"
        "    statement: null\n"
        "    evidence:\n"
        "      experiments: []\n"
        "      metrics: []\n"
        "      logs: []\n"
        "    strength: weak\n"
        "    supports_claim: null\n"
        "    limitations: null\n"
        "    can_use_in_abstract: false\n"
    ),
    "05_analysis/claim_support_matrix.md": (
        "# Claim Support Matrix\n\n"
        "| Claim ID | Supporting Findings | Supporting Literature | Strength | Status |\n"
        "|---|---|---|---|---|\n"
    ),
    "05_analysis/statistical_analysis.md": (
        "# Statistical Analysis\n\n"
        "## Tests Performed\n\n"
        "## Significance Levels\n\n"
        "## Effect Sizes\n\n"
        "## Confidence Intervals\n\n"
        "## Caveats\n"
    ),
    "05_analysis/failure_analysis.md": (
        "# Failure Analysis\n\n"
        "## Failed Experiments\n\n"
        "## Failure Categories\n\n"
        "## Lessons Learned\n\n"
        "## Implications For Claims\n"
    ),
    "06_figures/figure_plan.md": (
        "# Figure Plan\n\n"
        "## Figure 1\n\n"
        "### Purpose\n\n"
        "### Source Data\n\n"
        "### Supported Claim\n\n"
        "## Figure 2\n\n"
        "### Purpose\n\n"
        "### Source Data\n\n"
        "### Supported Claim\n\n"
        "## Tables\n"
    ),
    "06_figures/captions.md": (
        "# Figure and Table Captions\n\n"
        "## Figure 1\n\n"
        "## Figure 2\n\n"
        "## Table 1\n\n"
        "## Table 2\n"
    ),
    "07_writing/narrative_options.md": (
        "# Narrative Options\n\n"
        "## Narrative A\n\n"
        "### Frame\n\n"
        "### Strengths\n\n"
        "### Weaknesses\n\n"
        "## Narrative B\n\n"
        "### Frame\n\n"
        "### Strengths\n\n"
        "### Weaknesses\n\n"
        "## Narrative C\n\n"
        "### Frame\n\n"
        "### Strengths\n\n"
        "### Weaknesses\n\n"
        "## AI Recommendation\n"
    ),
    "07_writing/outline.md": (
        "# Paper Outline\n\n"
        "## Abstract\n\n"
        "## 1 Introduction\n\n"
        "## 2 Related Work\n\n"
        "## 3 Method\n\n"
        "## 4 Experiments\n\n"
        "## 5 Results\n\n"
        "## 6 Discussion\n\n"
        "## 7 Limitations\n"
    ),
    "07_writing/claim_ledger.md": (
        "# Claim Ledger\n\n"
        "| Claim ID | Claim Text | Evidence Source | Strength | Paper Location | Approved |\n"
        "|---|---|---|---|---|---|\n"
        "| claim001 | | finding001 / paper001 / human_assumption | weak/moderate/strong | abstract/introduction/results/discussion | no |\n"
    ),
    "07_writing/weak_spots.md": (
        "# Weak Spots\n\n"
        "## Underpowered Claims\n\n"
        "## Missing Baselines\n\n"
        "## Missing Ablations\n\n"
        "## Likely Reviewer Objections\n\n"
        "## Mitigations\n"
    ),
    "paper/main.tex": (
        "\\documentclass{article}\n"
        "\\usepackage[utf8]{inputenc}\n"
        "\\usepackage{graphicx}\n"
        "\\usepackage{hyperref}\n\n"
        "\\title{TBD}\n"
        "\\author{TBD}\n"
        "\\date{}\n\n"
        "\\begin{document}\n"
        "\\maketitle\n\n"
        "\\begin{abstract}\n"
        "TBD\n"
        "\\end{abstract}\n\n"
        "\\input{sections/01_introduction}\n"
        "\\input{sections/02_related_work}\n"
        "\\input{sections/03_method}\n"
        "\\input{sections/04_experiments}\n"
        "\\input{sections/05_results}\n"
        "\\input{sections/06_discussion}\n"
        "\\input{sections/07_limitations}\n\n"
        "\\bibliographystyle{plain}\n"
        "\\bibliography{references}\n\n"
        "\\end{document}\n"
    ),
    "paper/references.bib": "% References will be appended during the literature stage.\n",
    "paper/sections/01_introduction.tex": "\\section{Introduction}\n\nTBD\n",
    "paper/sections/02_related_work.tex": "\\section{Related Work}\n\nTBD\n",
    "paper/sections/03_method.tex": "\\section{Method}\n\nTBD\n",
    "paper/sections/04_experiments.tex": "\\section{Experiments}\n\nTBD\n",
    "paper/sections/05_results.tex": "\\section{Results}\n\nTBD\n",
    "paper/sections/06_discussion.tex": "\\section{Discussion}\n\nTBD\n",
    "paper/sections/07_limitations.tex": "\\section{Limitations}\n\nTBD\n",
    "08_review/review_friendly.md": (
        "# Friendly Simulated Review\n\n"
        "## Strengths\n\n"
        "## Suggested Improvements\n\n"
        "## Overall Recommendation\n"
    ),
    "08_review/review_skeptical.md": (
        "# Skeptical Simulated Review\n\n"
        "## Concerns\n\n"
        "## Required Clarifications\n\n"
        "## Suggested Additional Experiments\n\n"
        "## Overall Recommendation\n"
    ),
    "08_review/review_hostile.md": (
        "# Hostile Simulated Review\n\n"
        "## Strongest Objections\n\n"
        "## Reasons For Rejection\n\n"
        "## Hardest Questions To Answer\n\n"
        "## Overall Recommendation\n"
    ),
    "08_review/meta_review.md": (
        "# Meta Review\n\n"
        "## Synthesis Of Three Reviews\n\n"
        "## Most Critical Issues\n\n"
        "## Recommended Decision\n"
    ),
    "08_review/revision_plan.md": (
        "# Revision Plan\n\n"
        "## Items To Address\n\n"
        "## Items Deferred\n\n"
        "## Section-by-Section Edits\n\n"
        "## Required Followups\n"
    ),
    "08_review/final_checklist.md": (
        "# Final Checklist\n\n"
        "## Compilation\n\n"
        "- [ ] `paper/main.tex` compiles\n\n"
        "## Evidence\n\n"
        "- [ ] All abstract claims are supported\n"
        "- [ ] All main result claims link to findings\n"
        "- [ ] No fabricated citations\n"
        "- [ ] No hidden failed experiments\n\n"
        "## Reproducibility\n\n"
        "- [ ] Experiment commands logged\n"
        "- [ ] Metrics saved\n"
        "- [ ] Seeds recorded\n\n"
        "## Ethics / Disclosure\n\n"
        "- [ ] AI assistance disclosed if needed\n"
        "- [ ] Sensitive data handled properly\n\n"
        "## Human Approval\n\n"
        "- [ ] Final submission approved\n"
    ),
    "08_review/required_followup_experiments.md": (
        "# Required Follow-up Experiments\n\n"
        "## Triggered By Review\n\n"
        "## Description\n\n"
        "## Required For Acceptance?\n\n"
        "## Routing\n\n"
        "If any followup is required, the agent must create a revision request targeting\n"
        "stage 3 (`experiment_plan`) — never silently mutate locked stages.\n"
    ),
}


GITKEEP_DIRS = [
    "experiments",
    "figures",
    "tables",
]
