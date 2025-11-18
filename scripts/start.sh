#!/usr/bin/env bash
# Start the novahouse-chatbot-api in background (production-like)
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"
source venv/bin/activate
# Optionally set ADMIN_API_KEY in environment before running
FLASK_ENV=production nohup python src/main.py > server.log 2>&1 &
echo $! > server.pid
printf "Started server PID $(cat server.pid)\nLogs: server.log\n"
