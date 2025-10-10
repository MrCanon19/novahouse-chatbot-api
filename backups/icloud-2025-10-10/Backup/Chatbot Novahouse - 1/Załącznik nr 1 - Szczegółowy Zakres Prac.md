# Załącznik nr 1 - Szczegółowy Zakres Prac

## 1. Konfiguracja środowiska deweloperskiego Dialogflow

### 1.1. Utworzenie projektu Google Cloud Platform
- Utworzenie nowego projektu GCP o nazwie "Novabot"
- Aktywacja API Dialogflow
- Konfiguracja płatności i budżetu
- Ustawienie alertów kosztowych (50%, 75%, 90% budżetu)

### 1.2. Konfiguracja agenta Dialogflow
- Utworzenie nowego agenta Dialogflow ES
- Ustawienie języka polskiego jako podstawowego
- Konfiguracja strefy czasowej (Europe/Warsaw)
- Ustawienie parametrów ML (Machine Learning)

### 1.3. Konfiguracja dostępów
- Utworzenie kont deweloperskich dla zespołu
- Przyznanie odpowiednich uprawnień
- Konfiguracja Service Account
- Zabezpieczenie dostępów

## 2. Import i konfiguracja danych treningowych

### 2.1. Przygotowanie danych treningowych
- Konwersja przygotowanych intencji do formatu Dialogflow
- Przygotowanie plików JSON z intencjami
- Przygotowanie plików JSON z encjami
- Weryfikacja poprawności danych

### 2.2. Import danych do Dialogflow
- Import intencji z przygotowanych plików
- Import encji z przygotowanych plików
- Weryfikacja poprawności importu
- Uzupełnienie brakujących przykładów

### 2.3. Konfiguracja i optymalizacja
- Konfiguracja kontekstów dla intencji
- Konfiguracja parametrów i odpowiedzi
- Implementacja odpowiedzi warunkowych
- Trenowanie modelu NLU

## 3. Integracja z WhatsApp

### 3.1. Konfiguracja WhatsApp Business API
- Rejestracja konta WhatsApp Business dla NovaHouse
- Weryfikacja konta biznesowego
- Wybór i konfiguracja dostawcy API (np. Twilio, MessageBird)
- Uzyskanie kluczy API

### 3.2. Implementacja integracji
- Utworzenie serwera pośredniczącego (middleware)
- Implementacja obsługi webhooków
- Konfiguracja mapowania wiadomości WhatsApp na zapytania Dialogflow
- Implementacja obsługi odpowiedzi z Dialogflow do WhatsApp

### 3.3. Konfiguracja szablonów wiadomości
- Przygotowanie szablonów wiadomości
- Złożenie wniosku o zatwierdzenie szablonów
- Implementacja mechanizmu wyboru szablonów
- Testowanie szablonów

## 4. Integracja z Instagram

### 4.1. Konfiguracja Instagram Business
- Konfiguracja konta biznesowego na Instagramie
- Połączenie konta Instagram z Facebook Business Manager
- Konfiguracja Facebook Developer Account
- Uzyskanie niezbędnych uprawnień

### 4.2. Implementacja integracji
- Konfiguracja Facebook Messenger Platform
- Implementacja obsługi webhooków
- Konfiguracja mapowania wiadomości Instagram na zapytania Dialogflow
- Implementacja obsługi odpowiedzi z Dialogflow do Instagram

### 4.3. Konfiguracja funkcji specjalnych
- Implementacja obsługi Quick Replies
- Konfiguracja persistent menu
- Implementacja obsługi załączników
- Konfiguracja automatycznych odpowiedzi

## 5. Integracja z monday.com

### 5.1. Konfiguracja integracji
- Analiza struktury danych w monday.com
- Uzyskanie kluczy API monday.com
- Przygotowanie mapowania danych
- Konfiguracja webhooków

### 5.2. Implementacja funkcjonalności
- Implementacja automatycznego tworzenia leadów
- Konfiguracja automatycznego przypisywania zadań
- Implementacja automatycznych powiadomień
- Konfiguracja przepływów pracy

## 6. Integracja z Booksy

### 6.1. Konfiguracja integracji
- Analiza API Booksy
- Uzyskanie kluczy API
- Przygotowanie mapowania danych
- Konfiguracja dostępów

### 6.2. Implementacja funkcjonalności
- Implementacja sprawdzania dostępnych terminów
- Konfiguracja procesu rezerwacji
- Implementacja potwierdzeń i przypomnień
- Testowanie integracji

## 7. Testy funkcjonalne i wydajnościowe

### 7.1. Testy funkcjonalne
- Testowanie rozpoznawania intencji
- Testowanie odpowiedzi chatbota
- Testowanie przepływów konwersacji
- Testowanie integracji z zewnętrznymi systemami

### 7.2. Testy wydajnościowe
- Testowanie pod obciążeniem
- Testowanie czasu odpowiedzi
- Testowanie stabilności
- Identyfikacja i rozwiązanie wąskich gardeł

### 7.3. Testy użytkownika
- Przygotowanie scenariuszy testowych
- Przeprowadzenie sesji testowych z zespołem NovaHouse
- Zbieranie i analiza feedbacku
- Wprowadzenie poprawek na podstawie feedbacku

## 8. Szkolenie zespołu NovaHouse

### 8.1. Przygotowanie materiałów szkoleniowych
- Opracowanie instrukcji dla administratorów
- Przygotowanie instrukcji dla konsultantów
- Opracowanie materiałów wideo
- Przygotowanie ćwiczeń praktycznych

### 8.2. Przeprowadzenie szkoleń
- Szkolenie dla administratorów (2 dni)
- Szkolenie dla konsultantów (1 dzień)
- Warsztaty praktyczne
- Ocena efektywności szkolenia

## 9. Wdrożenie produkcyjne

### 9.1. Przygotowanie do wdrożenia
- Finalne testy przedprodukcyjne
- Przygotowanie planu wdrożenia
- Przygotowanie planu awaryjnego
- Komunikacja z zespołem i interesariuszami

### 9.2. Wdrożenie na kanałach komunikacji
- Wdrożenie na stronie internetowej
- Wdrożenie na WhatsApp
- Wdrożenie na Instagram
- Wdrożenie pozostałych integracji

### 9.3. Monitoring początkowy
- Monitoring 24/7 przez pierwszy tydzień
- Codzienna analiza logów i interakcji
- Identyfikacja i rozwiązywanie problemów
- Raportowanie statusu

## 10. Wsparcie powdrożeniowe

### 10.1. Wsparcie techniczne
- Zapewnienie wsparcia technicznego przez 4 tygodnie
- Rozwiązywanie zgłaszanych problemów
- Wprowadzanie drobnych poprawek
- Monitorowanie wydajności systemu

### 10.2. Wsparcie merytoryczne
- Konsultacje dotyczące optymalizacji bazy wiedzy
- Pomoc w interpretacji statystyk
- Doradztwo w zakresie rozwoju chatbota
- Odpowiadanie na pytania zespołu

## 11. Przekazanie projektu

### 11.1. Przygotowanie dokumentacji
- Opracowanie dokumentacji technicznej
- Przygotowanie instrukcji obsługi
- Opracowanie procedur awaryjnych
- Przygotowanie dokumentacji integracji

### 11.2. Formalne przekazanie
- Przygotowanie raportu z wdrożenia
- Przekazanie wszystkich dostępów i uprawnień
- Przekazanie kodów źródłowych i konfiguracji
- Podpisanie protokołu przekazania
