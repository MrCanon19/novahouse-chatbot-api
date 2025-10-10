# Dokumentacja Końcowa Chatbota NovaHouse

## 1. Przegląd Projektu

Celem projektu było stworzenie inteligentnego chatbota dla firmy NovaHouse, który zautomatyzuje obsługę klienta, usprawni proces pozyskiwania leadów i zintegruje się z wewnętrznymi systemami firmy.

**Główne funkcje:**
- Odpowiadanie na pytania klientów w oparciu o bazę wiedzy
- Rozpoznawanie intencji użytkowników (NLU)
- Integracja z Monday.com w celu tworzenia leadów
- System hybrydowy (baza wiedzy + NLU)
- Wdrożenie na Google App Engine z bazą danych PostgreSQL

## 2. Architektura Systemu

- **Backend:** Flask (Python)
- **Frontend:** HTML/CSS/JavaScript (interfejs chatbota)
- **Baza danych:** PostgreSQL na Google Cloud SQL
- **Hosting:** Google App Engine
- **Integracje:**
    - Monday.com API
    - OpenAI API (oczekuje na aktywację)

## 3. Kluczowe Osiągnięcia

- **Wdrożenie i stabilność:** Aplikacja została wdrożona na Google App Engine i jest w pełni stabilna. Aktualny link do działającej aplikacji: [https://glass-core-467907-e9.ey.r.appspot.com/static/chatbot.html](https://glass-core-467907-e9.ey.r.appspot.com/static/chatbot.html)
- **Baza danych:** Skonfigurowano i połączono bazę danych PostgreSQL, która przechowuje intencje, encje, konwersacje i leady.
- **System hybrydowy:** Chatbot działa w trybie hybrydowym, wykorzystując bazę wiedzy do odpowiedzi na ogólne pytania i system NLU do rozpoznawania intencji i ekstrakcji encji.
- **Integracja z Monday.com:** Pomyślnie zintegrowano chatbota z Monday.com. Nowe zapytania o spotkanie są automatycznie tworzone jako leady w tablicy "Chat" w Monday.com.

## 4. Instrukcje Użytkowania

- **Interfejs chatbota:** Dostępny pod adresem [https://glass-core-467907-e9.ey.r.appspot.com/static/chatbot.html](https://glass-core-467907-e9.ey.r.appspot.com/static/chatbot.html)
- **Testowanie integracji z Monday.com:** Wpisz w oknie chatbota wiadomość zawierającą prośbę o umówienie spotkania oraz numer telefonu (np. "Chcę umówić spotkanie, mój telefon to 123456789"). Nowy lead powinien pojawić się w Monday.com.

## 5. Dalsze Kroki

- **Aktywacja OpenAI:** Po doładowaniu konta OpenAI, system automatycznie przełączy się na tryb AI, co umożliwi bardziej zaawansowane i elastyczne odpowiedzi.
- **Rozbudowa bazy wiedzy:** Można kontynuować rozbudowę bazy wiedzy, aby chatbot mógł odpowiadać na szerszy zakres pytań.
- **Dodawanie nowych intencji:** W miarę potrzeb można dodawać nowe intencje i encje, aby rozszerzyć funkcjonalność chatbota.

## 6. Podsumowanie

Projekt został zrealizowany z sukcesem. Chatbot NovaHouse jest w pełni funkcjonalny i gotowy do użytku. Wszystkie kluczowe wymagania zostały spełnione, a system jest stabilny i skalowalny.

