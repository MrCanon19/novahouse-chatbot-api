# Załącznik nr 1 - Szczegółowy Zakres Prac

## 1. Konfiguracja środowiska Chatfuel z modułem Fuely AI

### 1.1. Utworzenie i konfiguracja konta Chatfuel Business
- Utworzenie konta Chatfuel Business dla NovaHouse
- Konfiguracja podstawowych ustawień (nazwa, logo, dane kontaktowe)
- Konfiguracja ustawień językowych (polski jako język podstawowy)
- Konfiguracja ustawień powiadomień i alertów

### 1.2. Konfiguracja modułu Fuely AI
- Aktywacja modułu Fuely AI
- Konfiguracja parametrów AI (próg pewności, kontekst konwersacji)
- Konfiguracja ustawień uczenia maszynowego
- Testowanie podstawowej funkcjonalności AI

### 1.3. Konfiguracja środowiska deweloperskiego
- Utworzenie środowiska testowego
- Konfiguracja dostępów dla zespołu deweloperskiego
- Konfiguracja narzędzi monitorowania i debugowania
- Przygotowanie środowiska do importu danych treningowych

## 2. Import i konfiguracja danych treningowych

### 2.1. Przygotowanie danych treningowych
- Konwersja istniejącej bazy wiedzy NovaHouse do formatu Chatfuel
- Przygotowanie plików CSV/JSON z intencjami i encjami
- Przygotowanie odpowiedzi chatbota
- Przygotowanie przepływów konwersacji

### 2.2. Import danych treningowych
- Import intencji do Chatfuel
- Import encji do Chatfuel
- Import odpowiedzi do Chatfuel
- Import przepływów konwersacji do Chatfuel

### 2.3. Konfiguracja i optymalizacja bazy wiedzy
- Konfiguracja kontekstów konwersacji
- Konfiguracja parametrów rozpoznawania intencji
- Konfiguracja parametrów wyodrębniania encji
- Optymalizacja odpowiedzi chatbota

### 2.4. Testowanie i trenowanie modelu AI
- Testowanie rozpoznawania intencji
- Testowanie wyodrębniania encji
- Testowanie przepływów konwersacji
- Trenowanie modelu AI na podstawie wyników testów

## 3. Integracja z kanałami komunikacji

### 3.1. Integracja ze stroną internetową NovaHouse
- Konfiguracja widgetu Chatfuel
- Implementacja kodu JavaScript na stronie WordPress
- Konfiguracja wyglądu i zachowania widgetu
- Testowanie integracji na różnych urządzeniach i przeglądarkach

### 3.2. Integracja z Instagram
- Konfiguracja połączenia z Facebook Business Manager
- Konfiguracja połączenia z kontem Instagram NovaHouse
- Konfiguracja automatycznych odpowiedzi na wiadomości prywatne
- Konfiguracja funkcji Comment-to-DM

### 3.3. Integracja z WhatsApp Business API
- Konfiguracja połączenia z WhatsApp Business API
- Konfiguracja i zatwierdzenie szablonów wiadomości
- Konfiguracja automatycznych odpowiedzi
- Konfiguracja powiadomień i alertów

## 4. Implementacja funkcji umawiania spotkań

### 4.1. Integracja z Google Calendar
- Konfiguracja połączenia z Google Calendar API
- Konfiguracja kalendarza dla spotkań chatbota
- Konfiguracja parametrów spotkań (długość, dostępność, przerwy)
- Implementacja funkcji sprawdzania dostępności terminów

### 4.2. Konfiguracja przepływu rezerwacji
- Implementacja przepływu konwersacji dla umawiania spotkań
- Implementacja formularza rezerwacji
- Implementacja potwierdzenia rezerwacji
- Implementacja przypomnienia o spotkaniu

### 4.3. Integracja z Booksy (opcjonalnie)
- Konfiguracja połączenia z Booksy API
- Konfiguracja usług i pracowników dostępnych przez chatbota
- Implementacja funkcji rezerwacji w Booksy
- Implementacja funkcji zarządzania rezerwacjami

## 5. Integracja z monday.com i innymi systemami

### 5.1. Integracja z monday.com
- Konfiguracja połączenia z monday.com API
- Konfiguracja mapowania pól Chatfuel do kolumn monday.com
- Implementacja automatycznego tworzenia leadów
- Implementacja automatycznej aktualizacji statusów

### 5.2. Implementacja middleware
- Implementacja serwera pośredniczącego (Node.js)
- Implementacja endpointów dla Chatfuel
- Implementacja logiki biznesowej
- Implementacja obsługi błędów i monitoringu

### 5.3. Integracja z systemem powiadomień
- Konfiguracja powiadomień email (SendGrid)
- Konfiguracja powiadomień SMS (Twilio)
- Implementacja szablonów powiadomień
- Implementacja logiki wysyłania powiadomień

## 6. Testy funkcjonalne i wydajnościowe

### 6.1. Testy funkcjonalne
- Testy rozpoznawania intencji i odpowiedzi
- Testy umawiania spotkań
- Testy przekierowania do konsultanta
- Testy integracji z systemami zewnętrznymi

### 6.2. Testy wydajnościowe
- Testy obciążeniowe
- Testy limitu API
- Testy stabilności
- Testy czasu odpowiedzi

### 6.3. Testy użyteczności
- Testy z udziałem zespołu NovaHouse
- Testy z udziałem potencjalnych klientów
- Analiza wyników testów
- Implementacja usprawnień na podstawie wyników testów

### 6.4. Testy akceptacyjne
- Przygotowanie scenariuszy testów akceptacyjnych
- Przeprowadzenie testów akceptacyjnych z udziałem NovaHouse
- Analiza wyników testów
- Implementacja poprawek na podstawie wyników testów

## 7. Szkolenie i dokumentacja

### 7.1. Przygotowanie materiałów szkoleniowych
- Przygotowanie instrukcji obsługi dla administratorów
- Przygotowanie instrukcji obsługi dla konsultantów
- Przygotowanie materiałów szkoleniowych
- Przygotowanie scenariuszy ćwiczeń praktycznych

### 7.2. Przeprowadzenie szkoleń
- Szkolenie administratorów
- Szkolenie konsultantów
- Szkolenie z zarządzania bazą wiedzy
- Szkolenie z monitorowania i analizy danych

### 7.3. Przygotowanie dokumentacji końcowej
- Przygotowanie dokumentacji technicznej
- Przygotowanie dokumentacji użytkownika
- Przygotowanie dokumentacji administratora
- Przygotowanie dokumentacji integracji

## 8. Wdrożenie produkcyjne i wsparcie

### 8.1. Wdrożenie na kanałach produkcyjnych
- Wdrożenie na stronie internetowej
- Wdrożenie na Instagram
- Wdrożenie na WhatsApp
- Konfiguracja monitoringu produkcyjnego

### 8.2. Wsparcie powdrożeniowe
- Monitoring początkowy (24/7 przez pierwszy tydzień)
- Wsparcie techniczne (przez 4 tygodnie)
- Optymalizacja na podstawie danych produkcyjnych
- Rozwiązywanie problemów zgłaszanych przez użytkowników

### 8.3. Przekazanie projektu
- Przygotowanie dokumentacji przekazania
- Organizacja spotkania zamykającego
- Przekazanie wszystkich dostępów i kodów źródłowych
- Formalne zakończenie projektu
