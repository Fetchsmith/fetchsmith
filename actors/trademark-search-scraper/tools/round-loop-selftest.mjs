// Self-test for fetchPage()'s round loop (cycle 2968). The loop cannot be exercised by a normal
// run -- 168 of 195 external runs reach TMview on attempt 0 -- and the failure it exists to fix
// (every proxy session AND direct failing transport-level in 35s of a 298s budget, run
// m6yx4Y87ooaDWhvXa) only reproduces when Apify's exit nodes are actually flaky. So the control
// flow is mirrored here against a stubbed attempt outcome and a fake clock.
//
// This is a MIRROR, not the real function: if the round loop in src/main.js changes, change this
// too. What it pins down is the four properties the real loop must have.
//   node tools/round-loop-selftest.mjs

const PROXY_ROTATIONS = 3;
const REQUEST_TIMEOUT_MS = 30000;
const DEADLINE_RESERVE_MS = 15000;
const MIN_ATTEMPT_MS = 5000;
const ROUND_PAUSE_MS = 15000;
const ROUND_PAUSE_MAX_MS = 45000;
const MAX_ROUNDS = 8;

// `outcomes` is consulted per attempt: 'fail' = transport error, 'ok' = HTTP 200.
// Every attempt burns `attemptMs` on the fake clock; pauses burn their full length.
function simulate({ budgetMs, outcomes, attemptMs = 10000 }) {
  let now = 0;
  const deadline = budgetMs === null ? null : budgetMs;
  const remaining = () => (deadline === null ? Infinity : deadline - now - DEADLINE_RESERVE_MS);
  const log = [];
  let attempts = 0;
  let proxyUrl = 'http://proxy';
  let lastErr;
  let outOfTime = false;
  let round = 0;

  for (;;) {
    for (let attempt = 0; attempt <= PROXY_ROTATIONS; attempt += 1) {
      const budget = remaining();
      if (budget < MIN_ATTEMPT_MS) { outOfTime = true; break; }
      if (attempt > 0) {
        const rotated = attempt < PROXY_ROTATIONS;
        if (!rotated) {
          if (!proxyUrl) break;
          proxyUrl = undefined;
          log.push(`r${round}: direct`);
        } else {
          log.push(`r${round}: rotate ${attempt}`);
        }
      } else {
        log.push(`r${round}: attempt 0 (${proxyUrl ? 'proxy' : 'direct'})`);
      }
      // The real attempt is capped by whichever of the request timeout / remaining budget is
      // smaller; a failing attempt burns that, never more.
      now += Math.min(attemptMs, REQUEST_TIMEOUT_MS, budget);
      attempts += 1;
      const outcome = outcomes[attempts - 1] ?? 'fail';
      if (outcome === 'ok') return { result: 'ok', attempts, rounds: round + 1, now, log };
      lastErr = new Error('transport');
    }
    if (outOfTime || round >= MAX_ROUNDS) break;
    const pause = Math.min(ROUND_PAUSE_MS * (round + 1), ROUND_PAUSE_MAX_MS);
    if (remaining() < pause + MIN_ATTEMPT_MS) break;
    round += 1;
    now += pause;
    log.push(`pause ${pause / 1000}s -> round ${round + 1}`);
    proxyUrl = 'http://proxy'; // rotateProxy() re-arms the session for the new round
  }
  return {
    result: outOfTime ? 'outOfTime' : 'failed', attempts, rounds: round + 1, now, log, lastErr,
  };
}

let bad = 0;
const check = (name, cond, detail) => {
  if (cond) { console.log(`ok   ${name}`); } else { bad += 1; console.log(`FAIL ${name} -- ${detail}`); }
};

// 1. The regression this fix is for: the whole ladder fails, but the 298s budget had room for
//    more. Before the fix this was 4 attempts / 1 round / FAILED at ~35s.
const a = simulate({ budgetMs: 298000, outcomes: [] });
check('exhausted ladder keeps retrying inside a 298s budget', a.rounds > 1 && a.attempts > PROXY_ROTATIONS + 1,
  `got ${a.attempts} attempts in ${a.rounds} round(s)`);

// 2. It must never run past the deadline reserve -- a TIMED-OUT run is strictly worse than a
//    FAILED one (h826): the container is killed with no status message and no baseline save.
check('never spends into the deadline reserve', a.now <= 298000 - DEADLINE_RESERVE_MS,
  `stopped at ${a.now}ms of a ${298000 - DEADLINE_RESERVE_MS}ms spendable budget`);

// 3. A flaky spell that clears on round 2 must return rows, not an error -- this is the whole
//    point: the run does the "re-run in a few minutes" that the old error text asked the buyer for.
const b = simulate({ budgetMs: 298000, outcomes: ['fail', 'fail', 'fail', 'fail', 'ok'] });
check('succeeds when the spell clears on a later round', b.result === 'ok' && b.rounds === 2,
  `got ${b.result} in round ${b.rounds}`);

// 4. No run timeout (local/dev) => remaining() is Infinity, so only MAX_ROUNDS can stop it.
const c = simulate({ budgetMs: null, outcomes: [] });
check('terminates with no deadline at all', c.rounds === MAX_ROUNDS + 1 && c.result === 'failed',
  `got ${c.result} after ${c.rounds} round(s)`);

// 5. A short budget must behave as before -- one ladder, then report. No pause it cannot afford.
const d = simulate({ budgetMs: 60000, outcomes: [] });
check('short budget still reports instead of being killed', d.rounds === 1 && d.now <= 60000 - DEADLINE_RESERVE_MS,
  `got ${d.rounds} round(s), stopped at ${d.now}ms`);

// 6. Attempt 0 of a fresh round must be back on the proxy, not left on the direct connection the
//    previous round downgraded to (cycle 513: direct is unreliable from Apify's own egress).
check('a new round re-arms the proxy', a.log.includes('r1: attempt 0 (proxy)'),
  `round-1 opening attempt was: ${a.log.find((l) => l.startsWith('r1: attempt 0'))}`);

console.log(`\ntrace of case 1:\n  ${a.log.join('\n  ')}\n  -> ${a.result} after ${a.attempts} attempts, ${a.now / 1000}s`);
console.log(bad === 0 ? '\nALL PASS' : `\n${bad} FAILURE(S)`);
process.exit(bad === 0 ? 0 : 1);
