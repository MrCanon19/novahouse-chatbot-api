# Specyfikacja techniczna chatbota NovaHouse

## 1. Wprowadzenie

Niniejszy dokument zawiera specyfikację techniczną dla chatbota NovaHouse, który ma zostać wdrożony do września/października 2025 roku. Specyfikacja uwzględnia wymagania biznesowe firmy oraz rekomendowaną platformę Dialogflow, z możliwością adaptacji do innych platform w przypadku zmiany decyzji.

## 2. Architektura systemu

### 2.1. Komponenty systemu

1. **Frontend chatbota**
   - Widget na stronie internetowej NovaHouse
   - Integracja z Messengerem (Facebook/Instagram)
   - Opcjonalnie: integracja z WhatsApp Business API

2. **Backend chatbota**
   - Silnik NLU (Dialogflow)
   - Serwer pośredniczący (middleware) do obsługi logiki biznesowej
   - Baza danych do przechowywania historii konwersacji i danych użytkowników

3. **Integracje**
   - Monday.com (zarządzanie leadami i zadaniami)
   - System analityczny (śledzenie wydajności chatbota)
   - Opcjonalnie: system CRM (jeśli używany poza monday.com)

### 2.2. Schemat architektury

```
+----------------+     +----------------+     +----------------+
|                |     |                |     |                |
|  Strona WWW    |     |  Facebook      |     |  Inne kanały   |
|  Widget        |     |  Messenger     |     |  (opcjonalnie) |
|                |     |                |     |                |
+-------+--------+     +-------+--------+     +-------+--------+
        |                      |                      |
        v                      v                      v
+-------+--------------------------------------+------+--------+
|                                                              |
|                   Dialogflow (NLU Engine)                    |
|                                                              |
+------------------------+-----------------------------------+-+
                         |                                   |
                         v                                   v
+------------------------+-+                 +---------------+-+
|                          |                 |                 |
|  Serwer middleware       |<--------------->|  Baza danych    |
|  (logika biznesowa)      |                 |  (konwersacje)  |
|                          |                 |                 |
+----------+---------------+                 +-----------------+
           |
           v
+----------+---------------+
|                          |
|  Monday.com API          |
|  (zarządzanie leadami)   |
|                          |
+--------------------------+
```

## 3. Wymagania techniczne

### 3.1. Wymagania sprzętowe

**Serwer middleware:**
- Procesor: min. 2 rdzenie
- RAM: min. 4 GB
- Dysk: min. 50 GB SSD
- System operacyjny: Linux (Ubuntu 22.04 LTS lub nowszy)

**Baza danych:**
- Procesor: min. 2 rdzenie
- RAM: min. 4 GB
- Dysk: min. 100 GB SSD
- System operacyjny: Linux (Ubuntu 22.04 LTS lub nowszy)

### 3.2. Wymagania programowe

**Serwer middleware:**
- Node.js (v18 lub nowszy) lub Python (v3.10 lub nowszy)
- Framework: Express.js (dla Node.js) lub FastAPI/Flask (dla Python)
- SSL/TLS dla bezpiecznej komunikacji

**Baza danych:**
- MongoDB (rekomendowane) lub PostgreSQL
- System backupu i monitoringu

**Frontend:**
- Responsywny widget chatbota kompatybilny z popularnymi przeglądarkami
- Wsparcie dla urządzeń mobilnych
- Zgodność z WCAG 2.1 (dostępność)

### 3.3. Wymagania dotyczące API

**Dialogflow API:**
- Autentykacja przez Google Cloud Service Account
- Limity zapytań dostosowane do przewidywanego ruchu

**Monday.com API:**
- Autentykacja przez token API
- Uprawnienia do tworzenia i aktualizacji elementów w odpowiednich tablicach

**Webhook API (dla integracji z zewnętrznymi systemami):**
- Endpoints RESTful
- Autentykacja przez tokeny JWT
- Rate limiting dla zabezpieczenia przed nadużyciami

## 4. Funkcjonalności chatbota

### 4.1. Podstawowe funkcjonalności

1. **Rozpoznawanie intencji użytkownika**
   - Obsługa wszystkich intencji zdefiniowanych w danych treningowych
   - Rozpoznawanie encji (pakiety, metraż, lokalizacje, itp.)
   - Obsługa kontekstu rozmowy

2. **Odpowiadanie na pytania**
   - Udzielanie informacji o pakietach wykończeniowych
   - Informowanie o cenach i rabatach
   - Wyjaśnianie procesu realizacji
   - Odpowiadanie na pytania o materiały i gwarancje

3. **Zbieranie danych kontaktowych**
   - Pozyskiwanie numeru telefonu/emaila
   - Zapisywanie preferencji klienta
   - Weryfikacja poprawności danych

4. **Przekazywanie rozmowy konsultantowi**
   - Automatyczne przekazywanie w przypadku złożonych pytań
   - Możliwość manualnego żądania rozmowy z konsultantem
   - Zapisywanie historii konwersacji dla konsultanta

### 4.2. Zaawansowane funkcjonalności

1. **Integracja z monday.com**
   - Automatyczne tworzenie leadów w monday.com
   - Aktualizacja statusu leadów na podstawie interakcji
   - Przypisywanie zadań do odpowiednich osób

2. **Personalizacja**
   - Zapamiętywanie preferencji użytkownika między sesjami
   - Dostosowywanie odpowiedzi na podstawie historii interakcji
   - Personalizacja tonu komunikacji

3. **Analityka i raportowanie**
   - Śledzenie konwersji (np. umówienie konsultacji)
   - Analiza popularnych pytań i problemów
   - Identyfikacja luk w wiedzy chatbota

4. **Wielojęzyczność**
   - Polski jako język podstawowy
   - Angielski jako język opcjonalny (w przyszłości)

## 5. Integracja z monday.com

### 5.1. Zakres integracji

1. **Automatyczne tworzenie leadów**
   - Tworzenie nowych elementów w tablicy "Leady"
   - Wypełnianie pól: imię, nazwisko, email, telefon, źródło (chatbot)
   - Dodawanie notatek z kluczowymi informacjami z rozmowy

2. **Kategoryzacja leadów**
   - Przypisywanie kategorii na podstawie zainteresowań (pakiety, domy pasywne, itp.)
   - Ustawianie priorytetu na podstawie zaawansowania rozmowy

3. **Przypisywanie zadań**
   - Tworzenie zadań dla konsultantów (kontakt z klientem)
   - Ustawianie terminów realizacji zadań
   - Powiadomienia dla odpowiednich osób

### 5.2. Wymagania techniczne integracji

1. **API monday.com**
   - Wykorzystanie GraphQL API
   - Autentykacja przez token API z odpowiednimi uprawnieniami
   - Obsługa rate limitów API

2. **Mapowanie danych**
   - Mapowanie intencji chatbota na kategorie w monday.com
   - Mapowanie encji na pola w monday.com
   - Konwersja formatu danych

3. **Obsługa błędów**
   - Mechanizm ponownych prób w przypadku niedostępności API
   - Logowanie błędów integracji
   - Powiadomienia o krytycznych błędach

## 6. Bezpieczeństwo i zgodność z przepisami

### 6.1. Ochrona danych osobowych (RODO)

1. **Zgoda użytkownika**
   - Mechanizm zbierania zgody na przetwarzanie danych
   - Informacja o celu przetwarzania danych
   - Możliwość wycofania zgody

2. **Przechowywanie danych**
   - Szyfrowanie danych osobowych w bazie danych
   - Automatyczne usuwanie danych po określonym czasie
   - Ograniczenie dostępu do danych osobowych

3. **Prawa użytkownika**
   - Możliwość eksportu danych na żądanie
   - Możliwość usunięcia danych na żądanie
   - Informowanie o przetwarzaniu danych

### 6.2. Bezpieczeństwo komunikacji

1. **Szyfrowanie**
   - Komunikacja HTTPS/SSL
   - Szyfrowanie danych w spoczynku
   - Bezpieczne przechowywanie kluczy API

2. **Autentykacja i autoryzacja**
   - Zabezpieczenie panelu administracyjnego
   - Kontrola dostępu oparta na rolach
   - Logowanie prób nieautoryzowanego dostępu

3. **Ochrona przed atakami**
   - Zabezpieczenie przed atakami DDoS
   - Ochrona przed SQL Injection
   - Walidacja danych wejściowych

## 7. Testowanie

### 7.1. Rodzaje testów

1. **Testy jednostkowe**
   - Testowanie poszczególnych komponentów systemu
   - Pokrycie testami min. 80% kodu

2. **Testy integracyjne**
   - Testowanie integracji z Dialogflow
   - Testowanie integracji z monday.com
   - Testowanie integracji z frontendem

3. **Testy wydajnościowe**
   - Testowanie pod obciążeniem (min. 100 równoczesnych użytkowników)
   - Testowanie czasu odpowiedzi (max. 2 sekundy)
   - Testowanie stabilności przy długotrwałym obciążeniu

4. **Testy użyteczności**
   - Testy z udziałem rzeczywistych użytkowników
   - Ocena jakości odpowiedzi chatbota
   - Identyfikacja problemów z interfejsem użytkownika

### 7.2. Środowiska testowe

1. **Środowisko deweloperskie**
   - Lokalne środowisko dla programistów
   - Izolowane od systemów produkcyjnych

2. **Środowisko testowe**
   - Konfiguracja zbliżona do produkcyjnej
   - Dostęp dla testerów i interesariuszy
   - Integracja z testowymi instancjami zewnętrznych systemów

3. **Środowisko przedprodukcyjne (staging)**
   - Identyczne z produkcyjnym
   - Finalne testy przed wdrożeniem
   - Testy akceptacyjne

## 8. Wdrożenie i utrzymanie

### 8.1. Strategia wdrożenia

1. **Wdrożenie fazowe**
   - Faza 1: Wdrożenie na stronie internetowej
   - Faza 2: Integracja z Facebook Messenger
   - Faza 3: Rozszerzenie o dodatkowe kanały

2. **Migracja danych**
   - Import danych treningowych
   - Konfiguracja integracji z monday.com
   - Weryfikacja poprawności migracji

3. **Uruchomienie produkcyjne**
   - Procedura uruchomienia
   - Plan awaryjny (rollback)
   - Monitoring początkowy (24/7 przez pierwszy tydzień)

### 8.2. Utrzymanie i rozwój

1. **Monitorowanie wydajności**
   - Narzędzia monitoringu (np. Prometheus, Grafana)
   - Alerty w przypadku problemów
   - Regularne przeglądy wydajności

2. **Aktualizacje**
   - Harmonogram regularnych aktualizacji
   - Procedura testowania aktualizacji
   - Zarządzanie wersjami

3. **Rozwój funkcjonalności**
   - Proces zgłaszania nowych funkcjonalności
   - Priorytetyzacja rozwoju
   - Testowanie nowych funkcjonalności

## 9. Dokumentacja

### 9.1. Dokumentacja techniczna

1. **Dokumentacja kodu**
   - Standardy dokumentacji kodu
   - Diagramy komponentów
   - Opis API

2. **Dokumentacja infrastruktury**
   - Schemat infrastruktury
   - Konfiguracja serwerów
   - Procedury backupu i odtwarzania

3. **Dokumentacja integracji**
   - Szczegółowy opis integracji z monday.com
   - Opis integracji z Dialogflow
   - Opis integracji z kanałami komunikacji

### 9.2. Dokumentacja użytkownika

1. **Instrukcja administratora**
   - Zarządzanie chatbotem
   - Konfiguracja integracji
   - Rozwiązywanie typowych problemów

2. **Instrukcja dla konsultantów**
   - Obsługa przekazanych rozmów
   - Interpretacja danych z chatbota
   - Proces eskalacji problemów

3. **FAQ dla użytkowników końcowych**
   - Najczęstsze pytania dotyczące korzystania z chatbota
   - Instrukcje dla użytkowników
   - Zgłaszanie problemów

## 10. Szacunkowe koszty i harmonogram

### 10.1. Szacunkowe koszty

1. **Koszty implementacji**
   - Analiza i projektowanie: 10,000-15,000 PLN
   - Rozwój i integracja: 20,000-30,000 PLN
   - Testowanie: 5,000-10,000 PLN
   - Wdrożenie: 5,000-10,000 PLN
   - **Razem: 40,000-65,000 PLN**

2. **Koszty miesięczne**
   - Dialogflow: 500-1,500 PLN
   - Hosting: 300-500 PLN
   - Utrzymanie i wsparcie: 1,000-2,000 PLN
   - **Razem miesięcznie: 1,800-4,000 PLN**

### 10.2. Harmonogram wdrożenia

1. **Faza przygotowawcza (2-3 tygodnie)**
   - Wybór platformy
   - Szczegółowa analiza wymagań
   - Przygotowanie środowiska deweloperskiego

2. **Faza rozwoju (6-8 tygodni)**
   - Implementacja chatbota
   - Integracja z monday.com
   - Rozwój frontendu

3. **Faza testów (2-3 tygodnie)**
   - Testy wewnętrzne
   - Testy z udziałem użytkowników
   - Poprawki i optymalizacje

4. **Faza wdrożenia (1-2 tygodnie)**
   - Wdrożenie na środowisko produkcyjne
   - Szkolenia dla zespołu
   - Monitoring początkowy

5. **Faza stabilizacji (2-4 tygodnie)**
   - Zbieranie feedbacku
   - Optymalizacje wydajności
   - Rozwiązywanie zidentyfikowanych problemów

**Całkowity czas wdrożenia: 13-20 tygodni**

## 11. Ryzyka i ich mitygacja

### 11.1. Zidentyfikowane ryzyka

1. **Jakość rozpoznawania języka naturalnego**
   - Ryzyko: Chatbot może nie rozumieć niektórych zapytań użytkowników
   - Mitygacja: Dokładne trenowanie modelu, regularne aktualizacje bazy wiedzy

2. **Problemy z integracją monday.com**
   - Ryzyko: Opóźnienia lub błędy w synchronizacji danych
   - Mitygacja: Dokładne testy integracji, mechanizmy ponownych prób

3. **Wydajność przy dużym obciążeniu**
   - Ryzyko: Spowolnienie lub awarie przy dużej liczbie użytkowników
   - Mitygacja: Testy wydajnościowe, skalowalna architektura

4. **Akceptacja przez użytkowników**
   - Ryzyko: Użytkownicy mogą preferować kontakt z człowiekiem
   - Mitygacja: Intuicyjny interfejs, łatwa opcja przejścia do konsultanta

### 11.2. Plan awaryjny

1. **Procedura rollback**
   - Kroki przywracania poprzedniej wersji
   - Kryteria decyzji o rollbacku

2. **Wsparcie techniczne**
   - Zespół wsparcia dostępny podczas wdrożenia
   - Procedury eskalacji problemów

3. **Komunikacja kryzysowa**
   - Plan komunikacji w przypadku awarii
   - Szablony komunikatów dla użytkowników

## 12. Podsumowanie

Specyfikacja techniczna przedstawia kompleksowy plan wdrożenia chatbota dla NovaHouse, z uwzględnieniem integracji z monday.com. Rekomendowane rozwiązanie oparte na Dialogflow zapewni wysoką jakość obsługi klienta przy rozsądnych kosztach wdrożenia i utrzymania. Fazowe wdrożenie pozwoli na minimalizację ryzyka i stopniowe doskonalenie rozwiązania.

Kluczowe czynniki sukcesu projektu:
1. Jakość danych treningowych (już przygotowanych)
2. Sprawna integracja z monday.com
3. Intuicyjny interfejs użytkownika
4. Odpowiednie przeszkolenie zespołu
5. Regularne aktualizacje i optymalizacje po wdrożeniu
