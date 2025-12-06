#!/bin/bash

# Hook do automatycznego generowania aktualizacji po deploy'u
# Umieść w .git/hooks/post-commit lub wywołaj ręcznie

set -e

# Sprawdź czy jest zmiana w plikach kluczowych dla deploy'u
DEPLOY_FILES="app.yaml|requirements.txt|src/|main.py"

# Pobierz zmienione pliki w ostatnim commit
CHANGED=$(git diff-tree --no-commit-id --name-only -r HEAD | grep -E "${DEPLOY_FILES}" || echo "")

if [ -n "${CHANGED}" ]; then
    echo "🔍 Wykryto zmiany w plikach deploy'owych"
    echo "🚀 Generuję automatyczną aktualizację..."

    # Uruchom generator
    ./generate-update.sh

    echo "✅ Aktualizacja wygenerowana!"
else
    echo "ℹ️  Brak zmian wymagających aktualizacji"
fi
