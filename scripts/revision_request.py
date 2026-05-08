"""Create a revision request to amend a locked earlier stage.

Revision requests are the only sanctioned way to mutate a locked stage. The
script creates a structured Markdown document under ``08_review/`` (or the
current stage directory) that the human must approve before any change is
made. This script does *not* unlock the target stage — that remains a
deliberate human decision.
"""
from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _common import REPO_ROOT, STAGE_NAMES, load_project, stage_dir  # noqa: E402


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def revision_request_path(root: Path, from_stage: int, target_stage: int) -> Path:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    fname = f"revision_request_{timestamp}_from{from_stage:02d}_to{target_stage:02d}.md"
    return stage_dir(from_stage, root) / fname


def write_revision_request(
    root: Path,
    from_stage: int,
    target_stage: int,
    reason: str,
    files: Optional[list] = None,
    proposed_change: Optional[str] = None,
) -> Path:
    if from_stage <= target_stage:
        raise ValueError(
            "revision requests must point from a later stage back to an earlier one"
        )
    if target_stage < 0 or from_stage >= len(STAGE_NAMES):
        raise ValueError("stage indices out of range")

    out = revision_request_path(root, from_stage, target_stage)
    out.parent.mkdir(parents=True, exist_ok=True)

    files = files or []
    files_block = "\n".join(f"- {f}" for f in files) if files else "(none specified)"
    proposed_block = proposed_change.strip() if proposed_change else "TBD"

    body = (
        "# Revision Request\n\n"
        f"- Created: {now_iso()}\n"
        f"- From stage: {from_stage:02d} ({STAGE_NAMES[from_stage]})\n"
        f"- Target stage: {target_stage:02d} ({STAGE_NAMES[target_stage]})\n\n"
        "## Target Stage\n\n"
        f"{target_stage:02d} ({STAGE_NAMES[target_stage]})\n\n"
        "## Reason\n\n"
        f"{reason.strip()}\n\n"
        "## Files Requested for Change\n\n"
        f"{files_block}\n\n"
        "## Why Current Locked Output Is Insufficient\n\n"
        "TBD\n\n"
        "## Proposed Change\n\n"
        f"{proposed_block}\n\n"
        "## Human Approval Needed\n\n"
        "- [ ] Approved by user\n"
        "- [ ] Target stage unlocked (manual)\n"
        "- [ ] Edits made\n"
        "- [ ] Target stage re-validated and re-locked\n"
    )
    out.write_text(body, encoding="utf-8")
    return out


def parse_args(argv=None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a revision request.")
    parser.add_argument("--from-stage", type=int, required=True)
    parser.add_argument("--target-stage", type=int, required=True)
    parser.add_argument("--reason", required=True)
    parser.add_argument("--files", nargs="*")
    parser.add_argument("--proposed-change")
    parser.add_argument("--root", default=str(REPO_ROOT))
    return parser.parse_args(argv)


def main(argv=None) -> int:
    args = parse_args(argv)
    # Touching project.yaml here only as a sanity check that we're in a real
    # repo — we never modify the locked stage on behalf of the user.
    load_project(Path(args.root).resolve())
    out = write_revision_request(
        Path(args.root).resolve(),
        from_stage=args.from_stage,
        target_stage=args.target_stage,
        reason=args.reason,
        files=args.files,
        proposed_change=args.proposed_change,
    )
    print(f"revision request created: {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
