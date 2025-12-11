# 🔍 AUDYT CZATU NOVA HOUSE - 11 grudnia 2025

## Format: Problem → Przyczyna → Poprawka

---

## ❌ KRYTYCZNE BŁĘDY (Blokują działanie) - ✅ NAPRAWIONE

### 1. Brakujący plik `src/config/prompts.py` ✅ NAPRAWIONE
**Problem:** Import `from src.config.prompts import SYSTEM_PROMPT` w `src/routes/chatbot.py:49` powoduje błąd `ModuleNotFoundError`
**Przyczyna:** Plik został zaplanowany w REFACTOR_PLAN.md, ale nigdy nie został utworzony
**Poprawka:** ✅ Utworzono plik `src/config/prompts.py` z SYSTEM_PROMPT zawierającym instrukcje dla GPT (7550 znaków)

### 2. Brakujący plik `src/chatbot/strategies/gpt_strategy.py` ✅ NAPRAWIONE
**Problem:** Import `from src.chatbot.strategies.gpt_strategy import GptStrategy` w `src/chatbot/services/chat_service.py:13` powoduje błąd
**Przyczyna:** Strategia GPT została zaplanowana, ale plik nie został utworzony
**Poprawka:** ✅ Utworzono plik `gpt_strategy.py` z klasą GptStrategy implementującą ChatStrategy

### 3. Podwójne wywołanie `extract_context` w `process_chat_message` ✅ NAPRAWIONE
**Problem:** W linii 366-371 `extract_context_safe` jest wywoływane, a następnie ponownie `extract_context` - może powodować nadpisywanie danych
**Przyczyna:** Brak usunięcia starego kodu podczas refaktoryzacji
**Poprawka:** ✅ Usunięto duplikat wywołania `extract_context` (linia 371)

---

## ⚠️ BŁĘDY FUNKCJONALNE

### 4. Odmiana nazwisk - tylko wołacz, brak innych przypadków
**Problem:** `PolishDeclension.decline_full_name()` zwraca tylko wołacz, ale w konwersacji potrzebne są też dopełniacz, celownik, narzędnik
**Przyczyna:** Implementacja została ograniczona tylko do wołacza
**Poprawka:** Rozszerzyć użycie `decline_full_name_cases()` w miejscach gdzie potrzebne są inne przypadki

### 5. Powitania - brak specjalnego systemu powitań
**Problem:** Powitania są wykrywane przez `intro_keywords`, ale nie ma specjalnego systemu powitań z pełną formą na start
**Przyczyna:** Brak implementacji systemu powitań zgodnie z wymaganiami
**Poprawka:** Dodać logikę wykrywania pierwszej wiadomości i użycia pełnej formy powitania z imieniem, następnie naturalnie w dalszej rozmowie

### 6. Miasta - lista nie jest kompletna
**Problem:** `PolishCities` ma 255 hardcoded miast + heurystyki dla GUS, ale może brakować niektórych miast
**Przyczyna:** Lista została ograniczona do najpopularniejszych miast
**Poprawka:** Sprawdzić czy wszystkie miasta z GUS są uwzględnione, dodać brakujące

### 7. Pamięć kontekstu - limit 10 wiadomości może być za mały
**Problem:** W linii 408 limit historii to 10 wiadomości - przy dłuższych rozmowach może być za mało kontekstu
**Przyczyna:** Ustawiony arbitralnie limit
**Poprawka:** Zwiększyć limit do 20 lub dynamicznie dostosowywać w zależności od długości rozmowy

### 8. Model GPT - domyślnie `gpt-4o-mini`, może być za słaby dla polskiego
**Problem:** Domyślny model `gpt-4o-mini` może mieć gorszą jakość odpowiedzi po polsku niż `gpt-4o`
**Przyczyna:** Wybór modelu oparty na kosztach, nie jakości
**Poprawka:** Przetestować oba modele i zalecić najlepszy dla polskiego języka

---

## 🔧 PROBLEMY ARCHITEKTURALNE

### 9. Duplikacja logiki między `process_chat_message` a `ChatService`
**Problem:** Istnieją dwie implementacje przetwarzania wiadomości - stara w `chatbot.py` i nowa w `ChatService`
**Przyczyna:** Refaktoryzacja nie została dokończona
**Poprawka:** Usunąć starą implementację `process_chat_message` z `chatbot.py` i używać tylko `ChatService`

### 10. Brak obsługi błędów w niektórych miejscach
**Problem:** Niektóre funkcje nie mają odpowiedniej obsługi błędów (np. `check_booking_intent`, `check_faq`)
**Przyczyna:** Brak defensive programming
**Poprawka:** Dodać try-except w krytycznych miejscach

### 11. TODO w kodzie - `track_ab_test_response` nie jest zaimplementowane
**Problem:** W linii 479 jest TODO dla `track_ab_test_response`, funkcja nie istnieje
**Przyczyna:** Funkcjonalność została zaplanowana, ale nie zaimplementowana
**Poprawka:** Zaimplementować funkcję lub usunąć TODO jeśli nie jest potrzebna

---

## 📝 PROBLEMY JĘZYKOWE I STYLISTYCZNE

### 12. Odmiana imion obcojęzycznych - może być niepoprawna
**Problem:** `FOREIGN_NAMES` lista może być niekompletna, niektóre obcojęzyczne imiona mogą być błędnie odmieniane
**Przyczyna:** Lista jest ograniczona
**Poprawka:** Rozszerzyć listę FOREIGN_NAMES o więcej popularnych imion obcojęzycznych

### 13. Brak obsługi literówek w imionach
**Problem:** Jeśli użytkownik napisze imię z literówką (np. "Michał" → "Michal"), system może nie rozpoznać
**Przyczyna:** Brak fuzzy matching dla imion
**Poprawka:** Dodać fuzzy matching lub normalizację dla imion

### 14. Emotikony - mogą być ignorowane lub źle interpretowane
**Problem:** System może nie uwzględniać emotikon w kontekście wiadomości
**Przyczyna:** Brak obsługi emotikon w ekstrakcji kontekstu
**Poprawka:** Dodać obsługę emotikon w `extract_context` i `extract_context_safe`

---

## 🔗 PROBLEMY INTEGRACYJNE

### 15. Monday.com - brak weryfikacji czy dane się zapisały
**Problem:** Po utworzeniu leada w Monday.com nie ma weryfikacji czy dane się faktycznie zapisały
**Przyczyna:** Brak error handling i weryfikacji odpowiedzi z API
**Poprawka:** Dodać weryfikację odpowiedzi z Monday.com API i logowanie błędów

### 16. ZenCal - brak obsługi błędów przy tworzeniu booking linku
**Problem:** Jeśli ZenCal API zwróci błąd, system może nie obsłużyć tego poprawnie
**Przyczyna:** Brak defensive programming dla integracji ZenCal
**Poprawka:** Dodać try-except i fallback dla błędów ZenCal

---

## 🧪 PROBLEMY TESTOWE

### 17. Brak testów dla sytuacji nietypowych
**Problem:** Nie ma testów dla sprzecznych danych, zmiany decyzji, brakujących danych
**Przyczyna:** Testy skupiają się na happy path
**Poprawka:** Dodać testy dla edge cases i sytuacji nietypowych

### 18. Brak testów dla różnych stylów pisania
**Problem:** Nie ma testów sprawdzających reakcje na literówki, emotikony, mieszanie języków
**Przyczyna:** Brak kompleksowych testów językowych
**Poprawka:** Dodać testy dla różnych stylów pisania i języków

---

## 💰 PROBLEMY KOSZTOWE

### 19. Brak monitorowania kosztów API
**Problem:** Nie ma systemu monitorowania kosztów użycia OpenAI API
**Przyczyna:** Brak implementacji trackingu kosztów
**Poprawka:** Dodać logging kosztów każdego requestu do OpenAI

### 20. Model może być nieoptymalny pod względem kosztów
**Problem:** `gpt-4o-mini` jest tańszy, ale może wymagać więcej tokenów dla dobrych odpowiedzi
**Przyczyna:** Brak analizy kosztów vs jakości
**Poprawka:** Przeprowadzić analizę kosztów różnych modeli i zalecić optymalny

---

## 📊 PODSUMOWANIE

**Krytyczne błędy:** 3 (blokują działanie)
**Błędy funkcjonalne:** 5
**Problemy architektoniczne:** 3
**Problemy językowe:** 3
**Problemy integracyjne:** 2
**Problemy testowe:** 2
**Problemy kosztowe:** 2

**RAZEM:** 20 problemów do naprawy

---

## 🎯 PRIORYTETY NAPRAWY

1. **PRIORYTET 1 (KRYTYCZNE):** Naprawić brakujące pliki (prompts.py, gpt_strategy.py)
2. **PRIORYTET 2 (WYSOKIE):** Naprawić duplikację extract_context, dodać obsługę błędów
3. **PRIORYTET 3 (ŚREDNIE):** Rozszerzyć odmianę nazwisk, poprawić system powitań
4. **PRIORYTET 4 (NISKIE):** Dodać testy, monitoring kosztów, rozszerzyć listy

