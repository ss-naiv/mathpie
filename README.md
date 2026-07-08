# MathPie

A gentle, Duolingo-style web app for building **math intuition** (not drilling) for a math-anxious
teen. Estimate-before-you-compute, no transcription, no punishment, 10 minutes a day.

> 📐 **Full design & build brief:** see [DESIGN.md](DESIGN.md). Start there.

## Status

**Phase 1 MVP built and live:** https://ss-naiv.github.io/mathpie/

Included: daily session (warm-up → percent quest → Move Gym), SRS fact deck, Ballpark gates,
tap-chips (no transcription), Equation Move Gym with her real homework problems, Prove-It ritual,
streaks/XP, Reward Shelf (parent-editable coupons in `content/rewards.json`), PWA offline support,
and an optional live tutor (see `server/`). Next: Costume Closet, Decimal Elevator (Phase 2).

## Architecture in one breath

- **The app is static**: a single `index.html` (inline CSS/JS) + `content/*.json`, a PWA
  (`manifest.json` + `sw.js`) installable to an iPad home screen, hosted on GitHub Pages. No backend,
  no runtime build, no API key in the client. Mirrors the sibling `caltrain-quick` app.
- **Build-time tooling is Python** (`tools/`): generates the problem banks and encouragement copy via
  the Anthropic API, baked into `content/*.json`. Run on your laptop; the key never leaves it.

## Run locally

The app must be served over http(s) — opening `index.html` as a `file://` URL won't work
(`fetch` of the content JSON and the service worker both require it).

```bash
node tools/serve.js          # serves the app at http://localhost:8080
```

That's it for the app. Tests: `node tests.js`.

### Local tutor (optional — powers the "Ask Pai" button)

Two separate servers: the **app** (:8080, static, no key) and the **tutor proxy** (:8787, holds
your Anthropic key). See `server/README.md` for detail.

```bash
source .venv/bin/activate
pip install -e ".[tutor]"
ANTHROPIC_API_KEY=sk-ant-... uvicorn server.main:app --port 8787
```

Then in the app: **⚙️ Settings → tutor URL → `http://localhost:8787` → Test connection → Save.**
The 🐯 "Ask Pai" button appears in a quest after two hints, or in the Move Gym after a wrong move.
Leave the URL blank and the app is fully playable offline with canned hints.

## Dev setup (only needed to (re)generate content)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"      # installs anthropic, python-dotenv, pillow, pytest
cp .env.example .env         # then paste your ANTHROPIC_API_KEY into .env
python tools/gen_problems.py # (re)generate content/problems.json etc.
```

## Deploy (planned, same as caltrain-quick)

Push to GitHub, enable Pages, serve at `ss-naiv.github.io/mathpie/`. Use relative (`./`) paths so it
works under the subpath. Verify "Add to Home Screen" on iPad.
