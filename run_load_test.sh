#!/usr/bin/env bash
set -euo pipefail

cleanup() {
  echo "Cleaning up…"
  kill "${LOCUST_PID:-}" 2>/dev/null || true
}
trap cleanup EXIT

# ─────────────── CONFIG ───────────────
PROJECT="ancient-ensign-451511-f4"
NAMESPACE="todo-app"
LOCUSTFILE="performance/locustfile.py"
HOST="http://34.31.66.206:5001" # dış IP ve port doğruysa
DURATION=60
WARMUP=30

# ──────── CPU SAMPLING FUNCTION ────────
get_cpu() {
  if date -v -60S &>/dev/null; then
    START=$(date -u -v -60S +%Y-%m-%dT%H:%M:%SZ)
  else
    START=$(date -u -d '60 seconds ago' +%Y-%m-%dT%H:%M:%SZ)
  fi
  NOW=$(date -u +%Y-%m-%dT%H:%M:%SZ)

  gcloud monitoring time-series list \
    --project="$PROJECT" \
    --filter='metric.type="kubernetes.io/container/cpu/usage_time" AND resource.namespace_name="todo-app" AND resource.container_name="todo-backend"' \
    --interval-start="$START" \
    --interval-end="$NOW" \
    --format="value(timeSeries[0].points[0].value.doubleValue)" || echo "0"
}

# ─────────────── 2 PARAMETRELİ TEST ───────────────
echo "users,spawn_rate,avg_cpu_core_seconds_per_sec"
for USERS in 10 50; do
  for SPAWN in 1 5; do
    echo "Testing $USERS users with spawn rate $SPAWN..."
    LOCUST_PID=""
    locust -f "$LOCUSTFILE" \
      --headless \
      -u "$USERS" \
      -r "$SPAWN" \
      -t "${DURATION}s" \
      --host "$HOST" \
      --csv="/tmp/locust_u${USERS}_r${SPAWN}" \
      --csv-full-history \
      & LOCUST_PID=$!

    sleep "$WARMUP"

    CPU=$(get_cpu)
    echo "$USERS,$SPAWN,$CPU"
    kill "$LOCUST_PID"
    wait "$LOCUST_PID" 2>/dev/null
  done
done

echo "done."

