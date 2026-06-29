# MathPie

A gentle, Duolingo-style web app for building **math intuition** (not drilling) for a math-anxious
teen. Estimate-before-you-compute, no transcription, no punishment, 10 minutes a day.

> 📐 **Full design & build brief:** see [DESIGN.md](DESIGN.md). Start there.

## Status

Design complete. App not yet built — Phase 1 (Percentages + restaurant scenarios) is next.

## Architecture in one breath

- **The app is static**: a single `index.html` (inline CSS/JS) + `content/*.json`, a PWA
  (`manifest.json` + `sw.js`) installable to an iPad home screen, hosted on GitHub Pages. No backend,
  no runtime build, no API key in the client. Mirrors the sibling `caltrain-quick` app.
- **Build-time tooling is Python** (`tools/`): generates the problem banks and encouragement copy via
  the Anthropic API, baked into `content/*.json`. Run on your laptop; the key never leaves it.

## Dev setup (only needed to (re)generate content)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"      # installs anthropic, python-dotenv, pillow, pytest
cp .env.example .env         # then paste your ANTHROPIC_API_KEY into .env
python tools/gen_problems.py # (re)generate content/problems.json etc.
```

The app needs **none** of the above to run — just open `index.html` (or the GitHub Pages URL).

## Deploy (planned, same as caltrain-quick)

Push to GitHub, enable Pages, serve at `ss-naiv.github.io/mathpie/`. Use relative (`./`) paths so it
works under the subpath. Verify "Add to Home Screen" on iPad.
