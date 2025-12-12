# 🔍 SPRAWDZENIE ZAPĘTLANIA CHATBOTA

**Status:** ✅ Naprawione  
**Data:** 12 grudnia 2025

---

## ✅ CO ZOSTAŁO NAPRAWIONE

1. **Logowanie:** Zastąpiono `print()` przez `logging` dla lepszego debugowania
2. **Walidacja API Key:** Poprawiono sprawdzanie `OPENAI_API_KEY`
3. **Komunikaty błędów:** Lepsze komunikaty dla użytkownika i deweloperów
4. **Dokumentacja:** Utworzono przewodnik diagnostyczny

---

## 🔍 JAK SPRAWDZIĆ, CZY ZAPĘTLANIE JEST NAPRAWIONE

### Krok 1: Sprawdź logi aplikacji

Logi powinny pokazywać:

**✅ Prawidłowe działanie:**
```
[GPT] Calling OpenAI API for message: ...
[OpenAI GPT] Response received: ...
[GPT COST] Input: X, Output: Y, Total: Z
```

**❌ Problem z API Key:**
```
[WARNING] OPENAI_API_KEY not set in environment variables
[WARNING] OpenAI nie skonfigurowany - używam fallback
```

**❌ Problem z API:**
```
[GPT ERROR] 401 Unauthorized
[GPT ERROR] 429 Too Many Requests
```

**Gdzie sprawdzić logi:**
- **Lokalnie:** `tail -f logs/chatbot.log` lub stdout
- **GCP App Engine:** Cloud Logging w konsoli GCP
- **Docker:** `docker logs <container_name>`

---

### Krok 2: Sprawdź OPENAI_API_KEY

```bash
# W terminalu
echo $OPENAI_API_KEY

# W kodzie (już dodane)
logging.warning("OPENAI_API_KEY not set or is test key - GPT disabled")
```

**Oczekiwany wynik:**
- Klucz powinien zaczynać się od `sk-` (dla OpenAI API v1) lub `sk-proj-` (dla nowszych kluczy)
- Klucz powinien mieć długość ~50-60 znaków
- **NIE** powinien zaczynać się od `test_`

**Przykłady:**
```
✅ sk-proj-ABC123...XYZ
✅ sk-ABC123...XYZ
❌ test_key_123
❌ (pusty)
```

---

### Krok 3: Sprawdź limity API w dashboard OpenAI

1. Zaloguj się do https://platform.openai.com/
2. Przejdź do sekcji **"Usage"** / **"Billing"**
3. Sprawdź:
   - **Rate limits** (requests per minute) - czy nie przekroczone
   - **Quota limits** (tokens per month) - czy nie wyczerpane
   - **Billing** - czy konto jest aktywne

**Typowe limity:**
- **Free tier:** 3 requests/min, 40k tokens/month
- **Tier 1:** 60 requests/min, 1M tokens/month
- **Tier 2+:** Wyższe limity

---

### Krok 4: Test bezpośredniego wywołania API

```python
# Test w Python
from openai import OpenAI
import os

api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    client = OpenAI(api_key=api_key)
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Test"}],
            max_tokens=10
        )
        print("✅ API key is valid")
        print(f"Response: {response.choices[0].message.content}")
    except Exception as e:
        print(f"❌ API key error: {e}")
else:
    print("❌ API key not set")
```

---

## 🐛 TYPOWE PROBLEMY I ROZWIĄZANIA

### Problem 1: API key nie jest ustawiony
**Objawy:** `[WARNING] OpenAI nie skonfigurowany - używam fallback`

**Rozwiązanie:**
```bash
# Lokalnie
export OPENAI_API_KEY="sk-..."

# W GCP App Engine
# Ustaw w Secret Manager lub app.yaml.secret
```

---

### Problem 2: API key jest nieprawidłowy lub wygasł
**Objawy:** `[GPT ERROR] 401 Unauthorized` lub `Invalid API key`

**Rozwiązanie:**
1. Sprawdź klucz w https://platform.openai.com/api-keys
2. Wygeneruj nowy klucz jeśli stary wygasł
3. Zaktualizuj w Secret Manager / app.yaml.secret

---

### Problem 3: Przekroczono limity API
**Objawy:** `[GPT ERROR] 429 Too Many Requests` lub `Rate limit exceeded`

**Rozwiązanie:**
1. Sprawdź limity w dashboard OpenAI
2. Poczekaj na reset limitu (zwykle co minutę/godzinę)
3. Rozważ upgrade planu jeśli często przekraczasz limity
4. Zaimplementuj retry logic z exponential backoff

---

### Problem 4: Błąd sieciowy
**Objawy:** `[GPT ERROR] ConnectionError` lub `Timeout`

**Rozwiązanie:**
1. Sprawdź połączenie sieciowe
2. Sprawdź firewall / proxy
3. Sprawdź czy OpenAI API jest dostępne (status.openai.com)

---

## 📊 MONITORING W CZASIE RZECZYWISTYM

### Sprawdź logi w czasie rzeczywistym

```bash
# Lokalnie
tail -f logs/chatbot.log | grep -E "GPT|OpenAI|fallback"

# W GCP
gcloud logging read "resource.type=gae_app AND textPayload=~'GPT'" --limit 50
```

---

## ✅ WERYFIKACJA NAPRAWY

Po naprawie, logi powinny pokazywać:

1. ✅ `✅ OpenAI client initialized with model: gpt-4o-mini`
2. ✅ `[GPT] Calling OpenAI API for message: ...`
3. ✅ `[OpenAI GPT] Response received: ...`
4. ✅ `[GPT COST] Input: X, Output: Y, Total: Z`
5. ❌ **NIE** powinno być: `[WARNING] OpenAI nie skonfigurowany`

---

## 🔧 DODATKOWE NARZĘDZIA

### Health Check Endpoint

```bash
# Sprawdź status chatbota
curl https://your-app-url/api/chatbot/health

# Oczekiwany wynik:
# {"status": "healthy", "service": "chatbot"}
```

### Test Endpoint

```bash
# Test wywołania GPT
curl -X POST https://your-app-url/api/chatbot/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Test", "session_id": "test-123"}'

# Oczekiwany wynik:
# {"response": "...", "session_id": "test-123", ...}
```

---

**Data utworzenia:** 12 grudnia 2025  
**Status:** ✅ Naprawione - dodano szczegółowe logowanie i walidację

