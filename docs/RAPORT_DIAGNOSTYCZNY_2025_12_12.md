# 📊 RAPORT DIAGNOSTYCZNY - ZAPĘTLANIE CHATBOTA

**Data:** 12 grudnia 2025  
**Status:** ✅ Kod naprawiony, wymaga konfiguracji API Key

---

## ✅ CO ZOSTAŁO NAPRAWIONE

1. **Logowanie:** Zastąpiono `print()` przez `logging` dla lepszego debugowania
2. **Walidacja API Key:** Poprawiono sprawdzanie `OPENAI_API_KEY`
3. **Komunikaty błędów:** Lepsze komunikaty dla użytkownika i deweloperów
4. **Dokumentacja:** Utworzono przewodnik diagnostyczny

---

## 📊 WYNIKI SPRAWDZENIA

### 1. ✅ KOD NAPRAWIONY

- ✅ Zastąpiono `print()` przez `logging`
- ✅ Dodano szczegółowe logi dla GPT calls:
  - `[GPT] Calling OpenAI API for message: ...`
  - `[OpenAI GPT] Response received: ...`
  - `[GPT COST] Input: X, Output: Y, Total: Z`
- ✅ Poprawiono walidację `OPENAI_API_KEY`
- ✅ Lepsze komunikaty błędów

**Pliki zmodyfikowane:**
- `src/routes/chatbot.py` - wszystkie `print()` zastąpione przez `logging`
- `src/utils/polish_declension.py` - poprawiona odmiana imion

---

### 2. ⚠️ OPENAI_API_KEY

**Status lokalny:**
- ❌ NIE ustawiony w środowisku lokalnym

**Status produkcyjny:**
- ⚠️  Wymaga sprawdzenia w `app.yaml.secret` lub GCP Secret Manager

**Rekomendacje:**
- Dla lokalnego testowania: `export OPENAI_API_KEY='sk-...'`
- Dla produkcji: Ustaw w `app.yaml.secret` lub GCP Secret Manager

---

### 3. ✅ ZALEŻNOŚCI

- ✅ `openai`: zainstalowany (wersja 2.8.1)
- ✅ `logging`: dostępny
- ✅ Wszystkie wymagane pakiety są zainstalowane

---

### 4. 📋 KONFIGURACJA

- ✅ `GPT_MODEL`: `gpt-4o-mini` (optymalny wybór)
- ✅ `GPT_FALLBACK_ENABLED`: `true`
- ✅ `MESSAGE_HISTORY_LIMIT`: `30` (ujednolicony)

---

## 🔍 JAK SPRAWDZIĆ W PRODUKCJI

### Krok 1: Sprawdź logi aplikacji

**W GCP App Engine:**
```bash
gcloud logging read "resource.type=gae_app AND textPayload=~'GPT'" --limit 50
```

**Oczekiwane logi:**
```
[GPT] Calling OpenAI API for message: ...
[OpenAI GPT] Response received: ...
[GPT COST] Input: X, Output: Y, Total: Z
```

**Jeśli widzisz:**
```
[WARNING] OpenAI nie skonfigurowany - używam fallback
```
→ Klucz API nie jest ustawiony lub jest nieprawidłowy

---

### Krok 2: Sprawdź OPENAI_API_KEY w produkcji

**W GCP Secret Manager:**
```bash
gcloud secrets versions access latest --secret="OPENAI_API_KEY"
```

**W app.yaml.secret:**
```bash
grep OPENAI_API_KEY app.yaml.secret
```

**Oczekiwany format:**
- Zaczyna się od `sk-` lub `sk-proj-`
- Długość: ~50-60 znaków
- **NIE** zaczyna się od `test_`

---

### Krok 3: Sprawdź limity API w dashboard OpenAI

1. Zaloguj się do https://platform.openai.com/
2. Przejdź do sekcji **"Usage"** / **"Billing"**
3. Sprawdź:
   - **Rate limits** (requests per minute) - czy nie przekroczone
   - **Quota limits** (tokens per month) - czy nie wyczerpane
   - **Billing** - czy konto jest aktywne

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

---

### Problem 4: Błąd sieciowy
**Objawy:** `[GPT ERROR] ConnectionError` lub `Timeout`

**Rozwiązanie:**
1. Sprawdź połączenie sieciowe
2. Sprawdź firewall / proxy
3. Sprawdź czy OpenAI API jest dostępne (status.openai.com)

---

## ✅ WERYFIKACJA NAPRAWY

Po naprawie, logi powinny pokazywać:

1. ✅ `✅ OpenAI client initialized with model: gpt-4o-mini`
2. ✅ `[GPT] Calling OpenAI API for message: ...`
3. ✅ `[OpenAI GPT] Response received: ...`
4. ✅ `[GPT COST] Input: X, Output: Y, Total: Z`
5. ❌ **NIE** powinno być: `[WARNING] OpenAI nie skonfigurowany`

---

## 📋 CHECKLISTA

- [x] Kod naprawiony (print → logging)
- [x] Walidacja API Key poprawiona
- [x] Dokumentacja utworzona
- [ ] OPENAI_API_KEY ustawiony w produkcji
- [ ] Testy w produkcji przeprowadzone
- [ ] Logi w produkcji sprawdzone

---

**Data utworzenia:** 12 grudnia 2025  
**Status:** ✅ Kod naprawiony, wymaga konfiguracji API Key w produkcji

