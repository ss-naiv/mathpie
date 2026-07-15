// MathPie content & logic tests. Run: node tests.js
// Mirrors caltrain-quick's plain-node test style: no framework, exit 1 on failure.

const fs = require('fs');
const path = require('path');

let pass = 0, fail = 0;
function check(name, cond, detail) {
  if (cond) { pass++; }
  else { fail++; console.error(`✗ ${name}${detail ? ' — ' + detail : ''}`); }
}
function load(f) {
  return JSON.parse(fs.readFileSync(path.join(__dirname, 'content', f), 'utf8'));
}

const facts = load('facts.json');
const problems = load('problems.json');
const equations = load('equations.json');
const skills = load('skills.json');
const enc = load('encouragement.json');
const rewards = load('rewards.json');
const elevator = load('elevator.json');
const tricks = load('tricks.json');
const closet = load('closet.json');

// ---------- facts ----------
for (const f of facts.facts) {
  check(`fact ${f.id}: answer in choices`, f.choices.includes(f.answer), f.answer);
  check(`fact ${f.id}: 3 choices`, f.choices.length === 3);
}
const factIds = facts.facts.map(f => f.id);
check('facts: unique ids', new Set(factIds).size === factIds.length);
for (const b of facts.ballparks) {
  check(`ballpark "${b.prompt.slice(0, 30)}": answer in options`, b.options.includes(b.answer));
}

// ---------- problems ----------
const probIds = problems.map(p => p.id);
check('problems: unique ids', new Set(probIds).size === probIds.length);
for (const p of problems) {
  check(`${p.id}: ballpark answer in options`, p.ballpark.options.includes(p.ballpark.answer));
  check(`${p.id}: has hints`, Array.isArray(p.hints) && p.hints.length >= 2);
  check(`${p.id}: has success line`, typeof p.success === 'string' && p.success.length > 0);

  const chips = {};
  for (const g of p.givens) chips[g.id] = g.value;

  p.steps.forEach((s, i) => {
    if (s.choice) {
      check(`${p.id} step ${i}: choice answer in options`, s.choice.options.includes(s.choice.answer));
      return;
    }
    // slot count matches fill list
    const slots = s.template.filter(t => t === '_').length;
    check(`${p.id} step ${i}: slots match fill`, slots === s.fill.length,
      `${slots} slots vs ${s.fill.length} fill`);
    // every fill chip exists at this point
    for (const c of s.fill) {
      check(`${p.id} step ${i}: chip "${c}" exists`, c in chips, `known: ${Object.keys(chips).join(',')}`);
    }
    // arithmetic: calc string evaluates to result
    const val = Function(`"use strict"; return (${s.calc});`)();
    check(`${p.id} step ${i}: calc = result`, Math.abs(val - s.result) < 1e-9,
      `${s.calc} → ${val}, expected ${s.result}`);
    if (s.makes) {
      check(`${p.id} step ${i}: makes.value = result`, s.makes.value === s.result);
      chips[s.makes.id] = s.makes.value;
    }
  });
}

// ---------- equations (Move Gym state graphs) ----------
const eqIds = equations.map(e => e.id);
check('equations: unique ids', new Set(eqIds).size === eqIds.length);
for (const e of equations) {
  check(`${e.id}: start state exists`, e.start in e.states);
  check(`${e.id}: has plan (the strategy WHY)`, typeof e.plan === 'string' && e.plan.length > 20);
  check(`${e.id}: has prove lines`, e.prove && Array.isArray(e.prove.lines) && e.prove.lines.length >= 2);

  let hasWin = false;
  for (const [sid, st] of Object.entries(e.states)) {
    if (st.win) { hasWin = true; continue; }
    check(`${e.id}/${sid}: has moves`, Array.isArray(st.moves) && st.moves.length >= 2);
    const goods = (st.moves || []).filter(m => m.good);
    check(`${e.id}/${sid}: ≥1 good move`, goods.length >= 1);
    for (const m of st.moves || []) {
      if (m.good) {
        check(`${e.id}/${sid}: good move target exists`, m.to in e.states, m.to);
      } else {
        check(`${e.id}/${sid}: detour has eq+note`, !!(m.eq && m.note), m.label);
      }
      check(`${e.id}/${sid}: move has note`, typeof m.note === 'string' && m.note.length > 0, m.label);
    }
  }
  check(`${e.id}: has win state`, hasWin);

  // win reachable from start via good moves (BFS)
  const seen = new Set([e.start]);
  const queue = [e.start];
  let reached = false;
  while (queue.length) {
    const sid = queue.shift();
    const st = e.states[sid];
    if (st.win) { reached = true; break; }
    for (const m of st.moves || []) {
      if (m.good && !seen.has(m.to)) { seen.add(m.to); queue.push(m.to); }
    }
  }
  check(`${e.id}: win reachable via good moves`, reached);
  // no orphan states
  for (const sid of Object.keys(e.states)) {
    const referenced = sid === e.start ||
      Object.values(e.states).some(st => (st.moves || []).some(m => m.good && m.to === sid));
    check(`${e.id}/${sid}: state reachable`, referenced);
  }
}

// ---------- skills / encouragement / rewards ----------
check('skills: warmup+percent+gym unlocked',
  ['warmup', 'percent-of', 'move-gym'].every(id => skills.find(s => s.id === id && s.unlocked)));
const questSkillSet = new Set(skills.flatMap(s => (s.unlocked && s.questSkills) || []));
for (const p of problems) {
  check(`${p.id}: skill "${p.skill}" reachable from a home tile`, questSkillSet.has(p.skill));
}
for (const key of ['welcome', 'success', 'tryAgain', 'gymGood', 'gymSoft', 'proveIt', 'wrap', 'ballparkRight']) {
  check(`encouragement: ${key} non-empty`, Array.isArray(enc[key]) && enc[key].length > 0);
}
check('rewards: coupons exist', rewards.coupons.length >= 3);
check('rewards: chance sane', rewards.schedule.chance > 0 && rewards.schedule.chance <= 0.5);
check('rewards: cosmetics sorted by xp',
  rewards.cosmetics.every((c, i, a) => i === 0 || a[i - 1].xp < c.xp));

// ---------- decimal elevator ----------
// A challenge is valid iff start and target share the same digit core (sliding
// the decimal point can never change the digit sequence, only add/remove zeros).
function core(s) { return s.replace('.', '').replace(/^0+/, '').replace(/0+$/, '') || '0'; }
check('elevator: has intro', typeof elevator.intro === 'string' && elevator.intro.length > 0);
for (const ch of elevator.challenges) {
  check(`elevator ${ch.id}: start/target same digit core`, core(ch.start) === core(ch.target),
    `${ch.start} vs ${ch.target}`);
  check(`elevator ${ch.id}: start ≠ target`, ch.start !== ch.target);
  check(`elevator ${ch.id}: has say`, typeof ch.say === 'string' && ch.say.length > 0);
}
const evIds = elevator.challenges.map(c => c.id);
check('elevator: unique ids', new Set(evIds).size === evIds.length);

// ---------- trick book ----------
for (const t of tricks) {
  check(`trick ${t.id}: try answer in options`, t.try.options.includes(t.try.answer));
  check(`trick ${t.id}: has why`, typeof t.why === 'string' && t.why.length > 20);
  check(`trick ${t.id}: xp is a number`, typeof t.xp === 'number' && t.xp >= 0);
}
check('tricks: at least two free at 0 XP', tricks.filter(t => t.xp === 0).length >= 2);
check('tricks: unique ids', new Set(tricks.map(t => t.id)).size === tricks.length);

// ---------- costume closet ----------
// Mirror of the app's SNAPS table — dial targets must sit on a named fraction snap
// (within the app's 1.5 tolerance) so the fraction costume is visible at the target.
const SNAP_PCTS = [0, 10, 12.5, 20, 25, 30, 33.3, 40, 45, 50, 60, 62.5, 66.7, 70, 75, 80, 90, 100];
check('closet: has intro', typeof closet.intro === 'string' && closet.intro.length > 0);
for (const ch of closet.challenges) {
  check(`closet ${ch.id}: has say`, typeof ch.say === 'string' && ch.say.length > 0);
  if (ch.type === 'dial') {
    check(`closet ${ch.id}: target in range`, ch.target > 0 && ch.target <= 100);
    check(`closet ${ch.id}: target on a fraction snap`,
      SNAP_PCTS.some(p => Math.abs(p - ch.target) <= 1.5), String(ch.target));
  } else {
    check(`closet ${ch.id}: answer in options`, ch.options.includes(ch.answer));
  }
}
check('closet: unique ids', new Set(closet.challenges.map(c => c.id)).size === closet.challenges.length);
check('closet: has both dial and match types',
  closet.challenges.some(c => c.type === 'dial') && closet.challenges.some(c => c.type === 'match'));

// ---------- SRS (Leitner) logic — mirror of the app's implementation ----------
const INTERVALS = [1, 3, 7, 16, 35];
function srsNext(box, correct) { return correct ? Math.min(box + 1, INTERVALS.length - 1) : 0; }
check('srs: promote', srsNext(0, true) === 1 && srsNext(1, true) === 2);
check('srs: cap at top box', srsNext(4, true) === 4);
check('srs: reset on miss', srsNext(3, false) === 0);
check('srs: intervals ascending', INTERVALS.every((v, i, a) => i === 0 || a[i - 1] < v));

// ---------- report ----------
console.log(`\n${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
