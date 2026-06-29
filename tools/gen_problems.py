#!/usr/bin/env python3
"""Build-time content generator for MathPie (NOT used at runtime).

A local CLI you run on your laptop to refresh the static content banks. It expands a small
hand-seeded set of problems into a larger, varied bank and writes content/problems.json, and can
rebalance difficulty as the learner masters skills. Uses the Anthropic API.

The deployed static app reads only the generated JSON — it never calls the API and never sees a key.
See DESIGN.md §5 (data model) and §7 (LLM usage) for the schema and guardrails.

Usage:
    cp .env.example .env            # put your ANTHROPIC_API_KEY in .env
    python tools/gen_problems.py expand    --skill percent-of --count 15 --difficulty 2
    python tools/gen_problems.py rebalance --skill percent-of --mastered   # fewer/easier of a mastered skill
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = REPO_ROOT / "content"

# Model id — keep current. See the claude-api skill / DESIGN.md before changing.
MODEL = "claude-opus-4-8"


def load_key() -> str:
    try:
        from dotenv import load_dotenv

        load_dotenv(REPO_ROOT / ".env")
    except ImportError:
        pass
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        sys.exit(
            "ANTHROPIC_API_KEY not set. Copy .env.example to .env and add your key, "
            "or export it in your shell."
        )
    return key


def cmd_expand(args: argparse.Namespace) -> None:
    """'Generate more versions of this problem.' Add `count` new variations for a skill."""
    _ = load_key()
    CONTENT_DIR.mkdir(exist_ok=True)
    # TODO (Phase 1 build): load seed/existing problems for args.skill, prompt Claude for
    # `args.count` fresh variations at `args.difficulty` matching DESIGN.md §5, validate, append to
    # content/problems.json (dedupe by id).
    print(
        f"[expand] skill={args.skill} count={args.count} difficulty={args.difficulty} "
        f"model={MODEL} -> {CONTENT_DIR/'problems.json'} (stub)"
    )


def cmd_rebalance(args: argparse.Namespace) -> None:
    """'She's mastered X, show fewer.' Trim/down-weight a mastered skill, or up-weight a weak one."""
    _ = load_key()
    # TODO (Phase 1+ build): adjust per-skill weighting/quantity in content/problems.json (or a
    # weights file) based on mastery; no destructive deletes by default.
    print(
        f"[rebalance] skill={args.skill} mastered={args.mastered} model={MODEL} (stub)"
    )


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="gen_problems.py", description=__doc__)
    sub = p.add_subparsers(dest="command", required=True)

    e = sub.add_parser("expand", help="generate more variations of a skill's problems")
    e.add_argument("--skill", required=True, help="skill id (see content/skills.json)")
    e.add_argument("--count", type=int, default=10, help="how many new variations")
    e.add_argument("--difficulty", type=int, default=2, choices=range(1, 6), help="1-5")
    e.set_defaults(func=cmd_expand)

    r = sub.add_parser("rebalance", help="adjust how much a skill shows up (mastery-aware)")
    r.add_argument("--skill", required=True, help="skill id")
    r.add_argument("--mastered", action="store_true", help="treat skill as mastered -> show fewer")
    r.set_defaults(func=cmd_rebalance)

    return p


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
