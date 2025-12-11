#!/bin/bash
# Quick commit script - pomija pre-commit hooks
# Użycie: ./scripts/quick_commit_no_hooks.sh "Twoja wiadomość commit"

set -e  # Zatrzymaj przy błędzie

# Przejdź do katalogu projektu
cd "$(dirname "$0")/.."

# Sprawdź czy jesteś w repo git
if [ ! -d .git ]; then
    echo "❌ Błąd: To nie jest repozytorium git!"
    exit 1
fi

# Pobierz wiadomość commit (domyślnie jeśli nie podano)
COMMIT_MSG="${1:-Aktualizacja kodu}"

echo "=== 🚀 QUICK COMMIT & PUSH (bez hooks) ==="
echo ""
echo "📁 Katalog: $(pwd)"
echo "💬 Commit message: $COMMIT_MSG"
echo ""

# Sprawdź status
echo "📋 Status zmian:"
git status --short

# Sprawdź czy są zmiany
if [ -z "$(git status --porcelain)" ]; then
    echo ""
    echo "ℹ️  Brak zmian do commitowania"
    exit 0
fi

echo ""
read -p "✅ Kontynuować? (y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Anulowano"
    exit 1
fi

# Dodaj wszystkie zmiany
echo "📦 Dodawanie zmian..."
git add .

# Commit (bez pre-commit hooks)
echo "💾 Commitowanie (bez hooks)..."
git commit --no-verify -am "$COMMIT_MSG"

# Push
echo "🚀 Pushowanie do GitHub..."
git push

echo ""
echo "✅ GOTOWE! Zmiany wysłane do GitHub"
echo "🔗 Repo: $(git remote get-url origin)"

