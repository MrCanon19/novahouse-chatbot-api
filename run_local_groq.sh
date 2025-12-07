#!/usr/bin/env bash

# Exit on error
set -e

echo "Loading environment..."
if [ -f ".env" ]; then
  export $(grep -v '^#' .env | xargs)
fi

export LLM_PROVIDER=groq

echo "Starting backend with Groq provider on port 5050..."
python main.py
