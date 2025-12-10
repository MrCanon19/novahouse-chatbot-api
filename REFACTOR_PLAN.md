# Plan Refaktoryzacji - Architektura Chatbota

Data: 2025-12-07

Cel: Rozplątanie logiki biznesowej z warstwy API, poprawa modułowości i ułatwienie dalszego rozwoju systemu.

Poniższy plan opisuje kroki niezbędne do naprawy krytycznych problemów architektonicznych zidentyfikowanych w pliku `AUDIT.md`.

---

## Faza 1: Oczyszczenie `src/routes/chatbot.py` i Stworzenie Nowych Serwisów

Celem tej fazy jest całkowite przeniesienie logiki biznesowej z pliku `src/routes/chatbot.py` do dedykowanych serwisów w `src/services/`.

### Krok 1: Stworzenie nowych plików serwisów

Należy utworzyć następujące puste pliki w `src/services/`:

-   `faq_service.py` - Do obsługi zapytań FAQ.
-   `lead_service.py` - Do zarządzania leadami (tworzenie, scoring, podsumowania).
-   `recommendation_service.py` - Do rekomendowania pakietów i akcji.
-   `prompt_service.py` (lub `prompt_builder.py`) - Do dynamicznego budowania promptów dla AI.
-   `competitor_service.py` - Do analizy konkurencji.

### Krok 2: Przeniesienie konfiguracji promptów

1.  Utworzyć plik `src/config/prompts.py`.
2.  Przenieść gigantyczną zmienną `SYSTEM_PROMPT` z `src/routes/chatbot.py` do `src/config/prompts.py`.
3.  W przyszłości, inne statyczne dane (np. pakiety, ceny) również powinny trafić do plików konfiguracyjnych lub bazy danych, aby uniezależnić je od kodu.

### Krok 3: Migracja funkcji z `chatbot.py` do `faq_service.py`

1.  Przenieść funkcje `check_faq` i `check_learned_faq` do `faq_service.py`.
2.  Stworzyć klasę `FaqService` i umieścić te funkcje jako jej metody.
3.  Zaktualizować `MessageHandler`, aby importował i używał `FaqService` zamiast funkcji z `routes`.

### Krok 4: Migracja funkcji do `lead_service.py`

1.  Przenieść funkcje `calculate_lead_score`, `generate_conversation_summary`, `should_ask_for_confirmation`, `format_data_confirmation_message`, `check_data_confirmation_intent` do `lead_service.py`.
2.  Stworzyć klasę `LeadService` i umieścić te funkcje jako jej metody.
3.  Przenieść logikę tworzenia leada (obecnie wewnątrz `process_chat_message` i `_handle_confirmation`) do dedykowanej metody w `LeadService`, np. `create_lead_from_conversation`.
4.  Zaktualizować `MessageHandler`, aby korzystał z `LeadService`.

### Krok 5: Migracja funkcji do `recommendation_service.py`

1.  Przenieść funkcje `recommend_package` i `suggest_next_best_action` do `recommendation_service.py`.
2.  Stworzyć klasę `RecommendationService` i umieścić te funkcje jako jej metody.
3.  Zaktualizować kod, aby korzystał z tego serwisu.

### Krok 6: Migracja pozostałej logiki

1.  Przenieść `detect_competitive_intelligence` do `competitor_service.py`.
2.  Przenieść `generate_follow_up_question` do serwisu odpowiedzialnego za przepływ konwersacji (może to być `multi_turn_dialog.py` lub nowy `ConversationFlowService`).
3.  Usunąć starą, nieużywaną funkcję `process_chat_message` z `src/routes/chatbot.py`.
4.  Usunąć starą funkcję `extract_context` z `src/routes/chatbot.py`.

---

## Faza 2: Refaktoryzacja `MessageHandler`

Po oczyszczeniu warstwy API, należy uprościć `MessageHandler`.

### Krok 1: Uproszczenie metody `_generate_response`

1.  Zastąpić obecną drabinę `if/else` systemem opartym na intencjach.
2.  Stworzyć prosty klasyfikator intencji (może być na początku oparty na słowach kluczowych, ale w dedykowanej funkcji/klasie).
3.  Zmapować intencje na odpowiednie serwisy, np.:
    -   Intencja `REQUEST_PACKAGES` -> `faq_service.get_packages_info()`
    -   Intencja `ASK_PRICE` -> `recommendation_service.get_price_for_context()`
    -   Intencja `BOOK_MEETING` -> `booking_service.get_booking_link()`
4.  Metoda `_generate_response` powinna jedynie wywoływać odpowiedni serwis na podstawie wykrytej intencji.

### Krok 2: Odchudzenie metody `process_message`

1.  Główna metoda `process_message` powinna działać jak orkiestrator. Jej zadaniem jest wywoływanie kolejnych kroków (serwisów) w odpowiedniej kolejności:
    -   `spam_service.check()`
    -   `conversation_service.get_or_create()`
    -   `context_service.extract_and_validate()`
    -   `intent_classifier.get_intent()`
    -   `response_generator.generate()` (który woła odpowiedni serwis)
    -   `lead_service.try_create_lead()`
    -   ...i tak dalej.
2.  Cała logika powinna znajdować się wewnątrz tych serwisów, a nie w `process_message`.

---

## Faza 3: Długoterminowe Ulepszenia

1.  **Repozytoria:** Wprowadzić wzorzec Repozytorium, aby oddzielić logikę serwisów od bezpośrednich zapytań do bazy danych (`db.session`, `Model.query`). Serwisy powinny komunikować się z bazą danych poprzez repozytoria (np. `LeadRepository`).
2.  **Kontenery DI:** Rozważyć użycie kontenera wstrzykiwania zależności (Dependency Injection), aby zarządzać tworzeniem i cyklem życia serwisów, co jeszcze bardziej zmniejszy powiązania między nimi.
3.  **Zarządzanie Konfiguracją:** Przenieść wszystkie hardkodowane wartości (ceny pakietów, słowa kluczowe, progi) do plików konfiguracyjnych lub bazy danych.

---
Po wykonaniu Fazy 1 i 2, kod będzie znacznie czystszy, łatwiejszy do testowania i rozwijania. Faza 3 to krok w stronę w pełni profesjonalnej, skalowalnej architektury.
