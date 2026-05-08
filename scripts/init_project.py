"""Initialise (or seed) a PhD Paper Skill repository.

Creates all stage folders, placeholder files, ``project.yaml``, and
``.gitkeep`` markers. Will not overwrite non-empty files unless
``--force`` is passed.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import REPO_ROOT  # noqa: E402
from _templates import GITKEEP_DIRS, TEMPLATES  # noqa: E402


def write_if_missing(path: Path, content: str, force: bool) -> str:
    """Write `content` to `path` unless the file is already non-empty.

    Returns one of: ``"created"``, ``"overwritten"``, ``"skipped"``.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.stat().st_size > 0 and not force:
        return "skipped"
    action = "overwritten" if path.exists() else "created"
    path.write_text(content, encoding="utf-8")
    return action


def init_project(
    root: Path,
    idea: Optional[str] = None,
    target_venue: Optional[str] = None,
    force: bool = False,
) -> dict:
    summary = {"created": [], "overwritten": [], "skipped": []}

    for rel_path, content in TEMPLATES.items():
        path = root / rel_path
        result = write_if_missing(path, content, force)
        summary[result].append(rel_path)

    for keep_dir in GITKEEP_DIRS:
        keep_path = root / keep_dir / ".gitkeep"
        keep_path.parent.mkdir(parents=True, exist_ok=True)
        if not keep_path.exists():
            keep_path.write_text("", encoding="utf-8")
            summary["created"].append(f"{keep_dir}/.gitkeep")

    if idea:
        idea_path = root / "00_inbox" / "idea.md"
        existing = idea_path.read_text(encoding="utf-8") if idea_path.exists() else ""
        appended = (
            "# Raw Research Idea\n\n"
            "## User Idea\n\n"
            f"{idea.strip()}\n\n"
            "## User Context\n\n"
            "## Known Constraints\n\n"
            "## Open Ambiguities\n"
        )
        if force or not existing.strip() or existing == TEMPLATES["00_inbox/idea.md"]:
            idea_path.write_text(appended, encoding="utf-8")
            summary["overwritten"].append("00_inbox/idea.md")

    if target_venue:
        project_path = root / "project.yaml"
        with project_path.open("r", encoding="utf-8") as handle:
            project = yaml.safe_load(handle) or {}
        project.setdefault("project", {})["target_venue"] = target_venue
        with project_path.open("w", encoding="utf-8") as handle:
            yaml.safe_dump(project, handle, sort_keys=False, allow_unicode=True)
        summary["overwritten"].append("project.yaml (target_venue)")

    return summary


def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Initialise the PhD Paper Skill repo.")
    parser.add_argument("--idea", help="Seed text for 00_inbox/idea.md")
    parser.add_argument("--target-venue", help="Set project.target_venue in project.yaml")
    parser.add_argument(
        "--force", action="store_true", help="Overwrite existing non-empty files."
    )
    parser.add_argument(
        "--root",
        default=str(REPO_ROOT),
        help="Repository root (defaults to the script's parent).",
    )
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    summary = init_project(
        root=Path(args.root).resolve(),
        idea=args.idea,
        target_venue=args.target_venue,
        force=args.force,
    )
    print("init_project complete.")
    for key in ("created", "overwritten", "skipped"):
        files = summary.get(key, [])
        print(f"  {key}: {len(files)} files")
        for name in files:
            print(f"    - {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
