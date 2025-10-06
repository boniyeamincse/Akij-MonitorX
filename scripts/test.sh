#!/usr/bin/env bash
set -euo pipefail

# Full system test script
# - Brings up docker-compose stack
# - Waits for key service ports to be available
# - Runs the existing linux smoke test

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT_DIR"

echo "Starting full system with docker-compose..."
docker-compose up -d

check_tcp(){
  local host="$1" port="$2" timeout=${3:-120}
  echo -n "Waiting for $host:$port `";
  for i in $(seq 1 $timeout); do
    if bash -c "</dev/tcp/$host/$port" >/dev/null 2>&1; then
      echo " up";
      return 0;
    fi
    sleep 1
  done
  echo " timed out after ${timeout}s";
  return 1
}

echo "Checking key services..."
# Zabbix web (HTTP)
check_tcp localhost 8080 180
# Grafana (HTTP)
check_tcp localhost 3000 180
# Alertmanager (HTTP)
check_tcp localhost 9093 120 || true

echo "Running repository smoke test (linux)..."
npm run smoke-test:linux

echo "Full system test completed."
