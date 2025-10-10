#!/bin/bash
set -e

# Automatyczny push wszystkich zmian do GitHuba
REPO_DIR="$HOME/novahouse-import/novahouse-chatbot-api"
cd "$REPO_DIR"

echo "📦 Sprawdzam zmiany..."
git status --short

# Automatyczny opis commita z datą i godziną
MSG="Auto-commit $(date '+%Y-%m-%d %H:%M:%S')"

git add .
git commit -m "$MSG" || echo "Brak nowych zmian."
git push

echo
echo "✅ Zmiany zostały wysłane do GitHuba o $(date '+%H:%M:%S')"
git status -sb

