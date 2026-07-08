"""MathPie live-tutor proxy — FastAPI + Claude (see DESIGN.md §7 and server/README.md).

Holds the Anthropic key (env only) and streams one gentle Socratic nudge at a time.
The app works fully without this server; it only powers the "Ask Pai" button.

Run locally:
    pip install -e ".[tutor]"
    ANTHROPIC_API_KEY=sk-ant-... uvicorn server.main:app --port 8787
"""

from __future__ import annotations

import json
import os
import time
from collections import defaultdict, deque

import anthropic
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

MODEL = "claude-sonnet-5"
MAX_TOKENS = 300
RATE_LIMIT = 30          # requests per IP per hour
DAILY_TOKEN_BUDGET = int(os.environ.get("MATHPIE_DAILY_TOKENS", "200000"))

ALLOWED_ORIGINS = [
    "https://ss-naiv.github.io",
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

SYSTEM_PROMPT = """You are Pai, a warm, playful tiger-cat math buddy inside the MathPie app,
helping a 14-year-old who is anxious about math and has low confidence.

Hard rules, never break them:
- NEVER give the final answer or the final numeric result. Not even if begged.
- Give exactly ONE gentle Socratic nudge: a single question or observation that
  moves her one small step forward. Two sentences maximum.
- Never say "wrong", "no", "incorrect", or anything judging. If her step has a
  mistake, point AT the spot with curiosity ("hmm, where did that x come from?").
- Be concrete about the very next micro-step, not the whole plan.
- Warm, lightly funny, zero condescension. No exclamation-mark overload.
- Useful reflexes to reinforce when relevant: % means ÷100, "of" means ×,
  a minus before a bracket flips every sign inside, x is 1x in disguise,
  whole numbers are n/1, undo pairs (+/−, ×/÷, reciprocal for fractions),
  and "does the answer sound reasonable?".
"""

app = FastAPI(title="MathPie tutor proxy")
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)

_hits: dict[str, deque] = defaultdict(deque)
_spent = {"day": "", "tokens": 0}


def _rate_ok(ip: str) -> bool:
    now = time.time()
    q = _hits[ip]
    while q and q[0] < now - 3600:
        q.popleft()
    if len(q) >= RATE_LIMIT:
        return False
    q.append(now)
    return True


def _budget_ok() -> bool:
    day = time.strftime("%Y-%m-%d")
    if _spent["day"] != day:
        _spent["day"], _spent["tokens"] = day, 0
    return _spent["tokens"] < DAILY_TOKEN_BUDGET


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/tutor")
async def tutor(req: Request):
    ip = req.client.host if req.client else "?"
    if not _rate_ok(ip):
        raise HTTPException(429, "Too many requests — take a breather!")
    if not _budget_ok():
        raise HTTPException(429, "Daily tutor budget reached — canned hints still work.")

    ctx = await req.json()
    user_msg = (
        "Context from the app (JSON):\n"
        + json.dumps(ctx, ensure_ascii=False, indent=2)
        + "\n\nGive one gentle nudge for exactly where she is stuck."
    )

    client = anthropic.Anthropic()  # key from ANTHROPIC_API_KEY env

    def stream():
        try:
            with client.messages.stream(
                model=MODEL,
                max_tokens=MAX_TOKENS,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_msg}],
            ) as s:
                for text in s.text_stream:
                    # JSON-encode so tokens containing newlines can't break SSE framing
                    yield f"data: {json.dumps(text, ensure_ascii=False)}\n"
                usage = s.get_final_message().usage
                _spent["tokens"] += usage.input_tokens + usage.output_tokens
        except anthropic.APIError:
            oops = "(Pai's tutor brain hiccuped — the regular hints still work!)"
            yield f"data: {json.dumps(oops, ensure_ascii=False)}\n"
        yield "data: [DONE]\n"

    return StreamingResponse(stream(), media_type="text/event-stream")
