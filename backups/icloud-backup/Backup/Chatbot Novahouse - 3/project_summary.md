# Podsumowanie Stanu Projektu Chatbot NovaHouse

## 1. Cel Projektu
Stworzenie interaktywnego chatbota AI dla NovaHouse Sp. z o.o., który będzie odpowiadał na pytania klientów na stronie internetowej, Instagramie i WhatsAppie, a także umożliwi umawianie spotkań sprzedażowych.

## 2. Dotychczasowe Ustalenia i Wykonane Prace

### 2.1. Analiza i Przygotowanie Danych
- Przeprowadzono szczegółową analizę firmy NovaHouse i jej oferty.
- Przygotowano bazę wiedzy dla chatbota na podstawie treści ze strony novahouse.pl.
- Opracowano intencje i encje dla modelu NLU (Natural Language Understanding).
- Przygotowano przykładowe odpowiedzi chatbota.
- Opracowano scenariusze testowe dla chatbota.

### 2.2. Wybór Technologii
- Przeprowadzono analizę porównawczą platform chatbotowych (Dialogflow, Botpress, Microsoft Bot Framework, ManyChat, Tidio, Chatfuel).
- **Kluczowa decyzja:** Wybrano platformę **Chatfuel z modułem Fuely AI** jako optymalne rozwiązanie, ze względu na:
    - Natywną funkcję AI-powered booking (umawianie spotkań).
    - Łatwą integrację multi-kanałową (strona www, Instagram, WhatsApp).
    - Szybkie wdrożenie (szacowany czas 6-8 tygodni).
    - Atrakcyjny koszt miesięczny (ok. $24/miesiąc).
- Określono priorytetowe kanały komunikacji: strona internetowa, Instagram, WhatsApp.

### 2.3. Dokumentacja Formalna i Planowanie Wdrożenia
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

## 3. Kluczowe Decyzje i Rekomendacje
- **Platforma:** Chatfuel z Fuely AI - najlepsze dopasowanie do wymagań NovaHouse.
- **Priorytety:** Chatbot na stronę internetową z funkcją umawiania spotkań, następnie integracje z Instagram i WhatsApp.
- **Integracje:** Planowane integracje z Google Calendar (dla umawiania spotkań), monday.com (dla zarządzania leadami) i Booksy (dla rezerwacji usług).
- **Baza wiedzy:** Wykorzystanie istniejącej bazy wiedzy z możliwością rozszerzania.
- **Przekierowanie do specjalisty:** W przypadku braku odpowiedzi, chatbot przekieruje rozmowę do specjalisty (mechanizm do dopracowania).

## 4. Następne Kroki (do omówienia z klientem)
- Zebranie niezbędnych dostępów i informacji od NovaHouse (formularz dostępów).
- Utworzenie konta Chatfuel Business i rozpoczęcie 7-dniowego trialu.
- Akceptacja planu wdrożenia przez NovaHouse.
- Rozpoczęcie Fazy 1: Przygotowanie i konfiguracja (zgodnie z harmonogramem).




## 5. Pytania do omówienia podczas spotkania:

1. **Konto Google Cloud Platform:**
   - Czy NovaHouse posiada już konto firmowe Google, które można wykorzystać?
   - Kto będzie administratorem projektu po zakończeniu wdrożenia?
   - Jaki jest maksymalny miesięczny budżet na usługi Google Cloud?

2. **WhatsApp Business:**
   - Jaki numer telefonu będzie wykorzystany do WhatsApp Business?
   - Czy firma posiada materiały potrzebne do weryfikacji konta biznesowego?
   - Jakie typy wiadomości automatycznych są priorytetowe?

3. **Integracja z monday.com:**
   - Jaka jest obecna struktura danych w monday.com?
   - Jakie automatyzacje są już skonfigurowane?
   - Jakie dane z chatbota powinny być przekazywane do monday.com?

4. **Integracja z Booksy:**
   - Jakie funkcje rezerwacyjne powinny być dostępne przez chatbota?
   - Czy klient ma mieć możliwość zmiany/odwołania rezerwacji przez chatbota?
   - Jak powinien wyglądać proces potwierdzania rezerwacji?

5. **Testowanie:**
   - Kto będzie odpowiedzialny za testy po stronie NovaHouse?
   - Jakie są oczekiwania dotyczące raportowania błędów?
   - Czy firma ma preferencje dotyczące narzędzi do śledzenia błędów?

6. **Wdrożenie:**
   - Czy wdrożenie powinno być fazowe (kanał po kanale) czy jednorazowe?
   - Jakie są oczekiwania dotyczące wsparcia powdrożeniowego?
   - Kto będzie odpowiedzialny za aktualizację bazy wiedzy po wdrożeniu?


