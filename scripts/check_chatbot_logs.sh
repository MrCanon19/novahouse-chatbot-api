#!/bin/bash
# Skrypt do sprawdzania logów chatbota w GCP
# Użycie: ./scripts/check_chatbot_logs.sh

PROJECT_ID="glass-core-467907-e9"

echo "=== 🔍 SPRAWDZANIE LOGÓW CHATBOTA W GCP ==="
echo ""

# Sprawdź czy gcloud jest dostępny
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud nie jest zainstalowany"
    echo "   Zainstaluj: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Sprawdź czy użytkownik jest zalogowany
if ! gcloud auth list --filter=status:ACTIVE --format="value(account)" &> /dev/null; then
    echo "⚠️  Nie jesteś zalogowany do gcloud"
    echo "   Zaloguj się: gcloud auth login"
    exit 1
fi

echo "✅ gcloud jest dostępny"
echo ""

# 1. Sprawdź logi GPT
echo "1. LOGI GPT (ostatnie 20):"
echo "---"
gcloud logging read "resource.type=gae_app AND textPayload=~\"GPT\"" \
    --limit 20 \
    --format="table(timestamp,textPayload)" \
    --project=$PROJECT_ID 2>&1 | head -30
echo ""

# 2. Sprawdź błędy
echo "2. BŁĘDY (ostatnie 10):"
echo "---"
gcloud logging read "resource.type=gae_app AND severity>=ERROR" \
    --limit 10 \
    --format="table(timestamp,severity,textPayload)" \
    --project=$PROJECT_ID 2>&1 | head -20
echo ""

# 3. Sprawdź ostrzeżenia
echo "3. OSTRZEŻENIA (ostatnie 10):"
echo "---"
gcloud logging read "resource.type=gae_app AND severity=WARNING AND textPayload=~\"OPENAI\"" \
    --limit 10 \
    --format="table(timestamp,textPayload)" \
    --project=$PROJECT_ID 2>&1 | head -20
echo ""

# 4. Sprawdź fallback
echo "4. FALLBACK (ostatnie 10):"
echo "---"
gcloud logging read "resource.type=gae_app AND textPayload=~\"FALLBACK\"" \
    --limit 10 \
    --format="table(timestamp,textPayload)" \
    --project=$PROJECT_ID 2>&1 | head -20
echo ""

echo "=== ✅ SPRAWDZANIE ZAKOŃCZONE ==="
echo ""
echo "💡 Wskazówki:"
echo "   • Jeśli nie widzisz logów GPT, sprawdź czy chatbot jest wdrożony"
echo "   • Jeśli widzisz błędy, sprawdź szczegóły w GCP Console"
echo "   • Pełne logi: https://console.cloud.google.com/logs?project=$PROJECT_ID"

