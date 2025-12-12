# 🔍 DIAGNOSTYKA ZAPĘTLANIA CHATBOTA

**Problem:** Chatbot zwraca ciągle tę samą odpowiedź fallback zamiast używać GPT API.

---

## 🔧 NAPRAWIONE

### 1. Poprawiono logowanie
- ✅ Zastąpiono `print()` przez `logging` dla lepszego debugowania
- ✅ Dodano szczegółowe logi dla każdego etapu przetwarzania
- ✅ Logi pokazują dokładnie gdzie proces się zatrzymuje

### 2. Poprawiono walidację OPENAI_API_KEY
- ✅ Sprawdzanie czy klucz jest ustawiony
- ✅ Sprawdzanie czy klucz nie jest testowy
- ✅ Lepsze komunikaty błędów

### 3. Poprawiono fallback response
- ✅ Lepszy komunikat z instrukcjami dla użytkownika

---

## 🔍 DIAGNOSTYKA

### Krok 1: Sprawdź czy OPENAI_API_KEY jest ustawiony

```bash
# W terminalu
echo $OPENAI_API_KEY

# W kodzie (już dodane)
logging.warning("OPENAI_API_KEY not set or is test key - GPT disabled")
```

**Oczekiwany wynik:** Klucz powinien zaczynać się od `sk-` (dla OpenAI API v1) lub `sk-proj-` (dla nowszych kluczy).

---

### Krok 2: Sprawdź logi aplikacji

Logi powinny pokazywać:
- `[GPT] Calling OpenAI API for message: ...` - jeśli GPT jest wywoływane
- `[OpenAI GPT] Response received: ...` - jeśli odpowiedź została otrzymana
- `[GPT ERROR] ...` - jeśli wystąpił błąd
- `[WARNING] OpenAI nie skonfigurowany - używam fallback` - jeśli klucz nie jest ustawiony

**Gdzie sprawdzić logi:**
- W produkcji (GCP App Engine): Cloud Logging
- Lokalnie: `tail -f logs/chatbot.log` lub stdout

---

### Krok 3: Sprawdź czy API key jest ważny

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
    except Exception as e:
        print(f"❌ API key error: {e}")
else:
    print("❌ API key not set")
```

---

### Krok 4: Sprawdź limity API

1. Zaloguj się do https://platform.openai.com/
2. Sprawdź sekcję "Usage" / "Billing"
3. Sprawdź czy nie przekroczono limitów:
   - Rate limits (requests per minute)
   - Quota limits (tokens per month)

---

## 🐛 TYPOWE PROBLEMY

### Problem 1: API key nie jest ustawiony w środowisku
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
2. Poczekaj na reset limitu
3. Rozważ upgrade planu jeśli często przekraczasz limity

---

### Problem 4: Błąd sieciowy
**Objawy:** `[GPT ERROR] ConnectionError` lub `Timeout`

**Rozwiązanie:**
1. Sprawdź połączenie sieciowe
2. Sprawdź firewall / proxy
3. Sprawdź czy OpenAI API jest dostępne (status.openai.com)

---

## 📊 MONITORING

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
1. `✅ OpenAI client initialized with model: gpt-4o-mini`
2. `[GPT] Calling OpenAI API for message: ...`
3. `[OpenAI GPT] Response received: ...`
4. **NIE** powinno być: `[WARNING] OpenAI nie skonfigurowany`

---

**Data utworzenia:** 12 grudnia 2025  
**Status:** ✅ Naprawione - dodano szczegółowe logowanie i walidację

