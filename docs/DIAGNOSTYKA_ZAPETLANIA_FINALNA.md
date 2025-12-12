# 🔍 FINALNA DIAGNOSTYKA ZAPĘTLANIA CHATBOTA

**Data:** 12 grudnia 2025  
**Status:** ✅ Kompleksowa naprawa zakończona

---

## ✅ CO ZOSTAŁO NAPRAWIONE

### 1. Szczegółowe Logowanie
- ✅ Logowanie na każdym kroku GPT flow
- ✅ Logowanie statusu API key w każdym miejscu
- ✅ Logowanie błędów z pełnymi szczegółami
- ✅ Logowanie fallback responses

### 2. Walidacja
- ✅ Walidacja odpowiedzi GPT (sprawdzanie czy nie jest pusta)
- ✅ Test API key przy inicjalizacji klienta
- ✅ Sprawdzanie czy client jest None

### 3. Diagnostyka
- ✅ Logowanie każdego kroku procesu
- ✅ Logowanie statusu API key w każdym miejscu
- ✅ Logowanie pełnych szczegółów błędów

---

## 🔍 JAK SPRAWDZIĆ LOGI

### Lokalnie

```bash
# Sprawdź logi aplikacji
tail -f logs/chatbot.log

# Szukaj logów GPT
grep "GPT" logs/chatbot.log | tail -20
```

### W Produkcji (GCP)

```bash
# Sprawdź logi GPT
gcloud logging read "resource.type=gae_app AND textPayload=~'GPT'" --limit 50 --project=glass-core-467907-e9

# Sprawdź wszystkie logi aplikacji
gcloud logging read "resource.type=gae_app" --limit 50 --project=glass-core-467907-e9

# Sprawdź błędy
gcloud logging read "resource.type=gae_app AND severity>=ERROR" --limit 20 --project=glass-core-467907-e9
```

### W GCP Console

1. Przejdź do: https://console.cloud.google.com/logs
2. Wybierz projekt: `glass-core-467907-e9`
3. Filtruj: `resource.type=gae_app AND textPayload=~"GPT"`
4. Sprawdź ostatnie logi

---

## 📋 CO SPRAWDZIĆ W LOGACH

### 1. Czy API key jest ustawiony

**Szukaj:**
```
✅ OpenAI client initialized with model: gpt-4o-mini
✅ OpenAI client test successful - API key is valid
```

**Jeśli widzisz:**
```
⚠️  OPENAI_API_KEY not set in environment variables
⚠️  OPENAI_API_KEY missing/placeholder
```
→ **Problem:** API key nie jest ustawiony w produkcji

**Rozwiązanie:**
- Sprawdź `app.yaml.secret` czy zawiera `OPENAI_API_KEY`
- Sprawdź GCP Secret Manager
- Sprawdź zmienne środowiskowe w App Engine

---

### 2. Czy klient jest inicjalizowany

**Szukaj:**
```
[GPT FLOW] No FAQ match for: ... - attempting GPT call
[INFO] OpenAI client initialized successfully - retrying GPT call
✅ OpenAI GPT-4o-mini client ready
```

**Jeśli widzisz:**
```
[WARNING] ensure_openai_client() returned None
[ERROR] Direct get_openai_client() also returned None!
```
→ **Problem:** Klient nie może być zainicjalizowany

**Rozwiązanie:**
- Sprawdź czy API key jest ważny
- Sprawdź czy pakiet `openai` jest zainstalowany
- Sprawdź limity API w dashboard OpenAI

---

### 3. Czy GPT jest wywoływane

**Szukaj:**
```
[OpenAI GPT] Przetwarzanie: ...
[GPT FLOW] OpenAI client available - calling GPT API for: ...
```

**Jeśli widzisz:**
```
[FALLBACK] Using default response
[WARNING] OpenAI nie skonfigurowany - używam fallback
```
→ **Problem:** GPT nie jest wywoływane

**Rozwiązanie:**
- Sprawdź czy `client` nie jest None
- Sprawdź logi błędów GPT
- Sprawdź czy API key jest ważny

---

### 4. Czy odpowiedź jest otrzymywana

**Szukaj:**
```
[OpenAI GPT] Response received: ...
[GPT COST] Input: X, Output: Y, Total: Z
```

**Jeśli widzisz:**
```
[GPT ERROR] Empty response from GPT API!
[GPT ERROR] ...
```
→ **Problem:** GPT zwraca pustą odpowiedź lub błąd

**Rozwiązanie:**
- Sprawdź szczegóły błędu w logach
- Sprawdź limity API w dashboard OpenAI
- Sprawdź czy model jest dostępny

---

### 5. Gdzie i dlaczego fallback jest używany

**Szukaj:**
```
[FALLBACK] Using default response: ...
[CRITICAL FALLBACK] Używam awaryjnej odpowiedzi
```

**Sprawdź kontekst:**
- Czy poprzedza to błąd GPT?
- Czy poprzedza to brak klienta?
- Czy poprzedza to pustą odpowiedź?

---

## 🚨 TYPOWE PROBLEMY I ROZWIĄZANIA

### Problem 1: API key nie jest ustawiony

**Objawy:**
```
⚠️  OPENAI_API_KEY not set in environment variables
[FALLBACK] Using default response (no client)
```

**Rozwiązanie:**
1. Sprawdź `app.yaml.secret`:
   ```yaml
   env_variables:
     OPENAI_API_KEY: "sk-proj-..."
   ```

2. Sprawdź GCP Secret Manager:
   ```bash
   gcloud secrets versions access latest --secret="OPENAI_API_KEY" --project=glass-core-467907-e9
   ```

3. Wdróż ponownie:
   ```bash
   ./scripts/deploy_production.sh
   ```

---

### Problem 2: API key jest nieprawidłowy

**Objawy:**
```
❌ OpenAI client test failed: 401 Unauthorized
[ERROR] OPENAI_API_KEY is set but client initialization failed
```

**Rozwiązanie:**
1. Sprawdź klucz w dashboard OpenAI: https://platform.openai.com/api-keys
2. Wygeneruj nowy klucz jeśli stary wygasł
3. Zaktualizuj w `app.yaml.secret` i wdróż ponownie

---

### Problem 3: Przekroczone limity API

**Objawy:**
```
[GPT ERROR] 429 Too Many Requests
[GPT ERROR] Rate limit exceeded
```

**Rozwiązanie:**
1. Sprawdź limity w dashboard OpenAI: https://platform.openai.com/usage
2. Poczekaj na reset limitu
3. Rozważ upgrade planu jeśli często przekraczasz limity

---

### Problem 4: GPT zwraca pustą odpowiedź

**Objawy:**
```
[GPT ERROR] Empty response from GPT API!
[FALLBACK] Using default response
```

**Rozwiązanie:**
1. Sprawdź szczegóły błędu w logach
2. Sprawdź czy `max_tokens` nie jest za małe
3. Sprawdź czy model jest dostępny

---

## 📊 PRZYKŁADOWE LOGI (PRAWIDŁOWE DZIAŁANIE)

```
[GPT FLOW] No FAQ match for: Cześć, chcę wycenę mieszkania 50m²... - attempting GPT call
[GPT FLOW] OpenAI client available - calling GPT API for: Cześć, chcę wycenę mieszkania 50m²...
[OpenAI GPT] Przetwarzanie: Cześć, chcę wycenę mieszkania 50m²...
[OpenAI GPT] Response received: Dziękuję za pytanie! Przy 50m² w standardzie komfort...
[GPT COST] Input: 245, Output: 89, Total: 334
```

---

## 📊 PRZYKŁADOWE LOGI (PROBLEM)

```
[GPT FLOW] No FAQ match for: Cześć, chcę wycenę mieszkania 50m²... - attempting GPT call
[WARNING] ensure_openai_client() returned None - trying direct initialization...
[ERROR] OPENAI_API_KEY is NOT SET in environment!
[ERROR] Direct get_openai_client() also returned None!
[FALLBACK] Using default response (no client): Dziękuję za wiadomość! Jak mogę pomóc...
```

---

## ✅ CHECKLISTA DIAGNOSTYKI

- [ ] Sprawdź czy `OPENAI_API_KEY` jest w `app.yaml.secret`
- [ ] Sprawdź logi w GCP Console
- [ ] Sprawdź czy klient jest inicjalizowany
- [ ] Sprawdź czy GPT jest wywoływane
- [ ] Sprawdź czy odpowiedź jest otrzymywana
- [ ] Sprawdź czy fallback jest używany i dlaczego
- [ ] Sprawdź limity API w dashboard OpenAI
- [ ] Sprawdź czy API key jest ważny

---

**Data utworzenia:** 12 grudnia 2025  
**Status:** ✅ Gotowe do diagnostyki

