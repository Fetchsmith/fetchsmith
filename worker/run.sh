#!/usr/bin/env bash
# FetchSmith worker: one Claude Code cycle. Cron calls this every 20 min; flock keeps one instance.
set -uo pipefail
A=/root/agent; S=$A/state; L=$A/logs; W=$A/worker
mkdir -p "$S" "$L/runs"
exec 9>"$S/worker.lock"; flock -n 9 || exit 0
set -a; . "$A/secrets/env"; set +a
export HOME=/root PATH=/root/.local/bin:/root/.nvm/versions/node/v24.20.0/bin:/usr/local/bin:/usr/bin:/bin
export IS_SANDBOX=1 DISABLE_AUTOUPDATER=1 CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
export API_TIMEOUT_MS=600000 BASH_MAX_TIMEOUT_MS=900000 BASH_DEFAULT_TIMEOUT_MS=300000
log(){ printf '%s %s\n' "$(date -Is)" "$*" >>"$L/worker.log"; }
now=$(date +%s)
if [[ -f $S/pause_until ]] && (( $(cat "$S/pause_until") > now )); then exit 0; fi
if [[ -f $S/auth_failed ]]; then exit 2; fi

# model routing: [hard] in queue top section or every 4th cycle -> opus; else sonnet
n=$(cat "$S/cycle" 2>/dev/null || echo 0); n=$((n+1)); echo "$n" >"$S/cycle"
MODEL=${MODEL_ROUTINE:-claude-sonnet-5}
if grep -m1 -E '^- \[ \]' "$A/tasks/queue.md" | grep -q '\[hard\]' || (( n % 4 == 0 )); then MODEL=${MODEL_HARD:-claude-opus-5}; fi
[[ -f $S/force_model ]] && MODEL=$(cat "$S/force_model")

ts=$(date +%Y%m%dT%H%M%S); out=$L/runs/$ts.json
PROMPT="Run one FetchSmith work cycle (cycle #$n, model $MODEL). Follow /root/CLAUDE.md cycle protocol: read state/queue, do the top task(s) end-to-end, verify, update STATUS.md and queue.md, end with a 3-line summary. Time budget: about 25 minutes; if a task is bigger, do a coherent part and leave precise notes in queue.md for the next cycle."
log "cycle=$n model=$MODEL start"
cd /root
timeout -s INT -k 60 1700 claude -p "$PROMPT" \
  --model "$MODEL" --fallback-model claude-sonnet-5 \
  --output-format json --max-turns 120 \
  --dangerously-skip-permissions </dev/null \
  >"$out" 2>>"$L/worker.err"
rc=$?
subtype=$(jq -r '.subtype // "none"' "$out" 2>/dev/null); is_err=$(jq -r '.is_error // "?"' "$out" 2>/dev/null)
text=$(jq -r '.result // ""' "$out" 2>/dev/null); turns=$(jq -r '.num_turns // 0' "$out" 2>/dev/null)
log "cycle=$n rc=$rc subtype=$subtype is_error=$is_err turns=$turns"
printf '%s\n' "$text" | tail -12 >>"$L/worker.log"
errtail=$(tail -c 2000 "$L/worker.err" 2>/dev/null)
if grep -qiE "hit your (session|weekly|opus|sonnet)? ?limit|rate_limit_error|exceed your account'?s rate limit|usage limit" <<<"$text $errtail"; then
  hint=$(grep -oiE 'resets? [^)]*\)|resets? [0-9apm: ]+' <<<"$text $errtail" | head -1 | sed -E 's/^resets? //')
  until=$(date -d "$hint" +%s 2>/dev/null || true)
  (( ${until:-0} > now )) || until=$(( now + 3600 + RANDOM % 900 ))
  (( until - now > 6*3600 )) && until=$(( now + 6*3600 ))
  echo "$until" >"$S/pause_until"; log "usage limit; pausing until $(date -d @$until -Is)"
  if [[ $MODEL != claude-sonnet-5 ]]; then echo claude-sonnet-5 >"$S/force_model"; echo "$((now+600))" >"$S/pause_until"; log "falling back to sonnet"; fi
  exit 0
fi
rm -f "$S/force_model"
if grep -qiE "login expired|oauth token (has )?expired|invalid authentication|authentication_failed|not logged in|401" <<<"$text $errtail" && [[ $is_err == true ]]; then
  touch "$S/auth_failed"; log "AUTH FAILURE"
  "$A/bin/notify" "[FetchSmith] CRITICAL: worker auth failed" "The autonomous worker can no longer authenticate to Claude. Please run 'claude setup-token' and put the token in /root/agent/secrets/env as CLAUDE_CODE_OAUTH_TOKEN, then: rm /root/agent/state/auth_failed. Last output: $text" --once auth_failed_$(date +%Y%m%d)
  exit 2
fi
find "$L/runs" -type f -mtime +14 -delete
exit 0
