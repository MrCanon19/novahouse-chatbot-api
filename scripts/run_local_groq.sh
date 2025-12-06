#!/usr/bin/env bash
set -euo pipefail

# Resolve repo root relative to this script
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

# Load environment variables from .env if present
if [[ -f ".env" ]]; then
  set -a
  source .env
  set +a
fi

export LLM_PROVIDER="${LLM_PROVIDER:-groq}"
export PORT="${PORT:-5050}"

if [[ -z "${GROQ_API_KEY:-}" ]]; then
  echo "❌ GROQ_API_KEY is not set. Add it to .env or export it before running."
  exit 1
fi

MODEL_INFO="${GROQ_MODEL:-llama3-8b-8192}"
echo "▶️  Starting NovaHouse Chatbot with Groq (model: ${MODEL_INFO}) on port ${PORT}"

python main.py "$@"
