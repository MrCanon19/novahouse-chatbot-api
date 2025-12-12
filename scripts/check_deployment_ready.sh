#!/bin/bash
# Skrypt sprawdzający gotowość do wdrożenia
# Użycie: ./scripts/check_deployment_ready.sh

echo "=== 🔍 SPRAWDZANIE GOTOWOŚCI DO WDROŻENIA ==="
echo ""

ERRORS=0
WARNINGS=0

# 1. Sprawdź app.yaml.secret
echo "1. Sprawdzanie app.yaml.secret..."
if [ -f "app.yaml.secret" ]; then
    if grep -q "OPENAI_API_KEY.*sk-" app.yaml.secret 2>/dev/null; then
        echo "   ✅ OPENAI_API_KEY znaleziony"
    else
        echo "   ❌ OPENAI_API_KEY nie znaleziony lub nieprawidłowy"
        ((ERRORS++))
    fi
    
    if grep -q "ADMIN_API_KEY" app.yaml.secret 2>/dev/null; then
        echo "   ✅ ADMIN_API_KEY znaleziony"
    else
        echo "   ⚠️  ADMIN_API_KEY nie znaleziony"
        ((WARNINGS++))
    fi
    
    if grep -q "DATABASE_URL" app.yaml.secret 2>/dev/null; then
        echo "   ✅ DATABASE_URL znaleziony"
    else
        echo "   ⚠️  DATABASE_URL nie znaleziony"
        ((WARNINGS++))
    fi
else
    echo "   ❌ app.yaml.secret nie istnieje"
    ((ERRORS++))
fi

echo ""

# 2. Sprawdź czy logging jest używany
echo "2. Sprawdzanie kodu..."
if grep -q "logging\." src/routes/chatbot.py 2>/dev/null; then
    echo "   ✅ Logging jest używany zamiast print()"
else
    echo "   ⚠️  Sprawdź czy logging jest używany"
    ((WARNINGS++))
fi

if grep -q "logging.warning.*OPENAI_API_KEY" src/routes/chatbot.py 2>/dev/null; then
    echo "   ✅ Walidacja OPENAI_API_KEY jest w kodzie"
else
    echo "   ⚠️  Sprawdź walidację API key"
    ((WARNINGS++))
fi

echo ""

# 3. Sprawdź zależności
echo "3. Sprawdzanie zależności..."
if python3 -c "import openai" 2>/dev/null; then
    echo "   ✅ Pakiet openai zainstalowany"
else
    echo "   ❌ Pakiet openai NIE jest zainstalowany"
    ((ERRORS++))
fi

if python3 -c "import flask" 2>/dev/null; then
    echo "   ✅ Pakiet flask zainstalowany"
else
    echo "   ❌ Pakiet flask NIE jest zainstalowany"
    ((ERRORS++))
fi

echo ""

# 4. Sprawdź dokumentację
echo "4. Sprawdzanie dokumentacji..."
if [ -f "docs/RAPORT_DIAGNOSTYCZNY_2025_12_12.md" ]; then
    echo "   ✅ Raport diagnostyczny utworzony"
else
    echo "   ⚠️  Raport diagnostyczny nie istnieje"
    ((WARNINGS++))
fi

if [ -f "docs/SPRAWDZENIE_ZAPETLANIA.md" ]; then
    echo "   ✅ Instrukcja sprawdzania utworzona"
else
    echo "   ⚠️  Instrukcja sprawdzania nie istnieje"
    ((WARNINGS++))
fi

echo ""
echo "=========================================="
echo "📊 PODSUMOWANIE:"
echo "   Błędy: $ERRORS"
echo "   Ostrzeżenia: $WARNINGS"
echo ""

if [ $ERRORS -eq 0 ]; then
    echo "✅ GOTOWE DO WDROŻENIA!"
    if [ $WARNINGS -gt 0 ]; then
        echo "   (z $WARNINGS ostrzeżeniami - sprawdź przed wdrożeniem)"
    fi
    exit 0
else
    echo "❌ NIE GOTOWE DO WDROŻENIA"
    echo "   Napraw $ERRORS błędy przed wdrożeniem"
    exit 1
fi

