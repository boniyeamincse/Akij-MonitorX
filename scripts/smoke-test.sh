#!/usr/bin/env bash
# Smoke test for Akij MonitorX (Linux - Debian/Ubuntu)
# - Starts the Node server in background
# - Runs the agent once to send metrics
# - Hits /api/metrics and exits

set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$PROJECT_ROOT"

echo "Starting smoke test (Linux)..."

# Start server in background
node src/server.js &
SERVER_PID=$!
echo "Started server (pid $SERVER_PID)"

sleep 2

# Run agent in background
node src/agent.js &
AGENT_PID=$!
echo "Started agent (pid $AGENT_PID)"

sleep 4

echo "Checking /api/metrics..."
if curl -sSf http://localhost:3000/api/metrics > /tmp/metrics.json; then
  echo "API /api/metrics response saved to /tmp/metrics.json"
  cat /tmp/metrics.json
  SUCCESS=0
else
  echo "Failed to get /api/metrics" >&2
  SUCCESS=1
fi

# Cleanup
if kill -0 $AGENT_PID 2>/dev/null; then
  kill $AGENT_PID || true
fi
if kill -0 $SERVER_PID 2>/dev/null; then
  kill $SERVER_PID || true
fi

exit $SUCCESS
