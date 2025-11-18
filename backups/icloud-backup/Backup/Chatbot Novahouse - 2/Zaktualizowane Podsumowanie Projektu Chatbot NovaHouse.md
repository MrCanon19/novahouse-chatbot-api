# Zaktualizowane Podsumowanie Projektu Chatbot NovaHouse

## 1. Kluczowe Ustalenia na podstawie Odpowiedzi Klienta:

### 1.1. Konto Google Cloud Platform:
- NovaHouse posiada jedynie Google Drive, co oznacza konieczność założenia nowego konta Google Cloud Platform.
- Michał Marini będzie administratorem projektu po zakończeniu wdrożenia.
- Maksymalny miesięczny budżet na usługi Google Cloud: do 400 zł/mc.

### 1.2. WhatsApp Business:
- Klienci NovaHouse nie komunikują się za pośrednictwem WhatsAppa; kanał ten jest wykorzystywany głównie wewnętrznie.
- Priorytet integracji z WhatsAppem zostaje obniżony. Zostanie zaimplementowana opcja wyboru komunikatora na stronie www, a WhatsApp będzie ostatnim do wdrożenia.
### 1.3. Integracja z monday.com:
- monday.com jest wykorzystywany do zarządzania wpadającymi leadami i spotkaniami.
- Integracja chatbota z monday.com będzie kluczowa dla automatyzacji procesów związanych z:
    1. Danymi zleceń i zapytań klientów - leadów, którzy wyrazili chęć kontaktu z człowiekiem.
    2. Opcją newslettera - jeżeli podadzą maila, to mogą dostawać co tydzień automatycznego maila.
    3. Umówionymi spotkaniami w kalendarzu.
### 1.4. Integracja z Booksy:
- Booksy jest używane do umawiania spotkań i integracji z kalendarzem, w tym do obsługi płatności online.
- Chatbot powinien umożliwiać umawianie spotkań i integrację z kalendarzem Booksy, z uwzględnieniem płatności online.

### 1.5. Testowanie:
- Za testy po stronie NovaHouse będą odpowiedzialni Michał Marini i Marcin z NovaHouse.
- Brak konkretnych preferencji dotyczących narzędzi do śledzenia błędów lub oczekiwań dotyczących raportowania błędów.
### 1.6. Wdrożenie:
- Wdrożenie chatbota będzie odbywać się etapami (kanał po kanale).
- Brak oczekiwań dotyczących wsparcia powdrożeniowego.
- Za aktualizację bazy wiedzy po wdrożeniu będzie odpowiedzialna NovaHouse (zaczynając od podstawowej bazy wiedzy).
## 2. Zaktualizowane Kolejne Kroki w Projekcie:

Na podstawie powyższych ustaleń, następujące kroki zostają zmodyfikowane lub potwierdzone:

1.  **Konfiguracja środowiska deweloperskiego Chatfuel i Google Cloud Platform**:
    - Utworzenie nowego konta Google Cloud Platform dla NovaHouse.
    - Konfiguracja konta Chatfuel Business.
    - Ustawienie parametrów i dostępów, z Michałem Marini jako administratorem po wdrożeniu.
    - Ustalenie i monitorowanie budżetu Google Cloud.

2.  **Import i konfiguracja danych treningowych**:
    - Import przygotowanych intencji i encji do Chatfuel.
    - Konfiguracja kontekstów i parametrów.
    - Trenowanie modelu NLU.

3.  **Integracja z monday.com i Booksy (Priorytet)**:
    - Implementacja integracji z monday.com w celu rejestrowania leadów i spotkań.
    - Konfiguracja integracji z Booksy, umożliwiająca umawianie spotkań i obsługę płatności online.

4.  **Integracja z Instagram**:
    - Konfiguracja integracji z Instagramem.

5.  **Integracja z WhatsApp (Niższy Priorytet)**:
    - Konfiguracja WhatsApp Business API (jeśli wymagane do wewnętrznych procesów).
    - Implementacja webhooków.

6.  **Testy i optymalizacja**:
    - Przeprowadzenie testów funkcjonalnych z udziałem Michała Mariniego i Marcina z NovaHouse.
    - Optymalizacja odpowiedzi i przepływów.
    - Ustalenie metody raportowania błędów.

7.  **Wdrożenie produkcyjne (Etapami)**:
    - Wdrożenie na kanałach produkcyjnych etapami (np. najpierw strona www, potem Instagram).
    - Monitoring początkowy.
    - Wsparcie powdrożeniowe.

8.  **Zarządzanie Bazą Wiedzy**:
    - Rozpoczęcie od podstawowej bazy wiedzy i jej stopniowe rozszerzanie.
    - Ustalenie osoby odpowiedzialnej za aktualizację bazy wiedzy po wdrożeniu.

## 3. Pytania do dalszego omówienia:

Pomimo uzyskanych odpowiedzi, nadal istnieją pewne kwestie, które wymagają doprecyzowania:

- **Budżet Google Cloud:** Jaki jest maksymalny miesięczny budżet na usługi Google Cloud?
- **WhatsApp Business:** Jaki numer telefonu będzie wykorzystany do WhatsApp Business? Czy firma posiada materiały potrzebne do weryfikacji konta biznesowego? Jakie typy wiadomości automatycznych są priorytetowe?
- **Integracja z monday.com:** Jaka jest obecna struktura danych w monday.com? Jakie automatyzacje są już skonfigurowane? Jakie dane z chatbota powinny być przekazywane do monday.com?
- **Integracja z Booksy:** Jakie konkretne funkcje rezerwacyjne powinny być dostępne przez chatbota? Czy klient ma mieć możliwość zmiany/odwołania rezerwacji przez chatbota? Jak powinien wyglądać proces potwierdzania rezerwacji?
- **Testowanie:** Jakie są oczekiwania dotyczące raportowania błędów? Czy firma ma preferencje dotyczące narzędzi do śledzenia błędów?
- **Wdrożenie:** Jakie są oczekiwania dotyczące wsparcia powdrożeniowego? Kto będzie odpowiedzialny za aktualizację bazy wiedzy po wdrożeniu?


