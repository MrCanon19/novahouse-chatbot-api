# Audyt Bota - Wstępna Analiza

Data: 2025-12-07

Inspektor: (40-letnie doświadczenie)

## Główne Problemy Architektoniczne

Na podstawie pierwszej inspekcji pliku `src/services/message_handler.py` zidentyfikowano następujące krytyczne problemy architektoniczne, które prowadzą do "splątanej logiki" i utrudniają rozwój oraz utrzymanie systemu.

---

### 1. Problem: Monolityczna metoda i "God Object"

- **Opis:** Główna metoda `process_message` jest monolitem o długości ponad 150 linii, który orkiestruje całym procesem przetwarzania wiadomości. Klasa `MessageHandler` stała się "Boskim Obiektem" (`God Object`), który wie o wszystkim i jest odpowiedzialny za zbyt wiele zadań – od obsługi requestów, przez logikę biznesową, aż po bezpośrednie interakcje z bazą danych i zewnętrznymi API.
- **Przyczyna:** Brak wyraźnego podziału odpowiedzialności. Logika, która powinna być rozproszona w mniejszych, wyspecjalizowanych serwisach, została skumulowana w jednej klasie.
- **Poprawka (sugerowana):**
    1.  Stworzyć nową warstwę orkiestracji (np. `ChatFlowService`), której jedynym zadaniem będzie wywoływanie kolejnych, mniejszych serwisów w odpowiedniej kolejności.
    2.  Wydzielić poszczególne kroki z `process_message` do osobnych, niezależnych klas/serwisów z jedną odpowiedzialnością (np. `SpamDetectionService`, `ContextEnrichmentService`, `LeadCreationService`).
    3.  `MessageHandler` powinien jedynie przyjmować wiadomość i przekazywać ją do serwisu orkiestrującego.

---

### 1.5. Problem: Śmietnik na logikę biznesową w warstwie API

- **Opis:** Plik `src/routes/chatbot.py` jest krytycznym przykładem anty-wzorca, gdzie logika biznesowa aplikacji została umieszczona bezpośrednio w warstwie API. Plik ten zawiera nie tylko definicje endpointów, ale również dziesiątki funkcji, które powinny znajdować się w warstwie serwisowej. Co gorsza, zawiera zduplikowaną, starszą wersję logiki przetwarzania wiadomości (`process_chat_message`).
- **Przyczyna:** Brak dyscypliny architektonicznej; dodawanie logiki tam, gdzie było najłatwiej w danym momencie, co doprowadziło do erozji struktury aplikacji.
- **Krytyczne elementy do przeniesienia z `src/routes/chatbot.py`:**
    - **Logika Biznesowa:** `recommend_package`, `calculate_lead_score`, `generate_conversation_summary`, `detect_competitive_intelligence`, `suggest_next_best_action`.
    - **Logika Konwersacji:** `check_booking_intent`, `check_learned_faq`, `check_faq`, `generate_follow_up_question`, `check_data_confirmation_intent`.
    - **Ekstrakcja Danych:** `extract_context` (stara wersja).
    - **Konfiguracja i Prompty:** `SYSTEM_PROMPT` (gigantyczny, hardkodowany string).
    - **Bezpośredni Dostęp do Bazy Danych:** Liczne wywołania `db.session` i `Model.query`.
- **Poprawka (sugerowana):**
    1.  **Totalne oczyszczenie `src/routes/chatbot.py`**: Ten plik ma zawierać **tylko** definicje endpointów (`@chatbot_bp.route(...)`).
    2.  **Utworzenie nowych serwisów**: Stworzyć dedykowane serwisy w `src/services/` dla każdej domeny logicznej (np. `FaqService`, `LeadScoringService`, `RecommendationService`).
    3.  **Przeniesienie funkcji**: Przenieść każdą z wyżej wymienionych funkcji do odpowiedniego serwisu.
    4.  **Centralizacja konfiguracji**: Przenieść `SYSTEM_PROMPT` i inne podobne dane do dedykowanego pliku konfiguracyjnego (np. `src/config/prompts.py`), skąd będą ładowane, a nie hardkodowane.

---

### 2. Problem: Odwrócona i splątana zależność (Circular Dependency)

- **Opis:** Serwis (`message_handler.py`) importuje funkcje bezpośrednio z warstwy routingu/API (`src/routes/chatbot.py`). Jest to fundamentalne złamanie zasady jednokierunkowego przepływu zależności (API -> Serwisy -> Baza danych).
- **Przyczyna:** Umieszczenie logiki biznesowej (np. `check_faq`, `generate_follow_up_question`) w pliku, który powinien jedynie obsługiwać endpointy HTTP.
- **Poprawka (sugerowana):**
    1.  Przenieść WSZYSTKIE funkcje biznesowe (takie jak `check_faq`, `recommend_package`, `calculate_lead_score` itp.) z `src/routes/chatbot.py` do odpowiednich, istniejących lub nowych serwisów w `src/services/`.
    2.  Plik `src/routes/chatbot.py` powinien jedynie zawierać definicje endpointów, które przyjmują dane wejściowe i wywołują metody z serwisów.

---

### 3. Problem: Sztywna i krucha logika generowania odpowiedzi

- **Opis:** Metoda `_generate_response` to skomplikowana drabina `if/elif/else` z twardo zakodowanymi słowami kluczowymi (np. `"tak chce"`, `"pokaż pakiety"`) i zagnieżdżonymi warunkami. Taka implementacja jest niezwykle trudna do modyfikacji i podatna na błędy przy najmniejszej zmianie sposobu wyrażania się użytkownika.
- **Przyczyna:** Próba ręcznego zarządzania przepływem konwersacji za pomocą prostych warunków zamiast użycia bardziej elastycznego mechanizmu opartego na intencjach (intents).
- **Poprawka (sugerowana):**
    1.  Wprowadzić prosty system rozpoznawania intencji (Intent Recognition). Każde zapytanie użytkownika byłoby najpierw klasyfikowane do jednej z intencji (np. `GREETING`, `REQUEST_PACKAGES`, `ASK_PRICE`, `PROVIDE_DATA`).
    2.  Zastąpić drabinę `if/else` logiką, która mapuje wykrytą intencję na odpowiednią akcję lub odpowiedź (np. wzorzec Strategy lub prosty słownik `intent -> function`).
    3.  To uprości metodę `_generate_response` i sprawi, że dodawanie nowych ścieżek dialogowych będzie znacznie łatwiejsze.

---

### 4. Problem: Mieszanie odpowiedzialności i brak spójności

- **Opis:** Klasa `MessageHandler` zawiera metody do wszystkiego: od niskopoziomowych operacji na stringach (`_levenshtein`, `_normalize_input`), przez heurystyki (`_enrich_context_with_heuristics`), aż po formatowanie odpowiedzi.
- **Przyczyna:** Brak wydzielonych modułów pomocniczych (utils) lub mniejszych serwisów.
- **Poprawka (sugerowana):**
    1.  Przenieść funkcje pomocnicze (`_levenshtein`, `_strip_accents`, `_is_greeting`) do pliku `src/utils/text_utils.py`.
    2.  Wydzielić logikę ekstrakcji danych z `_enrich_context_with_heuristics` do osobnej klasy, np. `HeuristicContextExtractor`.
    3.  Ujednolicić sposób, w jaki bot generuje odpowiedzi – zamiast wielu `return` w różnych miejscach, powinien być jeden, spójny przepływ.

---
## Następne Kroki

1.  **Szczegółowa inspekcja `src/routes/chatbot.py`** w celu zidentyfikowania całej logiki biznesowej do przeniesienia.
2.  Analiza `ConversationStateMachine` w celu zrozumienia, jak można ją lepiej zintegrować z nowym systemem opartym na intencjach.
3.  Przedstawienie planu refaktoryzacji powyższych problemów.
