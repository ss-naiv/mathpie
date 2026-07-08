# server/ — live tutor proxy (built; deploy when ready)

FastAPI proxy powering the "Ask Pai" button. Model: **`claude-sonnet-5`**. The app is fully playable
without it (offline/off-budget → canned hints remain), and the button only appears once a tutor URL
is saved in the app's Settings (⚙️).

## Run locally
```bash
pip install -e ".[tutor]"        # from the repo root
ANTHROPIC_API_KEY=sk-ant-... uvicorn server.main:app --port 8787
# then in the app: Settings ⚙️ → tutor URL → http://localhost:8787 → Test connection
```

## Deploy (pick one)
- **Fly.io:** `fly launch` in this dir (uses requirements.txt), set `fly secrets set ANTHROPIC_API_KEY=...`
- **Vercel:** expose `server.main:app` via a Python serverless function; set the key in project env vars.

After deploying, paste the URL into the app's Settings on the iPad. Endpoints: `GET /health`,
`POST /tutor` (SSE stream of JSON-encoded text chunks, `data: [DONE]` terminator).

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
