#!/usr/bin/env bash
# Stop the novahouse-chatbot-api background server started by start.sh
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"
if [ -f server.pid ]; then
  PID=$(cat server.pid)
  kill "$PID" || true
  rm -f server.pid
  echo "Stopped PID $PID"
else
  pkill -f "python .*src/main.py" || true
  echo "No server.pid found; attempted pkill"
fi
