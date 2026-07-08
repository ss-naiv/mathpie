# server/ — live tutor proxy (NOW PHASE 1 — decision updated July 2026, see DESIGN.md §7)

This holds the "talk me through it" tutor proxy. Originally deferred to Phase 4; pulled into Phase 1
after real homework showed coached equation-solving needs responses to *her actual wrong step*,
which canned hints can't anticipate. Model: **`claude-sonnet-5`**. The app must stay fully playable
when this proxy is unreachable (offline/off-budget → tutor button grays out, canned hints remain).

## Why a server at all
The static app can't hold the Anthropic key (a public site can't keep a secret). So the live tutor
needs a tiny server-side proxy that holds the key and forwards requests to Claude.

## Plan (decided)
- **Language: Python / FastAPI.** Chosen for token *streaming* — the tutor's reply renders
  word-by-word instead of after a pause, which is the main "feels fast" win. Deps are declared as the
  `tutor` extra in `pyproject.toml`; install when ready with `pip install -e ".[tutor]"`.
- **Text-only.** Voice is handled client-side in the browser (Web Speech API: `SpeechSynthesis` for
  the tiger's voice, `SpeechRecognition` for the kid). So this proxy never touches audio — keeps it
  tiny and cheap.
- **Hosting: scale-to-zero** (Vercel Python function or Fly.io) so it costs nothing idle.
- **One endpoint**, e.g. `POST /tutor`: takes the problem + her stuck-point, returns a single
  Socratic nudge. Streamed (SSE).

## Guardrails (must implement)
- Prompt Claude to **never give the final answer** — one gentle nudge at a time, warm, kid-appropriate.
- **Gate it**: only reachable after ≥2 failed canned hint levels, to cap cost.
- Lock **CORS** to the GitHub Pages origin; add a simple rate limit.
- Key from env only; never returned to the client.

See DESIGN.md §7. iOS Safari caveat: speech *recognition* support is patchier than synthesis — provide
a tap-to-type fallback.
