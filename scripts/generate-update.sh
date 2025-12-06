#!/bin/bash

# Script do automatycznego generowania pliku aktualizacji po deploy'u
# Autor: NovaHouse Team
# Data: 18.11.2025

set -e

# Kolory dla output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Generator Aktualizacji Projektu${NC}"
echo "=================================="

# Pobierz aktualną wersję z app.yaml lub ustaw domyślną
if [ -f "app.yaml" ]; then
    VERSION=$(grep -E "^# Version:" app.yaml | awk '{print $3}' || echo "2.3.0")
else
    VERSION="2.3.0"
fi

# Pobierz datę deployment
DEPLOY_DATE=$(date +"%Y%m%d")
DEPLOY_TIME=$(date +"%H:%M")
READABLE_DATE=$(date +"%d.%m.%Y")

# Pobierz informacje z git
COMMIT_HASH=$(git rev-parse --short HEAD)
COMMIT_MSG=$(git log -1 --pretty=%B)
BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Pobierz zmiany z ostatniego commita
CHANGED_FILES=$(git diff-tree --no-commit-id --name-only -r HEAD | wc -l | tr -d ' ')

# Nazwa pliku
UPDATE_FILE="updates/AKTUALIZACJA_${DEPLOY_DATE}_V${VERSION}.md"

echo -e "${YELLOW}📝 Generuję aktualizację:${NC}"
echo "  Wersja: ${VERSION}"
echo "  Data: ${READABLE_DATE} ${DEPLOY_TIME}"
echo "  Commit: ${COMMIT_HASH}"
echo "  Zmienione pliki: ${CHANGED_FILES}"
echo ""

# Generuj plik aktualizacji
cat > "${UPDATE_FILE}" << EOF
# 🚀 Aktualizacja Projektu NovaHouse Chatbot

**Wersja:** ${VERSION}
**Data deployment:** ${READABLE_DATE} ${DEPLOY_TIME}
**Branch:** ${BRANCH}
**Commit:** ${COMMIT_HASH}

---

## 📋 Informacje o Deploy'u

**URL Aplikacji:** https://glass-core-467907-e9.ey.r.appspot.com

**Ostatni commit:**
\`\`\`
${COMMIT_MSG}
\`\`\`

**Zmienione pliki:** ${CHANGED_FILES}

---

## ✅ Status Komponentów

- [ ] Backend API
- [ ] Frontend (Chatbot)
- [ ] Dashboard
- [ ] WebSocket
- [ ] Baza danych
- [ ] Cache (Redis)
- [ ] Integracje (Monday, Email)

---

## 🔧 Zmiany w Tej Wersji

<!-- Automatycznie wygenerowane zmiany z git -->
$(git log --oneline -5 --pretty=format:"- %s (%h)")

---

## 📊 Metryki Wydajności

**Do sprawdzenia po deploy'u:**
- Health check: \`curl https://glass-core-467907-e9.ey.r.appspot.com/api/chatbot/health\`
- Response time: ___s
- Memory usage: ___MB
- CPU usage: ___%

---

## 🐛 Znane Problemy

<!-- Dodaj znane problemy lub zostaw puste -->
- Brak

---

## 📝 Notatki

<!-- Dodatkowe uwagi dotyczące tego deployu -->
- Automatycznie wygenerowane przez \`generate-update.sh\`
- Wymagane uzupełnienie checklist'y statusów

---

**Wygenerowano:** ${READABLE_DATE} ${DEPLOY_TIME}
**Status:** 🟡 Oczekuje na weryfikację
EOF

echo -e "${GREEN}✅ Utworzono: ${UPDATE_FILE}${NC}"
echo ""
echo -e "${YELLOW}📌 Następne kroki:${NC}"
echo "1. Otwórz plik i uzupełnij checklist statusów"
echo "2. Sprawdź metryki wydajności"
echo "3. Dodaj dodatkowe notatki jeśli potrzeba"
echo "4. Commit: git add ${UPDATE_FILE} && git commit -m 'Docs: Aktualizacja ${DEPLOY_DATE}' && git push"
echo ""
echo -e "${BLUE}💡 Aby otworzyć plik:${NC} code ${UPDATE_FILE}"
