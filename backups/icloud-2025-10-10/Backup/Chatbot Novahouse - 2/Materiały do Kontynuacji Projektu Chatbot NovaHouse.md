# Materiały do Kontynuacji Projektu Chatbot NovaHouse

## 1. Podsumowanie Stanu Projektu

### 1.1. Cel Projektu
Stworzenie interaktywnego chatbota AI dla NovaHouse Sp. z o.o., który będzie odpowiadał na pytania klientów na stronie internetowej, Instagramie i WhatsAppie, a także umożliwi umawianie spotkań sprzedażowych.

### 1.2. Dotychczasowe Ustalenia i Wykonane Prace
- Przeprowadzono szczegółową analizę firmy NovaHouse i jej oferty.
- Przygotowano bazę wiedzy dla chatbota na podstawie treści ze strony novahouse.pl.
- Opracowano intencje i encje dla modelu NLU (Natural Language Understanding).
- Przygotowano przykładowe odpowiedzi chatbota.
- Opracowano scenariusze testowe dla chatbota.
- Przeprowadzono analizę porównawczą platform chatbotowych (Dialogflow, Botpress, Microsoft Bot Framework, ManyChat, Tidio, Chatfuel).
- **Kluczowa decyzja:** Wybrano platformę **Chatfuel z modułem Fuely AI** jako optymalne rozwiązanie, ze względu na:
    - Natywną funkcję AI-powered booking (umawianie spotkań).
    - Łatwą integrację multi-kanałową (strona www, Instagram, WhatsApp).
    - Szybkie wdrożenie (szacowany czas 6-8 tygodni).
    - Atrakcyjny koszt miesięczny (ok. $24/miesiąc).
- Określono priorytetowe kanały komunikacji: strona internetowa, Instagram, WhatsApp.
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

### 1.3. Kluczowe Decyzje i Rekomendacje
- **Platforma:** Chatfuel z Fuely AI - najlepsze dopasowanie do wymagań NovaHouse.
- **Priorytety:** Chatbot na stronę internetową z funkcją umawiania spotkań, następnie integracje z Instagram i WhatsApp.
- **Integracje:** Planowane integracje z Google Calendar (dla umawiania spotkań), monday.com (dla zarządzania leadami) i Booksy (dla rezerwacji usług).
- **Baza wiedzy:** Wykorzystanie istniejącej bazy wiedzy z możliwością rozszerzania.
- **Przekierowanie do specjalisty:** W przypadku braku odpowiedzi, chatbot przekieruje rozmowę do specjalisty (mechanizm do dopracowania).

## 2. Agenda Spotkania - 25 czerwca 2025, godz. 9:00

### 2.1. Powitanie i przedstawienie uczestników (5 min)
   - Krótkie przedstawienie się
   - Potwierdzenie celów spotkania

### 2.2. Status formalny projektu (10 min)
   - Potwierdzenie podpisania umowy zlecenia - stażu edukacyjnego
   - Omówienie głównych założeń umowy
   - Potwierdzenie harmonogramu realizacji (wrzesień/październik 2025)

### 2.3. Konfiguracja środowiska Dialogflow (15 min)
   - Potwierdzenie nazwy projektu "Novabot"
   - Ustalenie szczegółów dotyczących konta Google Cloud Platform:
     * Kto będzie właścicielem konta (NovaHouse czy zewnętrzny wykonawca)
     * Dane do założenia konta (adres email firmowy)
     * Omówienie ograniczeń budżetowych i opcji optymalizacji kosztów

### 2.4. Integracje z kanałami komunikacji (20 min)
   - Szczegóły dotyczące konfiguracji WhatsApp Business API:
     * Proces utworzenia profilu publicznego firmy
     * Wybór numeru telefonu do integracji
     * Szablony wiadomości do zatwierdzenia
   - Integracja z Instagramem:
     * Dostęp do konta firmowego na Instagramie
     * Połączenie z Facebook Business Manager

### 2.5. Integracje z systemami wewnętrznymi (15 min)
   - Integracja z monday.com:
     * Dostęp do API monday.com
     * Struktura danych i automatyzacje
   - Integracja z Booksy:
     * Dostęp do API Booksy
     * Zakres funkcjonalności

### 2.6. Dane treningowe i baza wiedzy (15 min)
   - Potwierdzenie zakresu przygotowanych danych treningowych
   - Ustalenie procesu aktualizacji bazy wiedzy
   - Omówienie scenariuszy konwersacji do zaimplementowania
   - Ustalenie priorytetowych funkcji chatbota

### 2.7. Proces wdrożenia i testowania (10 min)
   - Ustalenie harmonogramu testów wewnętrznych
   - Określenie grupy testerów po stronie NovaHouse
   - Proces zgłaszania i obsługi uwag
   - Kryteria akceptacji poszczególnych etapów

### 2.8. Podsumowanie i kolejne kroki (10 min)
   - Podsumowanie ustaleń
   - Określenie zadań i odpowiedzialności
   - Ustalenie terminu kolejnego spotkania

## 3. Kolejne Kroki po Spotkaniu:

1.  **Konfiguracja środowiska deweloperskiego Chatfuel** (do 10 lipca 2025):
    - Utworzenie projektu Google Cloud Platform
    - Konfiguracja agenta Chatfuel
    - Ustawienie parametrów i dostępów

2.  **Import i konfiguracja danych treningowych** (do 25 lipca 2025):
    - Import przygotowanych intencji i encji
    - Konfiguracja kontekstów i parametrów
    - Trenowanie modelu NLU

3.  **Integracja z WhatsApp i Instagram** (do 15 sierpnia 2025):
    - Konfiguracja WhatsApp Business API
    - Implementacja webhooków
    - Konfiguracja integracji z Instagramem

4.  **Integracja z monday.com i Booksy** (do 31 sierpnia 2025):
    - Implementacja integracji z monday.com
    - Konfiguracja integracji z Booksy

5.  **Testy i optymalizacja** (do 15 września 2025):
    - Przeprowadzenie testów funkcjonalnych
    - Optymalizacja odpowiedzi i przepływów
    - Testy z udziałem zespołu NovaHouse

6.  **Wdrożenie produkcyjne** (do 30 września 2025):
    - Wdrożenie na kanałach produkcyjnych
    - Monitoring początkowy
    - Wsparcie powdrożeniowe (4 tygodnie)

## 4. Pytania do Omówienia Podczas Spotkania:

1.  **Konto Google Cloud Platform:**
    - Czy NovaHouse posiada już konto firmowe Google, które można wykorzystać?
    - Kto będzie administratorem projektu po zakończeniu wdrożenia?
    - Jaki jest maksymalny miesięczny budżet na usługi Google Cloud?

2.  **WhatsApp Business:**
    - Jaki numer telefonu będzie wykorzystany do WhatsApp Business?
    - Czy firma posiada materiały potrzebne do weryfikacji konta biznesowego?
    - Jakie typy wiadomości automatycznych są priorytetowe?

3.  **Integracja z monday.com:**
    - Jaka jest obecna struktura danych w monday.com?
    - Jakie automatyzacje są już skonfigurowane?
    - Jakie dane z chatbota powinny być przekazywane do monday.com?

4.  **Integracja z Booksy:**
    - Jakie funkcje rezerwacyjne powinny być dostępne przez chatbota?
    - Czy klient ma mieć możliwość zmiany/odwołania rezerwacji przez chatbota?
    - Jak powinien wyglądać proces potwierdzania rezerwacji?

5.  **Testowanie:**
    - Kto będzie odpowiedzialny za testy po stronie NovaHouse?
    - Jakie są oczekiwania dotyczące raportowania błędów?
    - Czy firma ma preferencje dotyczące narzędzi do śledzenia błędów?

6.  **Wdrożenie:**
    - Czy wdrożenie powinno być fazowe (kanał po kanale) czy jednorazowe?
    - Jakie są oczekiwania dotyczące wsparcia powdrożeniowego?
    - Kto będzie odpowiedzialny za aktualizację bazy wiedzy po wdrożeniu?


