# server/ — live tutor proxy (Phase 4, not yet built)

Empty on purpose. This holds the optional "talk me through it" tutor proxy. The MVP and all earlier
phases ship **without** it — the app stays static, offline, and key-free until this exists.

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
