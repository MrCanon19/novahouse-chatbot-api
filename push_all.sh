#!/bin/bash
set -e

# Skrypt automatycznego dodawania i wysyłania zmian do GitHub
REPO_DIR="$HOME/novahouse-import/novahouse-chatbot-api"
cd "$REPO_DIR"

# Sprawdź status
echo "📦 Sprawdzam zmiany..."
git status --short

# Zapytaj o opis commita
echo
read -p "✏️  Podaj opis commita: " MSG
if [ -z "$MSG" ]; then
  MSG="Aktualizacja $(date +%F_%H-%M)"
fi

# Dodaj, commituj i pushuj
git add .
git commit -m "$MSG" || echo "Brak nowych zmian."
git push

echo
echo "✅ Zmiany zostały wysłane do GitHuba!"
git status -sb

