# Integracja Chatfuel z kanałami komunikacji i systemem umawiania spotkań
## Przewodnik techniczny

## Spis treści
1. [Integracja ze stroną internetową](#integracja-ze-stroną-internetową)
2. [Integracja z Instagram](#integracja-z-instagram)
3. [Integracja z WhatsApp](#integracja-z-whatsapp)
4. [Implementacja funkcji umawiania spotkań](#implementacja-funkcji-umawiania-spotkań)
5. [Mechanizm przekierowania do specjalisty](#mechanizm-przekierowania-do-specjalisty)
6. [Testowanie integracji](#testowanie-integracji)
7. [Najlepsze praktyki](#najlepsze-praktyki)

## Integracja ze stroną internetową

### Wymagania wstępne
- Dostęp do panelu administracyjnego strony internetowej NovaHouse
- Konto Chatfuel Business z modułem Fuely AI
- Uprawnienia do edycji kodu strony lub instalacji wtyczek

### Kroki integracji

#### 1. Konfiguracja widgetu Chatfuel
1. Zaloguj się do panelu Chatfuel Business
2. Przejdź do sekcji "Channels" > "Website"
3. Skonfiguruj wygląd widgetu:
   - Kolor główny: zgodny z CI NovaHouse
   - Ikona: logo NovaHouse lub standardowa ikona czatu
   - Tekst powitalny: "Witaj! Jak możemy Ci pomóc?"
   - Pozycja: prawy dolny róg
4. Skonfiguruj zachowanie widgetu:
   - Automatyczne powitanie po 5 sekundach
   - Dźwięk powiadomień: włączony
   - Tryb mobilny: zoptymalizowany

#### 2. Wygenerowanie kodu widgetu
1. Po konfiguracji, kliknij "Generate Code"
2. Skopiuj wygenerowany kod JavaScript

#### 3. Implementacja na stronie NovaHouse
**Dla WordPress:**
1. Zaloguj się do panelu WordPress
2. Przejdź do "Appearance" > "Theme Editor" lub użyj wtyczki "Insert Headers and Footers"
3. Wklej kod Chatfuel przed zamykającym tagiem `</body>`
4. Zapisz zmiany

**Dla innych CMS:**
1. Zidentyfikuj plik szablonu zawierający stopkę strony
2. Wklej kod Chatfuel przed zamykającym tagiem `</body>`
3. Zapisz zmiany i odśwież pamięć podręczną

#### 4. Testowanie integracji
1. Otwórz stronę NovaHouse w trybie incognito
2. Sprawdź, czy widget pojawia się poprawnie
3. Przetestuj interakcje z chatbotem
4. Sprawdź działanie na urządzeniach mobilnych

### Zaawansowana konfiguracja
- **Personalizacja na podstawie URL:** Różne powitania dla różnych podstron
- **Integracja z Google Analytics:** Śledzenie konwersji z chatbota
- **Tryb niewidoczny na wybranych podstronach:** Konfiguracja wykluczeń

## Integracja z Instagram

### Wymagania wstępne
- Konto Instagram Business
- Konto Facebook Business Manager
- Strona firmowa na Facebooku połączona z kontem Instagram
- Uprawnienia administratora do konta Instagram i Facebook

### Kroki integracji

#### 1. Konfiguracja Facebook Business Manager
1. Zaloguj się do Facebook Business Manager
2. Przejdź do "Settings" > "Business Assets"
3. Upewnij się, że strona Facebook i konto Instagram są dodane jako zasoby
4. Przydziel odpowiednie uprawnienia

#### 2. Połączenie Chatfuel z Facebook
1. Zaloguj się do panelu Chatfuel Business
2. Przejdź do sekcji "Channels" > "Instagram"
3. Kliknij "Connect Facebook Page"
4. Wybierz stronę Facebook powiązaną z kontem Instagram NovaHouse
5. Zaakceptuj wymagane uprawnienia

#### 3. Konfiguracja automatycznych odpowiedzi
1. W panelu Chatfuel, przejdź do "Flows"
2. Utwórz nowy flow dla Instagram lub zmodyfikuj istniejący
3. Skonfiguruj:
   - Automatyczną odpowiedź powitalną
   - Flow dla najczęstszych pytań
   - Opcję umawiania spotkań
   - Mechanizm przekierowania do konsultanta

#### 4. Testowanie integracji
1. Wyślij wiadomość testową do konta Instagram NovaHouse
2. Sprawdź, czy chatbot odpowiada prawidłowo
3. Przetestuj różne scenariusze konwersacji

### Zaawansowana konfiguracja
- **Comment-to-DM:** Automatyczne odpowiedzi na komentarze z przekierowaniem do wiadomości prywatnych
- **Story Mentions:** Automatyczne odpowiedzi na wzmianki w relacjach
- **Kampanie reklamowe:** Integracja z reklamami Instagram

## Integracja z WhatsApp

### Wymagania wstępne
- Numer telefonu firmowego do WhatsApp Business
- Konto WhatsApp Business API (nie zwykłe konto WhatsApp Business)
- Weryfikacja firmy przez Meta Business
- Konto Chatfuel Business z modułem Fuely AI

### Kroki integracji

#### 1. Konfiguracja WhatsApp Business API
1. Złóż wniosek o dostęp do WhatsApp Business API przez Meta Business Manager
2. Przejdź proces weryfikacji firmy (wymagane dokumenty firmowe)
3. Skonfiguruj profil firmowy:
   - Nazwa firmy
   - Opis działalności
   - Adres
   - Godziny pracy
   - Kategoria biznesowa

#### 2. Połączenie Chatfuel z WhatsApp
1. Zaloguj się do panelu Chatfuel Business
2. Przejdź do sekcji "Channels" > "WhatsApp"
3. Kliknij "Connect WhatsApp Business"
4. Postępuj zgodnie z instrukcjami, aby połączyć konto WhatsApp Business API

#### 3. Konfiguracja szablonów wiadomości
1. W panelu Chatfuel, przejdź do "Templates"
2. Utwórz szablony wiadomości dla:
   - Powitania
   - Potwierdzenia spotkania
   - Przypomnienia o spotkaniu
   - Przekierowania do konsultanta
3. Prześlij szablony do zatwierdzenia przez Meta (proces może trwać 24-48h)

#### 4. Konfiguracja automatycznych odpowiedzi
1. W panelu Chatfuel, przejdź do "Flows"
2. Utwórz nowy flow dla WhatsApp lub zmodyfikuj istniejący
3. Skonfiguruj:
   - Automatyczną odpowiedź powitalną
   - Flow dla najczęstszych pytań
   - Opcję umawiania spotkań
   - Mechanizm przekierowania do konsultanta

#### 5. Testowanie integracji
1. Wyślij wiadomość testową na numer WhatsApp Business NovaHouse
2. Sprawdź, czy chatbot odpowiada prawidłowo
3. Przetestuj różne scenariusze konwersacji
4. Sprawdź działanie zatwierdzonych szablonów

### Zaawansowana konfiguracja
- **Katalog produktów:** Integracja z katalogiem produktów/usług
- **Płatności:** Integracja z systemem płatności (jeśli dostępne)
- **Rich Media:** Konfiguracja wysyłania zdjęć, filmów i dokumentów

## Implementacja funkcji umawiania spotkań

### Wymagania wstępne
- Konto Google Calendar dla NovaHouse
- Dostęp do API Google Calendar
- Konto Chatfuel Business z modułem Fuely AI
- Informacje o dostępności konsultantów

### Kroki implementacji

#### 1. Konfiguracja Google Calendar
1. Utwórz dedykowany kalendarz dla spotkań chatbota
2. Skonfiguruj godziny dostępności konsultantów
3. Utwórz projekt w Google Cloud Platform
4. Włącz API Google Calendar
5. Wygeneruj klucze API

#### 2. Integracja Chatfuel z Google Calendar
1. Zaloguj się do panelu Chatfuel Business
2. Przejdź do sekcji "Integrations" > "Google Calendar"
3. Wprowadź klucze API
4. Wybierz dedykowany kalendarz
5. Skonfiguruj parametry spotkań:
   - Domyślna długość spotkania
   - Minimalny czas wyprzedzenia
   - Przerwy między spotkaniami

#### 3. Konfiguracja flow umawiania spotkań
1. W panelu Chatfuel, przejdź do "Flows"
2. Utwórz nowy flow "Umów spotkanie"
3. Skonfiguruj sekwencję kroków:
   - Pytanie o cel spotkania
   - Wybór preferowanej daty
   - Wybór preferowanej godziny
   - Potwierdzenie danych kontaktowych
   - Podsumowanie i potwierdzenie

#### 4. Konfiguracja powiadomień
1. Skonfiguruj powiadomienia email dla klienta:
   - Potwierdzenie rezerwacji
   - Przypomnienie 24h przed spotkaniem
   - Przypomnienie 1h przed spotkaniem
2. Skonfiguruj powiadomienia dla konsultanta:
   - Nowe spotkanie
   - Przypomnienie o spotkaniu

#### 5. Implementacja funkcji zmiany/odwołania spotkania
1. Utwórz flow "Zmień/odwołaj spotkanie"
2. Zaimplementuj weryfikację klienta (email/telefon)
3. Skonfiguruj opcje:
   - Podgląd zaplanowanych spotkań
   - Zmiana terminu
   - Odwołanie spotkania
4. Skonfiguruj powiadomienia o zmianach

#### 6. Testowanie funkcji umawiania spotkań
1. Przetestuj cały proces umawiania spotkania
2. Sprawdź, czy spotkanie pojawia się w Google Calendar
3. Sprawdź, czy powiadomienia są wysyłane prawidłowo
4. Przetestuj funkcje zmiany i odwołania spotkania

### Zaawansowana konfiguracja
- **Inteligentne dopasowanie terminów:** Wykorzystanie Fuely AI do sugerowania optymalnych terminów
- **Personalizacja spotkań:** Dostosowanie długości spotkania do tematu
- **Integracja z CRM:** Automatyczne tworzenie leadów w monday.com

## Mechanizm przekierowania do specjalisty

### Wymagania wstępne
- Lista konsultantów z danymi kontaktowymi
- Zasady przydzielania zapytań
- Konto Chatfuel Business z modułem Fuely AI

### Kroki implementacji

#### 1. Konfiguracja bazy konsultantów
1. W panelu Chatfuel, przejdź do "Settings" > "Team"
2. Dodaj konsultantów:
   - Imię i nazwisko
   - Email
   - Telefon
   - Specjalizacja
   - Godziny dostępności

#### 2. Konfiguracja warunków przekierowania
1. W panelu Chatfuel, przejdź do "Flows"
2. Zidentyfikuj punkty, w których może być potrzebne przekierowanie:
   - Brak odpowiedzi w bazie wiedzy
   - Złożone pytania wymagające konsultacji
   - Wyraźna prośba klienta o rozmowę z konsultantem
3. Skonfiguruj warunki przekierowania:
   - Próg pewności AI (np. <70%)
   - Słowa kluczowe (np. "konsultant", "człowiek")
   - Liczba nieudanych odpowiedzi (np. 3)

#### 3. Implementacja formularza zbierania danych
1. Utwórz flow "Przekierowanie do konsultanta"
2. Zaimplementuj zbieranie danych:
   - Imię i nazwisko
   - Email
   - Telefon
   - Temat zapytania
   - Preferowany sposób kontaktu

#### 4. Konfiguracja powiadomień dla konsultantów
1. Skonfiguruj powiadomienia email dla konsultantów
2. Skonfiguruj powiadomienia SMS (opcjonalnie)
3. Skonfiguruj integrację z monday.com (tworzenie zadań)

#### 5. Implementacja mechanizmu przydzielania zapytań
1. Zaimplementuj logikę przydzielania:
   - Według specjalizacji
   - Według dostępności
   - Według obciążenia
   - Rotacyjnie

#### 6. Testowanie mechanizmu przekierowania
1. Przetestuj różne scenariusze przekierowania
2. Sprawdź, czy powiadomienia są wysyłane prawidłowo
3. Sprawdź, czy zadania są tworzone w monday.com

### Zaawansowana konfiguracja
- **Live chat:** Integracja z systemem live chat dla natychmiastowej obsługi
- **Priorytetyzacja zapytań:** Automatyczna ocena pilności zapytania
- **Analiza sentymentu:** Priorytetyzacja zapytań z negatywnym sentymentem

## Testowanie integracji

### Testy funkcjonalne
1. **Test widgetu na stronie:**
   - Poprawne wyświetlanie na różnych przeglądarkach
   - Poprawne wyświetlanie na urządzeniach mobilnych
   - Działanie automatycznego powitania
   - Działanie dźwięków powiadomień

2. **Test integracji z Instagram:**
   - Odpowiedzi na wiadomości prywatne
   - Odpowiedzi na komentarze (jeśli skonfigurowano)
   - Działanie flow konwersacji

3. **Test integracji z WhatsApp:**
   - Odpowiedzi na wiadomości
   - Działanie zatwierdzonych szablonów
   - Działanie flow konwersacji

4. **Test funkcji umawiania spotkań:**
   - Cały proces umawiania spotkania
   - Tworzenie wydarzeń w Google Calendar
   - Wysyłanie powiadomień
   - Zmiana/odwołanie spotkania

5. **Test mechanizmu przekierowania:**
   - Różne scenariusze przekierowania
   - Zbieranie danych kontaktowych
   - Powiadomienia dla konsultantów
   - Tworzenie zadań w monday.com

### Testy wydajnościowe
1. **Test obciążeniowy:**
   - Symulacja wielu równoczesnych rozmów
   - Pomiar czasu odpowiedzi
   - Identyfikacja wąskich gardeł

2. **Test długotrwały:**
   - Monitorowanie działania przez 24h
   - Sprawdzenie stabilności integracji
   - Identyfikacja potencjalnych problemów z pamięcią

### Testy użyteczności
1. **Test z udziałem zespołu NovaHouse:**
   - Ocena intuicyjności interfejsu
   - Ocena jakości odpowiedzi
   - Identyfikacja obszarów do poprawy

2. **Test z udziałem potencjalnych klientów:**
   - Ocena satysfakcji z interakcji
   - Identyfikacja punktów tarcia
   - Zbieranie sugestii usprawnień

## Najlepsze praktyki

### Strona internetowa
- Umieść widget w prawym dolnym rogu (standardowa lokalizacja)
- Skonfiguruj automatyczne powitanie po 5-10 sekundach
- Dostosuj kolory do identyfikacji wizualnej NovaHouse
- Zoptymalizuj widget dla urządzeń mobilnych

### Instagram
- Używaj krótkich, zwięzłych odpowiedzi
- Implementuj przyciski szybkich odpowiedzi
- Wykorzystuj emoji dla zwiększenia zaangażowania
- Skonfiguruj automatyczne odpowiedzi na komentarze

### WhatsApp
- Przygotuj szablony dla wszystkich typów komunikacji
- Używaj formatowania tekstu (pogrubienie, kursywa)
- Wykorzystuj listy wypunktowane
- Przygotuj odpowiedzi z załącznikami (zdjęcia, PDF)

### Umawianie spotkań
- Ogranicz liczbę kroków do maksymalnie 5
- Oferuj sugestie terminów zamiast otwartych pytań
- Wysyłaj przypomnienia 24h i 1h przed spotkaniem
- Umożliw łatwą zmianę/odwołanie spotkania

### Przekierowanie do specjalisty
- Jasno komunikuj, kiedy rozmowa jest przekierowywana
- Zbieraj tylko niezbędne dane kontaktowe
- Informuj o oczekiwanym czasie odpowiedzi
- Zapewnij mechanizm follow-up

---

Przygotował: Michał Marini  
Data: 8 lipca 2025
