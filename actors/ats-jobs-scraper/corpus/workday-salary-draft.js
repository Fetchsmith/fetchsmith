// VALIDATED DRAFT -- NOT WIRED INTO src/main.js YET (cycle 2572). See tasks/queue.md.
// Measured 24/24 correct, 26/26 correctly null against corpus/workday-salary-prose.json
// (50 live postings, 5 tenants: okgov, nvidia, adobe, salesforce, paypal; 2026-11-01).
// --- candidate workdaySalary(), to be moved into src/main.js ---
function parseMoney(raw) {
  const m = String(raw ?? '').replace(/\s+/g, '').match(/\d[\d.,]*\d|\d/);
  if (!m) return null;
  const s = m[0];
  const last = Math.max(s.lastIndexOf(','), s.lastIndexOf('.'));
  const tail = last < 0 ? '' : s.slice(last + 1);
  const n = tail.length > 0 && tail.length < 3
    ? Number(`${s.slice(0, last).replace(/[.,]/g, '')}.${tail}`)
    : Number(s.replace(/[.,]/g, ''));
  return Number.isFinite(n) ? n : null;
}
function normalizeInterval(w){const x=String(w).toLowerCase();if(x.includes('year'))return 'year';if(x.includes('hour')||x==='hr')return 'hour';if(x.includes('month'))return 'month';if(x.includes('week'))return 'week';if(x.includes('day'))return 'day';return null;}
function periodWord(text) {
  const m = String(text ?? '').match(/annualiz\w*|annual|yearly|per\s+year|\/\s?yr|hourly|per\s+hour|an\s+hour|\/\s?hr|monthly|per\s+month|weekly|per\s+week|daily|per\s+day/i);
  if (!m) return null;
  const w = m[0].toLowerCase();
  if (w.startsWith('annual')) return 'year';
  if (w.startsWith('daily')) return 'day';
  if (w === '/yr' || w === '/ yr') return 'year';
  if (w === '/hr' || w === '/ hr' || w === 'an hour') return 'hour';
  return normalizeInterval(w);
}

// A labeled pay anchor. Only text the employer itself marked as pay for THIS job counts; a bare
// "$N" anywhere in a description is never evidence of salary (measured: sign-on bonuses, benefit
// allowances and shift differentials all appear as bare figures on the same boards).
const WD_PAY_LABEL = /(?:\bcompensation\b(?!\s+for\s+this\s+role)|\bsalary\b|\bpay\s+range\b|\brange\s+of\pay\b|\brange\s+of\s+pay\b|\bpayrate\b|\bpay\s+rate\b|\bannual\s+rate\s+of\b|\bhourly\s+rate\b)/gi;
// Words that mean the money nearby is NOT base pay. A forward window is cut at the first of these.
const WD_NOT_PAY = /\b(?:bonus|benefits?\s+allowance|allowance|differential|401|relocation|stipend|reimburs\w*|incentive|equity|overtime|per\s+diem|tuition|additional\s+compensation)\b/i;
const WD_MONEY = /(?:USD|CAD|\$)\s?\d[\d,.]*|\d[\d,.]*\s?(?:USD|CAD)\b/gi;
const WD_WINDOW = 260;

function workdaySalary(text) {
  const none = { min: null, max: null, currency: null, interval: null };
  if (!text) return none;
  const t = String(text);
  const figures = [];
  let intervalText = '';
  let sawUsd = false, sawCad = false;
  WD_PAY_LABEL.lastIndex = 0;
  let lab;
  while ((lab = WD_PAY_LABEL.exec(t)) !== null) {
    let win = t.slice(lab.index, lab.index + WD_WINDOW);
    const bad = win.search(WD_NOT_PAY);
    if (bad >= 0) win = win.slice(0, bad);
    WD_MONEY.lastIndex = 0;
    let m;
    while ((m = WD_MONEY.exec(win)) !== null) {
      const v = parseMoney(m[0]);
      if (v == null) continue;
      if (/USD/i.test(m[0]) || m[0].includes('$')) sawUsd = true;
      if (/CAD/i.test(m[0])) sawCad = true;
      figures.push(v);
    }
    if (win.length) intervalText += ' ' + win;
  }
  if (!figures.length) return none;
  const interval = periodWord(intervalText);
  // Plausibility gate, keyed to the interval the board itself printed -- never to magnitude alone.
  const lo = interval === 'hour' ? 2 : 1000;
  const hi = interval === 'hour' ? 2000 : 10000000;
  const ok = figures.filter((v) => v >= lo && v <= hi);
  if (!ok.length) return none;
  // Widest span across every labeled pay figure found, because minSalary/maxSalary filter by
  // RANGE OVERLAP: a posting that pays 168k at Level 4 and 322k at Level 5, or 160k in Chicago and
  // 262k in NYC, genuinely can pay anywhere in the outer band, and narrowing to one level/city
  // would wrongly exclude it from an overlapping filter.
  return {
    min: Math.min(...ok),
    max: Math.max(...ok),
    currency: sawCad && !sawUsd ? 'CAD' : (sawUsd ? 'USD' : null),
    interval,
  };
}
module.exports = { workdaySalary };
