# 🧪 TESTY PRZED ODDANIEM CHATBOTA KLIENTOWI

**Data:** 12 grudnia 2025  
**Status:** ✅ Gotowe do testowania

---

## ✅ CO ZOSTAŁO NAPRAWIONE

1. **Bezpieczeństwo kluczy API:**
   - ✅ Pliki z kluczami usunięte z Git
   - ✅ Logowanie tylko 4 pierwszych znaków
   - ✅ Wszystkie `print()` → `logging`

2. **Zapętlanie chatbota:**
   - ✅ Poprawiona walidacja `OPENAI_API_KEY`
   - ✅ Lepsze logowanie dla debugowania
   - ✅ Lepsze komunikaty błędów

3. **Gotowość do wdrożenia:**
   - ✅ Wszystkie zmiany zcommitowane
   - ✅ Dokumentacja bezpieczeństwa
   - ✅ Narzędzia testowe

---

## 🧪 TESTY DO WYKONANIA

### 1. Test połączenia z OpenAI API

```bash
# Lokalnie (jeśli masz klucz)
export OPENAI_API_KEY='sk-...'
python3 scripts/test_openai_connection.py
```

**Oczekiwany wynik:** ✅ Połączenie działa!

---

### 2. Test w przeglądarce

1. Otwórz chatbota w przeglądarce
2. Wyślij wiadomość testową: "Cześć, chcę wycenę mieszkania 50m²"
3. **Sprawdź:**
   - ✅ Chatbot odpowiada (nie zapętla się)
   - ✅ Odpowiedź jest różnorodna (nie zawsze ta sama)
   - ✅ Odpowiedź jest sensowna i związana z pytaniem

**Jeśli chatbot zapętla się:**
- Sprawdź logi aplikacji
- Sprawdź czy `OPENAI_API_KEY` jest ustawiony
- Sprawdź limity API w dashboard OpenAI

---

### 3. Test w produkcji (po wdrożeniu)

```bash
# Wdróż
./scripts/deploy_production.sh

# Sprawdź logi
gcloud logging read "resource.type=gae_app AND textPayload=~'GPT'" --limit 20
```

**Oczekiwane logi:**
```
[GPT] Calling OpenAI API for message: ...
[OpenAI GPT] Response received: ...
[GPT COST] Input: X, Output: Y, Total: Z
```

**Jeśli widzisz:**
```
[WARNING] OPENAI_API_KEY not set
```
→ Sprawdź czy klucz jest w `app.yaml.secret` lub GCP Secret Manager

---

### 4. Test różnych scenariuszy

**Scenariusz 1: Wycena**
- "Chcę wycenę mieszkania 50m² w Warszawie"
- ✅ Chatbot pyta o standard, zakres, lokalizację
- ✅ Podaje orientacyjną wycenę

**Scenariusz 2: Porównanie pakietów**
- "Jakie są różnice między pakietami?"
- ✅ Chatbot pokazuje porównanie pakietów

**Scenariusz 3: Pytanie ogólne**
- "Ile trwa wykończenie mieszkania?"
- ✅ Chatbot odpowiada na podstawie wiedzy

**Scenariusz 4: Zapytanie o kontakt**
- "Chcę umówić konsultację"
- ✅ Chatbot proponuje rezerwację przez Zencal

---

## 🔍 SPRAWDZENIE LOGÓW

### Lokalnie

```bash
tail -f logs/chatbot.log
```

### W produkcji (GCP)

```bash
gcloud logging read "resource.type=gae_app" --limit 50
```

**Szukaj:**
- `[GPT] Calling OpenAI API` - ✅ GPT działa
- `[WARNING] OPENAI_API_KEY` - ❌ Problem z kluczem
- `[GPT ERROR]` - ❌ Błąd API

---

## ✅ CHECKLISTA PRZED ODDANIEM

- [ ] Test połączenia z OpenAI API działa
- [ ] Chatbot odpowiada w przeglądarce (nie zapętla się)
- [ ] Odpowiedzi są różnorodne i sensowne
- [ ] Logi pokazują wywołania GPT API
- [ ] Wszystkie funkcje działają (wycena, pakiety, kontakt)
- [ ] Integracja z Monday.com działa (jeśli włączona)
- [ ] Integracja z Zencal działa (jeśli włączona)
- [ ] RODO compliance działa (usuwanie danych, eksport)

---

## 🚨 CO ZROBIĆ, GDY COŚ NIE DZIAŁA

### Chatbot się zapętla

1. Sprawdź logi aplikacji
2. Sprawdź czy `OPENAI_API_KEY` jest ustawiony
3. Sprawdź limity API w dashboard OpenAI
4. Sprawdź czy klucz API jest ważny

### Chatbot zwraca fallback

1. Sprawdź czy `OPENAI_API_KEY` jest w `app.yaml.secret`
2. Sprawdź czy klucz nie zaczyna się od `test_`
3. Sprawdź logi - powinny pokazywać przyczynę

### Błędy w produkcji

1. Sprawdź logi w GCP Console
2. Sprawdź czy wszystkie zmienne środowiskowe są ustawione
3. Sprawdź czy baza danych działa
4. Sprawdź czy wszystkie zależności są zainstalowane

---

## 📞 WSPARCIE

Jeśli potrzebujesz pomocy:
1. Sprawdź dokumentację: `docs/BEZPIECZENSTWO_SEKRETOW.md`
2. Sprawdź logi aplikacji
3. Skontaktuj się z zespołem deweloperskim

---

**Data utworzenia:** 12 grudnia 2025  
**Status:** ✅ Gotowe do testowania i oddania klientowi

