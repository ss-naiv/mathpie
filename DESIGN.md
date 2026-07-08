# MathPie — Design & Build Spec

> A gentle, Duolingo-style web app for building **math intuition** (not drilling) for a 14-year-old
> entering 8th grade with math anxiety and low confidence. Named for Sagan's "to make an apple pie
> from scratch you must first invent the universe" — the whole point is to STOP re-inventing the
> universe at every problem.
>
> **This file is the brief for a Claude Code build session.** Read it top to bottom, then build the
> MVP (Phase 1). Mirror the conventions of the sibling `caltrain-quick` app.

---

## 0. The learner & the problem (why this exists)

A bright, non-STEM-for-now 14-year-old. Loves Duolingo Chinese (10 min/day, keeps streaks). Hates
Kumon/Mathnasium-style drilling. The goal is **confidence + intuition**, not speed or coverage. She
will likely top out around Algebra 2 / Geometry and that is completely fine. Success = she trusts
her own number sense and stops panicking.

Five diagnosed failure modes (every mechanic below maps to one or more):

| # | Failure mode | Real example |
|---|---|---|
| **P1** | **"Tesla autopilot / apple-pie" problem** — re-bootstraps facts every time instead of having them automatic | Re-derived cm-per-mile by adding 4000+1000+280 ft instead of recalling proportionality |
| **P2** | **Working-memory overload → transcription/entry errors** under anxiety | "10% of $20" → divided 10/100 → wrote "1 cent"; "20% tip on $100" → "2 cents" |
| **P3** | **No reasonableness sense** — order-of-magnitude-wrong answers don't trigger alarm | "2 cents" tip never felt absurd |
| **P4** | **Fractions not seen as ONE concept** with many costumes | fraction / decimal / % / ratio / proportion / odds treated as unrelated |
| **P5** | **Mental block: letters aren't numbers** | couldn't write "starts at -1, +4 each term" as a rule; couldn't solve `x + 5y = 20` for `y` |
| **P6** | **Inverse operations not automatic** — doesn't see ÷ as the undo of ×, +/− as complements | didn't realize dividing both sides by 11/3 (or ×3 then ÷11) frees `x` |
| **P7** | **Strategy and mechanics entangled** — knows the goal ("get x alone") but each move's arithmetic derails the plan | a full solve-for-x needed coaching at *every* step; page covered in erasures |
| **P8** | **No verify-by-substitution reflex** — checking the answer isn't part of "done" | never thought to plug x=5 back into the original equation |
| **P9** | **Brackets & sign flips** — a minus in front of a bracket doesn't flip the signs inside; nested brackets have no inside-out order; combining terms across zero (`x − 3x = −2x`) fails | `Simplify 3 + (2x − (x + 3(−x+2))) + 3` stumped her entirely |

P9 drills live in the Move Gym (§4.8): "open the minus-bracket — flip every sign" is a move card,
nested brackets teach the inside-out ("untie the deepest knot first") order, and `x − 3x = −2x` is
both an SRS fact and a combine-terms move. Note `x = 1x` (a costume, §4.1) is the same root gap.

Also missing: **rules of thumb** ("% means ÷100", "of means ×", "shift decimal left = ÷10"). The dad
already taught "X% of Y = (X÷100) × Y" verbally — the app's job is to make it *muscle memory*.

### Case study: the canonical solve-for-x (from real summer homework, July 2026)

She solved `(4/3)(2x − 7) = −x + 9` → `x = 5` correctly, but needed coaching at every step.
Preserve this as the **reference problem** for the Equation Move Gym (§4.8) — every observed stumble
becomes a drill:

1. Didn't see `−x + 9` can be read as `9 − x` (expression flexibility).
2. Distributing `4/3` was hard: didn't treat `2x` as one number; unsure if `x` lands in numerator or
   denominator (`(4/3)·2x = 8x/3`); wrote `(4/3)·(−7)` as `−28x/3` — a spurious `x`. Scaffold: show
   whole numbers as `n/1` (7 = 7/1) so numerator×numerator / denominator×denominator is mechanical.
3. Moving `x` across `=` by adding `x` to both sides needed prompting (legal-moves concept).
4. Combining `8x/3 + x` requires the costume change `x = 3x/3` — **her fraction gap directly blocks
   algebra here**. Same for `9 = 27/3` on the RHS (she went decimal, `9 + 9.3`, instead).
5. Didn't recognize the last step is one undo: `(11/3)x = 55/3` → multiply both sides by the
   reciprocal `3/11` (P6).
6. Entering `(9 + 28/3) × 3/11` into a calculator in one go overloaded her (P2). Her decimal path got
   `4.99…` — a teachable moment: decimals wobble, fractions land exactly on 5.
7. No "plug it back in" check (P8) — and the check here is satisfying: both sides equal 4.

---

## 1. Design principles (non-negotiable — these ARE the product)

1. **Estimate before you compute, always.** Every numeric problem opens with a *ballpark gate*: pick
   a range / order of magnitude BEFORE the exact answer. This is the direct cure for P3 and forces
   reasonableness to become a reflex. (See "Ballpark Booth".)
2. **Never make her transcribe or retype a number.** Given values are extracted into tappable
   **chips**. She builds solutions by tapping/dragging chips, not typing. Kills the P2 error class at
   the source — you can't fat-finger a number you never typed.
3. **One operation per visible step.** Multi-step problems are decomposed into a **Step Ladder** with
   the running result shown, so she never "loses the thread" (the map-problem failure).
4. **One concept, many costumes.** Fractions/decimals/%/ratios are taught as the *same thing wearing
   different outfits*, with live morphing visuals.
5. **No punishment, ever.** No red X, no "Wrong", no timers (timers = anxiety). Wrong attempts get
   "let's look again" + an escalating hint ladder. The answer is always reachable. **Streak rewards
   showing up, not accuracy** (Duolingo model: you finish the lesson, you keep the streak).
6. **Warm + funny.** A mascot reacts kindly. Encouragement copy in a Calvin-&-Hobbes-ish spirit
   ("Let's call this variable y, as in *why* do we care"). ⚠️ Use ORIGINAL characters/voice inspired
   by C&H — do **not** ship copyrighted strips or the actual characters (repo is public-ish).
7. **10-minute cap.** After the daily quest, it says "come back tomorrow" to protect the habit and
   avoid burnout. Short and finishable beats long and dreaded.
8. **Spaced repetition for facts she keeps re-bootstrapping** (5280 ft/mi, ×10 = shift decimal, "%
   means ÷100", "of means ×"). A small SRS deck surfaces these in warm-ups (cure for P1).
9. Cuteness/kawai factor, customizability (icons, skins, mascots), awards redeemable for quirky things ("hug from Dad", "one trip to Miniso") at somewhat random times or after accomplishments would help with retention
10. Extensibility hooks built-in as mastery is built or class content changes (Algebra, Geometry etc.) with the emphasis on building intuition and comfort with real world applications. 

---

## 2. Tech stack & deployment (mirror caltrain-quick as needed/appropriate)

- **Single `index.html`** with inline CSS + JS. No framework, no build step.
- **Static content** in JSON files (`content/*.json`) loaded at runtime — like `schedule-data.min.json`.
- **PWA**: `manifest.json` + `sw.js` (service worker, network-first w/ cache fallback) so she can
  "Add to Home Screen" on iPad and it works offline. Copy caltrain-quick's `sw.js` almost verbatim;
  update `CACHE_NAME` and the `ASSETS` list.
- **Progress** persisted in `localStorage` (streak, XP, skill mastery, SRS queue, settings). No
  backend, no login, no account.
- **Hosting**: GitHub Pages at `ss-naiv.github.io/mathpie/`. Same flow as caltrain-quick
  (main branch + gh-pages, or Pages-from-main). Use **relative paths** (`./`) everywhere so it works
  under the `/mathpie/` subpath.
- **Icons**: reuse caltrain-quick's `generate-icons.js` approach (canvas) or a simple SVG → PNG.
- **No secrets in the repo or client.** MVP ships with zero API key. (Tutor module, Phase 4, uses a
  serverless proxy — see §7.)

### File layout
```
mathpie/
  index.html            # app shell + all CSS/JS inline (like caltrain-quick)
  manifest.json
  sw.js
  icon.svg  icon-192.png  icon-512.png
  content/
    skills.json         # skill tree / progression
    facts.json          # SRS deck (the "apple-pie" facts she re-bootstraps)
    problems.json       # problem bank (data-driven; see §5 schema)
    encouragement.json  # mascot lines, success/“let’s look again” copy
  tools/
    gen_problems.py     # BUILD-TIME ONLY (Python CLI): expand/rebalance problem banks via Anthropic API
  server/               # PHASE 1 (updated): Python/FastAPI live-tutor proxy (holds key; text-only; streams)
    README.md           # plan + guardrails; deps are the `tutor` extra in pyproject.toml
  content/rewards.json  # parent-editable coupon list + cosmetic unlocks (Reward Shelf, §4.9)
  tests.js              # logic tests (mirror caltrain-quick/tests.js style)
  README.md
  CLAUDE.md             # build/deploy notes for future sessions
```

---

## 3. The daily loop (≈10 min)

1. **Warm-up (2–3 min):** 3–5 quick cards from the **SRS fact deck** + a couple of **Ballpark**
   taps. Fast, high-success, builds momentum.
2. **Quest (5–6 min):** ONE themed real-world scenario (restaurant / recipe / map / shopping) played
   through the Ballpark gate → Step Ladder. This is the meat.
3. **Wrap (1 min):** streak +1, XP, mascot celebration, "see you tomorrow". Update SRS queue with any
   facts missed today.

XP + streak + a small **skill tree** that lights up as mastery grows. Optional confetti. No
leaderboards (solo, no social pressure).

---

## 4. Core mechanics (each maps to a failure mode)

### 4.1 Costume Closet — fractions are ONE thing (P4)
A value shown morphing across forms with a live visual (a pie/bar filling):
`1/2 ⇄ 0.5 ⇄ 50% ⇄ 1 : 2 ⇄ "1 out of 2"`.
- **Slider mode:** drag a slider; the pie fills and all representations update live together.
- **Match mode:** sort/match cards that are the *same value in different costumes*.
- Teaches the gut-level "these are all the same partial-quantity idea."
- **Algebra costumes (feeds §4.8):** the same morphing idea applied to expressions — `x ⇄ 1x ⇄ 3x/3`,
  `9 ⇄ 27/3`, `7 ⇄ 7/1`, `−x + 9 ⇄ 9 − x`. Same value, different outfit. This is precisely the gap
  that blocked combining `8x/3 + x` in the case study.

### 4.2 Ballpark Booth — reasonableness gate (P3) ⭐ the keystone mechanic
Before computing, she picks an order of magnitude:
> "A 20% tip on a \$100 meal is closest to:  **2¢ / \$2 / \$20 / \$200**?"
Choosing wildly wrong gets a gentle, concrete nudge: *"Hmm — would you really hand the waiter two
pennies?"* Every numeric quest passes through this gate first. Over time it becomes reflex.

### 4.3 Decimal Elevator — place value & ×/÷10 rules of thumb (P1, P2)
A number rides an elevator; pressing **×10 / ÷10** slides the digits past the decimal point visually.
Builds "10% = move one step left", "% = ÷100 = move two steps". Cures the 10/100 = "1 cent" slip by
making decimal movement physical and memorable.

### 4.4 Sentence Decoder — "X% of Y" contains its own recipe (P2)
Tap-to-translate: the sentence "**30% of 80**" is rebuilt word-by-word into math —
tap `%` → it becomes `÷ 100`, tap `of` → it becomes `×` — lighting up `30 ÷ 100 × 80`. Gamifies the
exact rule the dad already taught. Includes the pro tip: "tax is 10% → just move the decimal one
step; double it for a 20% tip."

### 4.5 Pinned Givens + Chips — no transcription (P2)
Word problems auto-extract numbers into labeled, tappable chips that stay pinned on screen:
`[1 cm = 2000 ft]  [4.8 miles]  [5280 ft/mile]`. She *builds* the solution from chips; she never
retypes a value, so she can't enter it wrong. The map problem becomes a clean chain:
`miles → feet (× 5280) → cm (÷ 2000)`.

### 4.6 Step Ladder — structured multi-step, running result shown (P1, P2)
Decomposes a problem into rungs, one operation each, each rung showing the cumulative result so the
goal stays in view. Example (the map problem):
```
Rung 1:  4.8 miles × 5280 ft/mile      = 25,344 ft
Rung 2:  25,344 ft ÷ 2000 ft/cm        = 12.672 cm   ✅ does ~13 cm sound right on a map? yes.
```
Contrast with what went wrong before (adding 4000+1000+280 and dropping the ×4.8). Optional
"recognize the shortcut" badge when she spots proportionality.

### 4.7 "Y Do We Care" Island — letters are numbers (P5)
Calvin-flavored algebra zone. Letters shown as **labeled boxes that hold an unknown number** — "the
box could be any number, but it's the *same* number everywhere this letter appears." Avoids the
literal "replace the letter" trap.
- **Sequence builder:** "starts at −1, add 4 each term" → stack tiles to discover the rule
  `term(n) = −1 + 4 × (n − 1)`. Build it visually before writing it.
- **Seesaw solver:** for `x + 5y = 20`, "express y in terms of x" via a balance scale — move terms
  across the `=` and the operation flips. End state keeps the variable in the answer
  (`y = (20 − x) / 5`), reinforcing that the answer is an *expression*, not a single number.

### 4.8 Equation Move Gym — separate strategy from mechanics (P6, P7) ⭐ new keystone
The case-study insight: she has the *goal* (get x alone) but drowns because every move requires
arithmetic she doesn't trust, so the plan and the mechanics fail together. Train them separately,
like chess puzzles vs. full games:

- **Mode A — "Call the move":** an equation is shown; she picks the next move from 3–4 cards
  ("distribute the 4/3", "add x to both sides", "multiply both sides by 3/11"…). The app executes
  the arithmetic *perfectly* and shows the new equation. Zero arithmetic anxiety; pure game plan.
  Wrong move choices aren't punished — the app applies them and lets her see the equation get
  *messier*, then offers an undo ("hmm, did that get us closer to x alone?").
- **Mode B — "Make the move":** the app calls the move; she executes just that ONE step with chips
  (e.g., distribute `4/3` across `(2x − 7)` with the 7 auto-shown as `7/1`). One-step arithmetic,
  bounded working memory.
- **Mode C — "Full solve":** both together, with the hint ladder + live tutor (§7) as backup.
- **Move cards teach undo pairs (P6):** every card shows its inverse on the flip side (+5 ↔ −5,
  ×3 ↔ ÷3, ×(11/3) ↔ ×(3/11) *reciprocal*). "To free x, undo what's wrapped around it, in reverse
  order" — the wrapping-paper metaphor.
- **"Prove it!" ritual (P8):** every solved equation ends by plugging the answer back in — and the
  substitution check IS the win animation (both sides light up equal → confetti). Checking becomes
  the reward, not homework. Also closes the loop on reasonableness (Ballpark gate said x ≈ 5-ish;
  Prove-it confirms exactly 5).
- Calculator discipline falls out for free: one op per rung means she never types a compound
  expression like `(9 + 28/3) × 3/11` — the failure in case-study item 6.

### 4.9 Reward Shelf — kawaii + real-world coupons (retention; design principle 9)
Cosmetic unlocks (mascot accessories, skins, app icons) plus **parent-configurable real-world
coupons** ("hug from Dad", "one Miniso trip", "you pick dinner") stored in `content/rewards.json`.
Award on a *variable-ratio* schedule — sometimes after a milestone, sometimes at random — which is
the strongest-known schedule for habit retention. Redeemed coupons get a little ticket animation.

---

### Content sources (updated July 2026)

The content banks are seeded from her actual **Rising 8th Summer Work packet** (Review Pages 1–6 +
Practice Problems), covering: unit conversion chains, the percent triangle (find part / find percent
/ find whole), percent of change, markup/discount/tax, distance-rate-time, proportional
relationships & unit rates, solving linear equations, express-y-in-terms-of-x, brackets & sign
flips. Several problems are lifted verbatim (map-scale, squirrel reaction-distance, $8.25 sandwich,
(4/3)(2x−7)=−x+9, the nested-bracket simplify, 4x+5y=20). **Note:** Practice Problems pages 14,
25–39, 53–56 are image-only scans, not yet mined (needs poppler/pdftoppm to render). Concepts
already "completed" in the packet stay in rotation — the SRS deck exists precisely because
completion ≠ retention (the "Y% of Z = Z×Y÷100" recipe appears in multiple costumes for this
reason).

## 5. Content data model (data-driven; Claude generates the bank)

Everything the kid sees is data, so the bank can grow without code changes. Suggested `problems.json`
item schema:

```jsonc
{
  "id": "tip-100-20",
  "skill": "percent-of",          // FK into skills.json
  "theme": "restaurant",          // restaurant | recipe | map | shopping | abstract
  "difficulty": 2,                 // 1–5
  "scenario": "Dinner came to $100. You want to leave a 20% tip. Is $115 cash enough?",
  "givens": [                      // become tappable chips (mechanic 4.5)
    { "label": "bill", "value": 100, "unit": "$" },
    { "label": "tip rate", "value": 20, "unit": "%" },
    { "label": "cash", "value": 115, "unit": "$" }
  ],
  "ballpark": {                    // mechanic 4.2 — gate shown first
    "prompt": "About how much is a 20% tip on $100?",
    "options": ["2¢", "$2", "$20", "$200"],
    "answer": "$20",
    "nudge": "Would you hand the waiter two pennies on a $100 dinner?"
  },
  "steps": [                       // mechanic 4.6 — one op per rung
    { "expr": "20 ÷ 100 × 100", "result": 20, "say": "20% of $100 is $20" },
    { "expr": "100 + 20",        "result": 120, "say": "bill + tip = $120" },
    { "compare": [120, 115], "op": ">", "result": false, "say": "$120 > $115 → not quite enough" }
  ],
  "hints": [                       // escalating ladder; never reveals all at once
    "What does '20%' turn into? (% means ÷100)",
    "20 ÷ 100 = 0.20. Now 'of $100' means × 100.",
    "Tip is $20, so the total is $100 + $20 = $120."
  ],
  "success": "Nice — you caught that $115 wouldn’t cover it. That’s real-world math."
}
```

`facts.json` (SRS deck, mechanic for P1):
```jsonc
{ "id": "ft-per-mile", "front": "How many feet in a mile?", "back": "5,280",
  "tag": "units", "interval": 1 }
{ "id": "pct-means", "front": "What does '%' mean as an operation?", "back": "÷ 100",
  "tag": "rules-of-thumb" }
```

`skills.json` defines the tree/order (see §6). `encouragement.json` holds mascot/success/"look again"
lines (this is the file most worth LLM-generating for variety & voice).

**SRS algorithm:** keep it dead simple — a Leitner box / SM-2-lite. Missed → interval resets to 1
day; correct → interval grows (1→3→7→16…). Persist per-fact interval + due date in localStorage.

---

## 6. Skill progression (the tree)

Start with **fractions in all costumes**, then percentages (where her real-world pain is), then
ratio/proportion, then the on-ramp to algebra. Order:

1. **Fraction Costumes** — fraction ⇄ decimal ⇄ % ⇄ "out of" (mechanic 4.1)
2. **Decimal Moves** — ×/÷ 10, 100; rounding; place value (4.3)
3. **Percentages** — "% of" decoder, tax/tip, discounts, "is it enough?" (4.2, 4.4) ← real-world core
4. **Ratio & Proportion** — recipes (scale a recipe up/down), maps & scale (the cm/ft problem)
5. **Pre-Algebra on-ramp** — "Y Do We Care" sequences & patterns (4.7)
6. **Algebra basics** — expressions, "express y in terms of x", the seesaw solver (4.7)
7. **Equation Move Gym** (4.8) — solve-for-x with linear equations incl. fractions

**Exception to the ordering:** the Move Gym's Mode A ("call the move") requires NO arithmetic, so a
starter version ships in Phase 1 even though full equation-solving is late-tree — because solve-for-x
is her *live* 8th-grade homework pain right now. Modes B/C unlock as the fraction skills build,
which makes the dependency visible and motivating: "finish Fraction Costumes to unlock Make-the-Move."

Each skill unlocks the next but earlier ones stay open for revisiting. Themes (restaurant, recipe,
map, shopping) cut across skills so the same idea shows up in different real-world clothes.

---

## 7. LLM usage — exactly where and how

**DECISION UPDATE (July 2026, after the case-study homework):** the live tutor moves from Phase 4
to **Phase 1**. Coached equation-solving needs responses to *her actual wrong step*, which canned
hint ladders can't fully anticipate. **Model: `claude-sonnet-5`** (right cost/capability point for
Socratic nudging). The deterministic core (move legality, arithmetic, SRS, rewards) stays static and
offline-capable — the tutor degrades gracefully when offline or over budget: canned hints still work,
the "ask the tiger" button just grays out.

Runtime tutor roles, in order of value:
1. **Diagnose the actual mistake:** she (or the app) shows what she did — e.g. wrote `−28x/3` for
   `(4/3)(−7)` — and the tutor names the misconception gently ("where did that x come from? Only the
   7 is being multiplied…").
2. **Fresh Socratic nudge** when the 3-level canned ladder is exhausted. Never the final answer.
3. **Move commentary in the Gym:** one warm sentence on *why* the move she picked helped or didn't.

- **Build-time generation (`tools/gen_problems.py`, Python, runs on the dad's laptop):** uses the
  Anthropic Python SDK (key from `.env`, never committed) to expand a small seed set into a large
  `problems.json` + varied `encouragement.json`. Run it, commit the JSON, done. Model: a current
  Claude model; cheap, one-time per content refresh. This is where the API key delivers most of its
  value. (Toolchain: venv + `pyproject.toml`; see README.)
- **Live tutor (now Phase 1, "talk me through it" button):** because a public static site can't hold
  a secret key, this requires a **tiny proxy** that holds the key and forwards requests. **Decided:
  Python / FastAPI** (chosen for token streaming — replies render word-by-word, the main "feels
  fast" win), hosted scale-to-zero (Vercel Python function or Fly.io). Model: `claude-sonnet-5`.
  **Voice is client-side** (browser Web Speech API: `SpeechSynthesis` + `SpeechRecognition`), so the
  proxy stays text-only and tiny — voice itself can wait for a later phase; the proxy design doesn't
  change either way. Prompt it to *never give the final answer* — one nudge at a time, warm,
  kid-appropriate. Gate it (only after ≥2 failed hint levels, except in Move Gym where diagnosis is
  first-class) to control cost; lock CORS to the Pages origin; rate-limit; set a daily token budget.
  Deps live as the `tutor` extra in `pyproject.toml` (`pip install -e ".[tutor]"`). See
  `server/README.md`. iOS Safari caveat: speech *recognition* is patchier than synthesis — provide a
  tap-to-type fallback.

---

## 8. Build phases (revised July 2026 — tutor & Move Gym pulled forward)

- **Phase 1 — MVP (build this first):** app shell + PWA + localStorage progress/streak; Ballpark
  Booth + Step Ladder + Pinned Chips; the **Percentages** skill with ~20 restaurant/shopping problems
  (hand-seeded, then expanded by `tools/gen_problems.py`); **Equation Move Gym Mode A** ("call the
  move" — no arithmetic required) seeded with the case-study equation and ~10 linear equations;
  **live-tutor proxy** (FastAPI + `claude-sonnet-5`, streaming, guardrails per §7); SRS warm-up with
  ~15 facts; mascot + warm copy; Reward Shelf v1 (cosmetics + parent-editable coupon list); deploy
  to GitHub Pages; "Add to Home Screen" verified on iPad.
- **Phase 2:** Costume Closet (incl. algebra costumes) + Decimal Elevator + Sentence Decoder; full
  Fractions & Decimals skills; Move Gym **Mode B** (make-the-move) gated on fraction progress.
- **Phase 3:** Ratio/Proportion (recipes + maps — includes the cm/ft problem); skill-tree UI; Move
  Gym **Mode C** (full solve + Prove-It ritual); parent mini-dashboard (what facts keep coming back,
  accuracy trend — localStorage only).
- **Phase 4:** "Y Do We Care" algebra island (sequences + seesaw solver); voice mode for the tutor
  (client-side Web Speech API); extensibility packs as class content evolves (Geometry, Algebra 2).

---

## 9. Acceptance checks (what "done" looks like for Phase 1)

- Loads offline on iPad after first visit; installable to home screen with icon + name.
- A full daily session is completable in ≤10 min and ends with a streak bump.
- No screen ever shows "Wrong" or a red X; every problem is eventually solvable via hints.
- The "$100 dinner, 20% tip, is $115 enough?" problem plays correctly: ballpark gate → chips → step
  ladder → "$120 > $115, not enough", with a reasonableness nudge if "2¢" is picked.
- The cm/ft map problem (Phase 3) decomposes into the two-rung ladder with a reasonableness check.
- Move Gym Mode A plays the case-study equation `(4/3)(2x−7) = −x+9` end-to-end: she can reach
  `x = 5` purely by picking moves, a wrong move shows the messier equation + undo, and the session
  ends with the Prove-It substitution (both sides = 4).
- Tutor: replies stream word-by-word; never contains the final numeric answer; app remains fully
  playable with the proxy unreachable (button grays out, canned hints still work).
- No API key in the repo or client bundle; `gen_problems.py` reads it from `.env`, the proxy from
  its hosting env.
- `tests.js` covers the percent/step-ladder/SRS logic and passes.

---

## 10. Open choices for the dad (sensible defaults already chosen)

- **App/mascot name:** placeholder "MathPie" + an original tiger-ish sidekick (let the kid name it).
- **Static-only vs. live tutor:** default static-only for MVP; add proxy later only if needed.
- **Visual theme:** warm, low-stimulation, dyslexia-friendly font, generous spacing, dark-mode option.
