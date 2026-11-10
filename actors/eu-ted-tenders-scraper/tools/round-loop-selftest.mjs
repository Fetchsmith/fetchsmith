// Self-test for fetchPage()'s round loop (cycle 2974, mirroring the trademark-search-scraper
// round loop added in cycle 2968 -- same defect shape, found by c2969's fleet audit: a bounded
// retry ladder (HTTP_RETRY_DELAYS_MS, 4 steps) gives up and reports a terminal HTTP error even
// when the run's own time budget still has plenty of room left, pushing buyers toward a FAILED
// run and a "re-run in a few minutes" message the run itself had time to act on.
//
// This is a MIRROR, not the real function: if the round loop in src/main.js changes, change this
// too. What it pins down is the same four properties cycle 2968's selftest pinned down, adapted
// to this Actor's simpler (no proxy-rotation) ladder.
//   node tools/round-loop-selftest.mjs

const HTTP_RETRY_DELAYS_MS = [2000, 5000, 10000, 20000];
const ROUND_PAUSE_MS = [15000, 30000, 45000];
const MAX_ROUNDS = 10;
const TIME_BUDGET_MARGIN_MS = 45000;
const REQUEST_MS = 1000; // a TED request itself is fast; the ladder's cost is almost all sleep

// `outcomes` is consulted per fetchPageOnce() call: 'fail' = TRANSIENT_STATUS, 'ok' = HTTP 200.
// Every attempt burns REQUEST_MS on the fake clock; waits/pauses burn their full (capped) length.
function simulate({ budgetMs, outcomes }) {
  let now = 0;
  const remaining = () => (budgetMs === null ? Infinity : budgetMs - now - TIME_BUDGET_MARGIN_MS);
  const timeBudgetOk = () => remaining() > 0;
  const log = [];
  let attempts = 0;

  const once = () => {
    now += REQUEST_MS;
    attempts += 1;
    return outcomes[attempts - 1] ?? 'fail';
  };

  for (let round = 0; round < MAX_ROUNDS; round += 1) {
    let outcome = once();
    log.push(`r${round}: attempt 0 -> ${outcome}`);
    if (outcome === 'ok') return { result: 'ok', attempts, rounds: round + 1, now, log };
    for (const fallbackMs of HTTP_RETRY_DELAYS_MS) {
      if (!timeBudgetOk()) return { result: 'timeBudgetHit', attempts, rounds: round + 1, now, log };
      const waitMs = Math.max(Math.min(fallbackMs, remaining()), 0);
      now += waitMs;
      log.push(`r${round}: wait ${waitMs}ms`);
      if (!timeBudgetOk()) return { result: 'timeBudgetHit', attempts, rounds: round + 1, now, log };
      outcome = once();
      log.push(`r${round}: ladder attempt -> ${outcome}`);
      if (outcome === 'ok') return { result: 'ok', attempts, rounds: round + 1, now, log };
    }
    // ladder exhausted, still transient
    if (!timeBudgetOk()) return { result: 'timeBudgetHit', attempts, rounds: round + 1, now, log };
    const pauseMs = Math.max(Math.min(ROUND_PAUSE_MS[Math.min(round, ROUND_PAUSE_MS.length - 1)], remaining()), 0);
    now += pauseMs;
    log.push(`pause ${pauseMs}ms -> round ${round + 1}`);
    if (!timeBudgetOk()) return { result: 'timeBudgetHit', attempts, rounds: round + 1, now, log };
  }
  return { result: 'failed', attempts, rounds: MAX_ROUNDS, now, log };
}

let bad = 0;
const check = (name, cond, detail) => {
  if (cond) { console.log(`ok   ${name}`); } else { bad += 1; console.log(`FAIL ${name} -- ${detail}`); }
};

// 1. The regression this fix is for: the whole ladder fails, but a typical run budget (e.g. 300s)
//    has room for more. Before the fix this was 5 attempts / 1 round / terminal error at ~37s.
const a = simulate({ budgetMs: 300000, outcomes: [] });
check('exhausted ladder keeps retrying inside a 300s budget', a.rounds > 1 && a.attempts > HTTP_RETRY_DELAYS_MS.length + 1,
  `got ${a.attempts} attempts in ${a.rounds} round(s)`);

// 2. It must never run past the margin reserve -- TIMED-OUT (killed, no status message, no
//    partial-results save) is strictly worse than a reported terminal HTTP error.
check('never spends into the time budget margin', a.now <= 300000 - TIME_BUDGET_MARGIN_MS,
  `stopped at ${a.now}ms of a ${300000 - TIME_BUDGET_MARGIN_MS}ms spendable budget`);

// 3. A transient spell that clears on round 2 must return the 200, not a terminal error -- the
//    whole point: the run does the "re-run in a few minutes" the old error text asked the buyer for.
const b = simulate({ budgetMs: 300000, outcomes: ['fail', 'fail', 'fail', 'fail', 'fail', 'ok'] });
check('succeeds when the spell clears on a later round', b.result === 'ok' && b.rounds === 2,
  `got ${b.result} in round ${b.rounds}`);

// 4. No run timeout (local/dev, timeoutAt null => remainingMs() is Infinity) => only MAX_ROUNDS
//    can stop it -- this is the exact non-termination trap cycle 2968 found in the original
//    trademark-search-scraper selftest before MAX_ROUNDS was added there.
const c = simulate({ budgetMs: null, outcomes: [] });
check('terminates with no deadline at all', c.rounds === MAX_ROUNDS && c.result === 'failed',
  `got ${c.result} after ${c.rounds} round(s)`);

// 5. A short budget still reports after one round -- no pause it cannot afford, same as before
//    this fix for a run that genuinely has no time left.
const d = simulate({ budgetMs: 60000, outcomes: [] });
check('short budget still reports instead of being killed', d.rounds === 1 && d.now <= 60000 - TIME_BUDGET_MARGIN_MS,
  `got ${d.rounds} round(s), stopped at ${d.now}ms`);

console.log(`\ntrace of case 1:\n  ${a.log.join('\n  ')}\n  -> ${a.result} after ${a.attempts} attempts, ${a.now / 1000}s`);
console.log(bad === 0 ? '\nALL PASS' : `\n${bad} FAILURE(S)`);
process.exit(bad === 0 ? 0 : 1);
