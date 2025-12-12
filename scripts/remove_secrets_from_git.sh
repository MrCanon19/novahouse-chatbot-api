#!/bin/bash
# Skrypt usuwający sekrety z Git history
# UWAGA: To jest destrukcyjna operacja - użyj tylko jeśli jesteś pewien!

echo "⚠️  UWAGA: Ten skrypt usunie pliki z sekretami z Git!"
echo "   Upewnij się, że masz backup przed kontynuacją."
echo ""
read -p "Czy na pewno chcesz kontynuować? (tak/nie): " confirm

if [ "$confirm" != "tak" ]; then
    echo "Anulowano."
    exit 0
fi

echo ""
echo "🔒 Usuwanie plików z sekretami z Git..."

# Lista plików do usunięcia
FILES_TO_REMOVE=(
    "app.yaml.deploy"
    "app.yaml.deploy.*"
    "config/app.yaml"
)

for file in "${FILES_TO_REMOVE[@]}"; do
    if git ls-files | grep -q "$file"; then
        echo "   Usuwam: $file"
        git rm --cached "$file" 2>/dev/null || true
    fi
done

echo ""
echo "✅ Pliki usunięte z Git (ale pozostają lokalnie)"
echo ""
echo "📝 NASTĘPNE KROKI:"
echo "   1. Sprawdź zmiany: git status"
echo "   2. Commit: git commit -m 'Remove secrets from Git'"
echo "   3. Jeśli pliki były w historii, użyj git filter-repo do całkowitego usunięcia"
echo ""
echo "⚠️  WAŻNE: Jeśli pliki były już w historii Git, użyj:"
echo "   git filter-repo --path app.yaml.deploy --invert-paths"
echo "   (wymaga: pip install git-filter-repo)"

