#!/usr/bin/env python3
"""Build-time content generator for MathPie (NOT used at runtime).

Expands a small hand-seeded set of problems into a larger, varied bank and writes it to
content/problems.json (and can refresh content/encouragement.json). Uses the Anthropic API.

Usage:
    cp .env.example .env   # put your ANTHROPIC_API_KEY in .env
    python tools/gen_problems.py

The deployed static app reads only the generated JSON — it never calls the API and never sees a key.
See DESIGN.md §5 (data model) and §7 (LLM usage) for the schema and guardrails.
"""

from __future__ import annotations

import json
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


def main() -> None:
    _ = load_key()
    CONTENT_DIR.mkdir(exist_ok=True)
    # TODO (Phase 1 build): load seed problems, prompt Claude to generate variations matching the
    # schema in DESIGN.md §5, validate, and write content/problems.json. Stub for now so the
    # scaffolding + venv are verifiable before content work begins.
    print(
        "gen_problems.py scaffold ready. "
        f"Model={MODEL}. Content dir={CONTENT_DIR}. "
        "Implement generation in the Phase 1 build (see DESIGN.md)."
    )


if __name__ == "__main__":
    main()
