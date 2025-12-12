#!/bin/bash
# Pre-commit hook sprawdzający bezpieczeństwo sekretów
# Użycie: ln -s ../../scripts/pre_commit_security_check.sh .git/hooks/pre-commit

echo "🔒 Sprawdzanie bezpieczeństwa sekretów przed commitem..."

# Sprawdź czy są pliki z sekretami w staging area
STAGED_FILES=$(git diff --cached --name-only)

# Lista plików które NIE powinny być commitowane
FORBIDDEN_PATTERNS=(
    "app.yaml.secret"
    "app.yaml.deploy"
    "*.secret.yaml"
    ".env"
    "*.key"
    "*.pem"
)

FOUND_SECRETS=0

for file in $STAGED_FILES; do
    for pattern in "${FORBIDDEN_PATTERNS[@]}"; do
        if [[ $file == $pattern ]] || [[ $file == *$pattern ]]; then
            echo "❌ BŁĄD: Próbujesz commitować plik z sekretami: $file"
            echo "   Ten plik zawiera wrażliwe dane i nie powinien być w repozytorium!"
            FOUND_SECRETS=1
        fi
    done
    
    # Sprawdź czy plik zawiera potencjalne sekrety
    if git diff --cached "$file" | grep -qE "sk-proj-[A-Za-z0-9_-]{40,}|sk-[A-Za-z0-9_-]{40,}"; then
        echo "❌ BŁĄD: Plik $file może zawierać sekrety API!"
        echo "   Sprawdź czy nie commitujesz kluczy API do kodu"
        FOUND_SECRETS=1
    fi
done

if [ $FOUND_SECRETS -eq 1 ]; then
    echo ""
    echo "⚠️  COMMIT ZABLOKOWANY ze względów bezpieczeństwa!"
    echo "   Usuń sekrety z plików przed commitem"
    echo "   Użyj: git reset HEAD <file> aby usunąć z staging area"
    exit 1
fi

echo "✅ Sprawdzanie bezpieczeństwa zakończone pomyślnie"
exit 0

