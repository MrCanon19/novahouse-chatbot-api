# Ogólny Przegląd Projektu Chatbot NovaHouse

## 1. Cel Projektu
Stworzenie interaktywnego chatbota AI dla NovaHouse Sp. z o.o., który będzie odpowiadał na pytania klientów na stronie internetowej, Instagramie i WhatsAppie, a także umożliwi umawianie spotkań sprzedażowych.

## 2. Kluczowe Decyzje i Rekomendacje
- **Platforma:** Chatfuel z modułem Fuely AI - najlepsze dopasowanie do wymagań NovaHouse ze względu na natywną funkcję AI-powered booking, łatwą integrację multi-kanałową, szybkie wdrożenie i atrakcyjny koszt.
- **Priorytety:** Chatbot na stronę internetową z funkcją umawiania spotkań, następnie integracje z Instagram i WhatsApp.
- **Integracje:** Planowane integracje z Google Calendar (dla umawiania spotkań), monday.com (dla zarządzania leadami) i Booksy (dla rezerwacji usług).
- **Baza wiedzy:** Wykorzystanie istniejącej bazy wiedzy z możliwością rozszerzania.
- **Przekierowanie do specjalisty:** W przypadku braku odpowiedzi, chatbot przekieruje rozmowę do specjalisty (mechanizm do dopracowania).

## 3. Co jest zrobione, a co nie (Status Projektu)

### 3.1. Wykonane Prace (Zrobione):
- Przeprowadzono szczegółową analizę firmy NovaHouse i jej oferty.
- Przygotowano bazę wiedzy dla chatbota na podstawie treści ze strony novahouse.pl.
- Opracowano intencje i encje dla modelu NLU (Natural Language Understanding).
- Przygotowano przykładowe odpowiedzi chatbota.
- Opracowano scenariusze testowe dla chatbota.
- Przeprowadzono analizę porównawczą platform chatbotowych i wybrano Chatfuel z Fuely AI.
- Podpisano umowę o zachowaniu poufności (NDA) z Michałem Marini.
- Przygotowano i podpisano umowę zlecenia - staż edukacyjny z Michałem Marini, uwzględniającą nową platformę i zakres prac.
- Przygotowano szczegółowy zakres prac (Załącznik nr 1 do umowy).
- Opracowano szczegółowy harmonogram realizacji (Załącznik nr 2 do umowy), z terminem wdrożenia produkcyjnego do 8 października 2025 r.
- Przygotowano porównanie platform chatbotowych (Załącznik nr 3 do umowy).
- Przeprowadzono analizę kompatybilności hostingu Cyber Folks WP-GO i przygotowano specyfikację techniczną hostingu (Załącznik nr 4 do umowy).
- Opracowano szczegółowy plan wdrożenia Chatfuel z Fuely AI, obejmujący 7 faz implementacji.
- Przygotowano instrukcję integracji Chatfuel z WhatsApp i Instagram.
- Przygotowano instrukcję importu i konfiguracji danych treningowych w Chatfuel.
- Przygotowano przewodnik integracji Chatfuel z monday.com, Booksy i innymi systemami zewnętrznymi.
- Opracowano szczegółowy plan testów funkcjonalnych i akceptacyjnych.
- Przygotowano kompletną dokumentację końcową i materiały szkoleniowe dla zespołu NovaHouse.

### 3.2. Do Zrobienia (Kolejne Kroki Techniczne):
Po otrzymaniu niezbędnych dostępów i informacji, będę mógł przystąpić do realizacji kolejnych faz projektu zgodnie z harmonogramem:
1.  **Konfiguracja środowiska deweloperskiego Chatfuel**:
    - Utworzenie konta Chatfuel Business
    - Konfiguracja agenta Chatfuel
    - Ustawienie parametrów i dostępów
2.  **Import i konfiguracja danych treningowych**:
    - Import przygotowanych intencji i encji do Chatfuel
    - Konfiguracja kontekstów i parametrów
    - Trenowanie modelu NLU
3.  **Integracja z WhatsApp i Instagram**:
    - Konfiguracja WhatsApp Business API
    - Implementacja webhooków
    - Konfiguracja integracji z Instagramem
4.  **Integracja z monday.com i Booksy**:
    - Implementacja integracji z monday.com
    - Konfiguracja integracji z Booksy
5.  **Testy i optymalizacja**:
    - Przeprowadzenie testów funkcjonalnych
    - Optymalizacja odpowiedzi i przepływów
    - Testy z udziałem zespołu NovaHouse
6.  **Wdrożenie produkcyjne**:
    - Wdrożenie na kanałach produkcyjnych
    - Monitoring początkowy
    - Wsparcie powdrożeniowe

## 4. Najbliższe Działania (do wykonania przez Michała Mariniego)

Kluczowym elementem do kontynuacji projektu jest zebranie niezbędnych dostępów i informacji od NovaHouse. Przygotowałem już szczegółowy formularz zbierania dostępów i informacji, który należy przekazać klientowi i uzyskać jego wypełnienie.

**Lista do przygotowania przez Pana (Michała Mariniego):**
1.  **Wypełnić formularz dostępów** z następującymi danymi:
    - Dane firmowe NovaHouse do konta Chatfuel
    - Dostępy do panelu administracyjnego strony www
    - Dostępy do kont Instagram i Facebook Business
    - Numer telefonu do WhatsApp Business
    - Klucze API do monday.com i Booksy
    - Dane konsultantów do przekierowań
    - Informacje o dostępności i harmonogramie spotkań
2.  **Zebrać materiały marketingowe**:
    - Logo firmy w wysokiej rozdzielczości
    - Zdjęcia produktów/usług
    - Materiały opisowe pakietów wykończeniowych
    - Przykładowe realizacje
3.  **Ustalić z NovaHouse**:
    - Budżet miesięczny na Chatfuel (plan Business - $23.99/miesiąc)
    - Osobę odpowiedzialną za akceptację etapów wdrożenia
    - Zespół do testów i szkoleń

## 5. Potencjalne Luki / Pytania do Klienta (do omówienia podczas spotkania)

Te pytania zostały już zidentyfikowane i zawarte w podsumowaniu projektu, ale warto je ponownie podkreślić jako potencjalne luki w informacjach, które mogą wpłynąć na płynność wdrożenia:
1.  **Konto Google Cloud Platform:**
    - NovaHouse posiada jedynie Google Drive, więc konieczne będzie założenie nowego konta Google Cloud Platform.
    - Kto będzie administratorem projektu po zakończeniu wdrożenia? (Do ustalenia)
    - Maksymalny miesięczny budżet na usługi Google Cloud: do 400 zł/mc..  **WhatsApp Business:**
    - Klienci nie komunikują się na tym kanale (bardziej wewnętrzna opcja), więc priorytet integracji z WhatsApp jest niższy.
    - Jaki numer telefonu będzie wykorzystany do WhatsApp Business? (Do ustalenia)
    - Czy firma posiada materiały potrzebne do weryfikacji konta biznesowego? (Do ustalenia)
    - Jakie typy wiadomości automatycznych są priorytetowe? (Do ustalenia)
3.  **Integracja z monday.com:**
    - Chatbot powinien integrować się z monday.com w celu rejestrowania wpadających leadów i spotkań.
    - Jaka jest obecna struktura danych w monday.com? (Do ustalenia)
    - Jakie automatyzacje są już skonfigurowane? (Do ustalenia)
    - Jakie dane z chatbota powinny być przekazywane do monday.com? (Do ustalenia)
4.  **Integracja z Booksy:**
    - Chatbot powinien umożliwiać umawianie spotkań i integrację z kalendarzem Booksy, w tym obsługę płatności online.
    - Jakie funkcje rezerwacyjne powinny być dostępne przez chatbota? (Do ustalenia)
    - Czy klient ma mieć możliwość zmiany/odwołania rezerwacji przez chatbota? (Do ustalenia)
    - Jak powinien wyglądać proces potwierdzania rezerwacji? (Do ustalenia)
5.  **Testowanie:**
    - Za testy po stronie NovaHouse będą odpowiedzialni Michał Marini i Marcin z NovaHouse.
    - Nie ma preferencji dotyczących narzędzi do śledzenia błędów ani oczekiwań dotyczących raportowania błędów (do ustalenia).
6.  **Wdrożenie:**
    - Wdrożenie powinno być fazowe (kanał po kanale).
    - Kto będzie odpowiedzialny za aktualizację bazy wiedzy po wdrożeniu? (Do ustalenia, zaczynając od podstawowej bazy wiedzy).


