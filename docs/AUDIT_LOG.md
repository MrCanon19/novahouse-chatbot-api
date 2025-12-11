# Dziennik Audytu Chatbota - Wersja Początkowa

Ten dokument śledzi wszystkie problemy zidentyfikowane podczas audytu kodu chatbota, ich główne przyczyny oraz proponowane lub wdrożone poprawki.

---

| ID | Problem | Przyczyna | Poprawka | Status |
|----|---------|-----------|----------|--------|
| 1  | Monolityczna logika czatu w `process_chat_message` | Brak architektury, rozrost przez dodawanie kolejnych instrukcji `if`. | Refaktoryzacja do `ChatService` z wzorcem strategii. | Oczekuje |
| 2  | Ścisłe powiązanie (Tight Coupling) | Brak separacji odpowiedzialności; handler trasy wykonuje logikę biznesową, dostęp do danych i wywołania API. | Użycie wstrzykiwania zależności (Dependency Injection). | Oczekuje |
| 3  | Zaszyte na stałe reguły biznesowe | Proceduralny styl programowania. | Ekstrakcja reguł do osobnej konfiguracji lub dedykowanych klas strategii. | Oczekuje |
| 4  | Niespójna obsługa błędów | Dodawanie funkcji bez spójnej strategii obsługi błędów. | Scentralizowanie obsługi błędów, stworzenie dedykowanych wyjątków. | Oczekuje |
| 5  | Mieszane odpowiedzialności w punktach końcowych API | Umieszczanie wszystkiego związanego z chatbotem w jednym pliku. | Podział na osobne Blueprints/pliki (np. `admin_bp`, `rodo_bp`). | Oczekuje |
| 6  | Zaszyta na stałe baza wiedzy w `novahouse_info.py` | Najprostszy sposób na przechowywanie danych bez CMS lub bazy danych. | Przeniesienie danych (FAQ, pakiety) do plików YAML/JSON lub bazy danych. Logika kwalifikacji leadów do osobnej strategii. | Oczekuje |
| 7  | Mieszanie danych i logiki w `novahouse_info.py` | Wygoda; umieszczanie funkcji i danych w jednym miejscu. | Oddzielenie logiki prezentacji (formatowanie danych) do osobnego serwisu (`KnowledgeService`). | Oczekuje |
| 8  | Krucha ekstrakcja encji oparta na Regex | Regex jest szybkim, ale brudnym sposobem na ekstrakcję encji bez modelu NLP/NLU. | Zastąpienie w dłuższej perspektywie modelem NER (np. z użyciem LLM). Krótkoterminowo: zamiana na `ExtractionStrategy`. | Oczekuje |
| 9  | Zaszyte na stałe wzorce i logika w `extract_context_safe.py` | Najprostszy sposób implementacji. | Przeniesienie wzorców do pliku konfiguracyjnego; uczynienie logiki bardziej sterowaną danymi. | Oczekuje |
| 10 | Logika i dane mieszane w `FaqService` | Brak separacji odpowiedzialności; serwis jest odpowiedzialny za *jak* sprawdzać FAQ, ale nie za *co* to są FAQ lub *jak* odpowiadać na ogólne intencje. | Przeniesienie słów kluczowych i progów FAQ do pliku konfiguracyjnego/bazy danych. Ekstrakcja logiki wykrywania miast i generowania odpowiedzi na powitania/pakiety do dedykowanych strategii. | Oczekuje |
| 11 | Niespójne wykorzystanie bazy wiedzy w `_get_faq_response` | Wygoda i brak warstwy dostępu do wiedzy. | Wprowadzenie `KnowledgeBaseService`, który abstrahuje źródło wiedzy. | Oczekuje |
| 12 | Bezpośredni dostęp do bazy danych w `check_learned_faq` | Ścisłe powiązanie. | Wstrzykiwanie sesji bazy danych (lub `LearnedFaqRepository`) jako zależności. | Oczekuje |
| 13 | Zaszyty na stałe `SYSTEM_PROMPT` w `GptStrategy` | Wygoda i ściśle powiązana konfiguracja. | Przeniesienie `SYSTEM_PROMPT` do zewnętrznego źródła konfiguracji (np. plik YAML/JSON lub baza danych). | Oczekuje |
| 14 | Zaszyta na stałe logika leadów i reguły scoringu | Pierwotnie część monolitycznej funkcji `process_chat_message`. | Ekstrakcja do dedykowanego `LeadService` lub klas narzędziowych. Parametry scoringu ładowane z konfigurowalnego źródła. | Oczekuje |
| 15 | Bezpośrednie wywołania zewnętrznych serwisów w strategii | Oryginalna monolityczna funkcja obsługiwała je bezpośrednio. | Hermetyzacja interakcji z zewnętrznymi serwisami w dedykowanych serwisach integracyjnych (np. `MondayIntegrationService`, `NotificationService`). | Oczekuje |
