# Dokumentacja końcowa chatbota NovaHouse
## Instrukcja dla administratorów i użytkowników

## Spis treści
1. [Wprowadzenie](#wprowadzenie)
2. [Architektura systemu](#architektura-systemu)
3. [Panel administracyjny](#panel-administracyjny)
4. [Zarządzanie bazą wiedzy](#zarządzanie-bazą-wiedzy)
5. [Zarządzanie kanałami komunikacji](#zarządzanie-kanałami-komunikacji)
6. [Zarządzanie integracjami](#zarządzanie-integracjami)
7. [Monitorowanie i analityka](#monitorowanie-i-analityka)
8. [Rozwiązywanie problemów](#rozwiązywanie-problemów)
9. [Procedury awaryjne](#procedury-awaryjne)
10. [Rozwój i aktualizacje](#rozwój-i-aktualizacje)

## Wprowadzenie

### O chatbocie NovaHouse

Chatbot NovaHouse to inteligentny asystent oparty na platformie Chatfuel z modułem Fuely AI, zaprojektowany do obsługi klientów zainteresowanych usługami wykończenia wnętrz i budowy domów pasywnych. Chatbot działa na stronie internetowej NovaHouse oraz w kanałach Instagram i WhatsApp.

### Główne funkcje

- **Odpowiadanie na pytania klientów** - chatbot wykorzystuje bazę wiedzy do odpowiadania na pytania dotyczące oferty, pakietów wykończeniowych, procesu realizacji, cen itp.
- **Umawianie spotkań** - chatbot umożliwia klientom umawianie spotkań z konsultantami poprzez integrację z Google Calendar i Booksy
- **Przekierowanie do konsultanta** - w przypadku złożonych pytań lub na życzenie klienta, chatbot przekierowuje rozmowę do odpowiedniego konsultanta
- **Tworzenie leadów** - chatbot automatycznie tworzy leady w monday.com na podstawie rozmów z klientami
- **Wysyłanie powiadomień** - chatbot wysyła powiadomienia email i SMS do klientów i konsultantów

### Korzyści

- **Dostępność 24/7** - chatbot jest dostępny dla klientów przez całą dobę, 7 dni w tygodniu
- **Szybka odpowiedź** - chatbot odpowiada na pytania klientów natychmiast
- **Automatyzacja procesów** - chatbot automatyzuje procesy umawiania spotkań i tworzenia leadów
- **Wielokanałowość** - chatbot działa na stronie internetowej, Instagramie i WhatsAppie
- **Analityka** - chatbot dostarcza dane analityczne o rozmowach i konwersjach

## Architektura systemu

### Komponenty systemu

```
+-------------+     +----------------+     +----------------+
|             |     |                |     |                |
|  Chatfuel   +---->+  Middleware   +---->+   monday.com   |
|             |     |   (Webhook)   |     |                |
+-------------+     +----------------+     +----------------+
       |                    |
       |                    |            +----------------+
       |                    +----------->+     Booksy     |
       |                    |            |                |
       |                    |            +----------------+
       v                    |
+-------------+             |            +----------------+
|             |             +----------->+Google Calendar |
|   Fuely AI  |             |            |                |
|             |             |            +----------------+
+-------------+             |
                            |            +----------------+
                            +----------->+  Email System  |
                            |            |                |
                            |            +----------------+
                            |
                            |            +----------------+
                            +----------->+   SMS System   |
                                         |                |
                                         +----------------+
```

### Przepływ danych

1. **Klient** - inicjuje rozmowę z chatbotem poprzez stronę internetową, Instagram lub WhatsApp
2. **Chatfuel** - obsługuje rozmowę, rozpoznaje intencje i encje, generuje odpowiedzi
3. **Fuely AI** - analizuje pytania klienta i dopasowuje odpowiedzi z bazy wiedzy
4. **Middleware** - pośredniczy w komunikacji między Chatfuel a systemami zewnętrznymi
5. **Systemy zewnętrzne** - przechowują dane o leadach, spotkaniach, powiadomieniach

### Środowiska

- **Środowisko produkcyjne** - dostępne pod adresem [https://dashboard.chatfuel.com](https://dashboard.chatfuel.com)
- **Środowisko testowe** - dostępne pod adresem [https://dashboard.chatfuel.com/test](https://dashboard.chatfuel.com/test)

## Panel administracyjny

### Logowanie do panelu

1. Otwórz przeglądarkę i przejdź do [https://dashboard.chatfuel.com](https://dashboard.chatfuel.com)
2. Wprowadź dane logowania:
   - Email: `admin@novahouse.pl`
   - Hasło: `********` (dostępne w bezpiecznym repozytorium haseł NovaHouse)
3. Kliknij "Zaloguj się"

### Nawigacja po panelu

Panel administracyjny Chatfuel składa się z następujących sekcji:

- **Dashboard** - ogólny przegląd statystyk i aktywności
- **Flows** - zarządzanie przepływami konwersacji
- **AI** - zarządzanie bazą wiedzy, intencjami i encjami
- **Channels** - zarządzanie kanałami komunikacji (strona www, Instagram, WhatsApp)
- **Integrations** - zarządzanie integracjami z systemami zewnętrznymi
- **Analytics** - szczegółowe statystyki i raporty
- **Settings** - ustawienia ogólne, użytkownicy, powiadomienia

### Uprawnienia użytkowników

W systemie zdefiniowano następujące role użytkowników:

- **Administrator** - pełny dostęp do wszystkich funkcji
- **Edytor** - możliwość edycji bazy wiedzy i przepływów konwersacji
- **Analityk** - dostęp tylko do statystyk i raportów
- **Konsultant** - dostęp do rozmów przekierowanych do konsultanta

## Zarządzanie bazą wiedzy

### Struktura bazy wiedzy

Baza wiedzy chatbota NovaHouse składa się z:

- **Intencji** - reprezentują cel lub zamiar użytkownika
- **Encji** - reprezentują kluczowe informacje w wypowiedziach użytkownika
- **Odpowiedzi** - treści zwracane użytkownikowi
- **Kontekstów** - zarządzają przepływem konwersacji

### Dodawanie nowych intencji

1. Przejdź do sekcji "AI" > "Intents"
2. Kliknij "Add Intent"
3. Wprowadź nazwę intencji (np. "info_pakiet_waniliowy")
4. Dodaj przykładowe wypowiedzi (min. 15-20)
5. Skonfiguruj parametry (encje do wyodrębnienia)
6. Skonfiguruj odpowiedzi
7. Kliknij "Save"

### Dodawanie nowych encji

1. Przejdź do sekcji "AI" > "Entities"
2. Kliknij "Add Entity"
3. Wprowadź nazwę encji (np. "pakiet_wykonczeniowy")
4. Dodaj wartości encji (np. "waniliowy", "cynamonowy", "szafranowy", "pomarańczowy")
5. Dla każdej wartości, dodaj synonimy
6. Kliknij "Save"

### Aktualizacja odpowiedzi

1. Przejdź do sekcji "AI" > "Responses"
2. Wybierz odpowiedź do aktualizacji
3. Edytuj treść odpowiedzi
4. Dodaj warianty odpowiedzi dla naturalności
5. Kliknij "Save"

### Testowanie bazy wiedzy

1. Przejdź do sekcji "AI" > "Test"
2. Wprowadź przykładowe wypowiedzi użytkownika
3. Sprawdź, czy intencje są poprawnie rozpoznawane
4. Sprawdź, czy encje są poprawnie wyodrębniane
5. Sprawdź, czy odpowiedzi są poprawne

### Importowanie i eksportowanie bazy wiedzy

1. Przejdź do sekcji "AI" > "Knowledge Base"
2. Aby wyeksportować bazę wiedzy:
   - Kliknij "Export"
   - Wybierz format (JSON lub CSV)
   - Kliknij "Download"
3. Aby zaimportować bazę wiedzy:
   - Kliknij "Import"
   - Wybierz plik (JSON lub CSV)
   - Kliknij "Upload"

## Zarządzanie kanałami komunikacji

### Strona internetowa

#### Konfiguracja widgetu

1. Przejdź do sekcji "Channels" > "Website"
2. Skonfiguruj wygląd widgetu:
   - Kolor główny: `#F5A623` (pomarańczowy NovaHouse)
   - Ikona: logo NovaHouse
   - Tekst powitalny: "Witaj! Jak możemy Ci pomóc?"
   - Pozycja: prawy dolny róg
3. Skonfiguruj zachowanie widgetu:
   - Automatyczne powitanie po 5 sekundach
   - Dźwięk powiadomień: włączony
   - Tryb mobilny: zoptymalizowany
4. Kliknij "Save"

#### Instalacja widgetu na stronie

Kod widgetu jest już zainstalowany na stronie NovaHouse. W przypadku potrzeby reinstalacji:

1. Przejdź do sekcji "Channels" > "Website"
2. Kliknij "Generate Code"
3. Skopiuj wygenerowany kod JavaScript
4. Zaloguj się do panelu WordPress NovaHouse
5. Przejdź do "Appearance" > "Theme Editor" lub użyj wtyczki "Insert Headers and Footers"
6. Wklej kod przed zamykającym tagiem `</body>`
7. Zapisz zmiany

### Instagram

#### Konfiguracja Instagram

1. Przejdź do sekcji "Channels" > "Instagram"
2. Kliknij "Connect Facebook Page"
3. Wybierz stronę Facebook powiązaną z kontem Instagram NovaHouse
4. Zaakceptuj wymagane uprawnienia
5. Skonfiguruj automatyczne odpowiedzi:
   - Odpowiedź powitalna
   - Odpowiedzi na komentarze
   - Odpowiedzi na wzmianki w relacjach
6. Kliknij "Save"

#### Testowanie integracji z Instagram

1. Wyślij wiadomość na Instagram NovaHouse
2. Sprawdź, czy chatbot odpowiada
3. Sprawdź, czy odpowiedzi są poprawne
4. Sprawdź, czy przyciski szybkich odpowiedzi działają

### WhatsApp

#### Konfiguracja WhatsApp

1. Przejdź do sekcji "Channels" > "WhatsApp"
2. Kliknij "Connect WhatsApp Business"
3. Postępuj zgodnie z instrukcjami, aby połączyć konto WhatsApp Business API
4. Skonfiguruj szablony wiadomości:
   - Powitanie
   - Potwierdzenie spotkania
   - Przypomnienie o spotkaniu
   - Przekierowanie do konsultanta
5. Prześlij szablony do zatwierdzenia przez Meta
6. Kliknij "Save"

#### Testowanie integracji z WhatsApp

1. Wyślij wiadomość na numer WhatsApp Business NovaHouse
2. Sprawdź, czy chatbot odpowiada
3. Sprawdź, czy odpowiedzi są poprawne
4. Sprawdź, czy szablony wiadomości działają

## Zarządzanie integracjami

### Integracja z monday.com

#### Konfiguracja integracji

1. Przejdź do sekcji "Integrations" > "monday.com"
2. Wprowadź klucz API monday.com
3. Wybierz tablicę "Leady"
4. Mapuj pola Chatfuel do kolumn monday.com:
   - Imię i nazwisko -> Nazwa
   - Email -> Email
   - Telefon -> Telefon
   - Temat -> Temat
   - Źródło -> Źródło
   - Data spotkania -> Data spotkania
   - Godzina spotkania -> Godzina
   - Pakiet -> Pakiet
   - Status -> Status
5. Kliknij "Save"

#### Testowanie integracji

1. Przeprowadź rozmowę z chatbotem
2. Wypełnij formularz kontaktowy lub umów spotkanie
3. Sprawdź, czy lead został utworzony w monday.com
4. Sprawdź, czy wszystkie dane zostały poprawnie zmapowane

### Integracja z Booksy

#### Konfiguracja integracji

1. Przejdź do sekcji "Integrations" > "Booksy"
2. Wprowadź klucz API Booksy
3. Wybierz usługi dostępne przez chatbota
4. Wybierz pracowników dostępnych przez chatbota
5. Skonfiguruj parametry rezerwacji:
   - Domyślna długość spotkania: 60 minut
   - Minimalny czas wyprzedzenia: 24 godziny
   - Przerwy między spotkaniami: 15 minut
6. Kliknij "Save"

#### Testowanie integracji

1. Przeprowadź rozmowę z chatbotem
2. Przejdź przez proces umawiania spotkania
3. Sprawdź, czy rezerwacja została utworzona w Booksy
4. Sprawdź, czy powiadomienia zostały wysłane

### Integracja z Google Calendar

#### Konfiguracja integracji

1. Przejdź do sekcji "Integrations" > "Google Calendar"
2. Wprowadź klucze API Google Calendar
3. Wybierz kalendarz dla spotkań chatbota
4. Skonfiguruj parametry spotkań:
   - Domyślna długość spotkania: 60 minut
   - Minimalny czas wyprzedzenia: 24 godziny
   - Przerwy między spotkaniami: 15 minut
5. Kliknij "Save"

#### Testowanie integracji

1. Przeprowadź rozmowę z chatbotem
2. Przejdź przez proces umawiania spotkania
3. Sprawdź, czy wydarzenie zostało utworzone w Google Calendar
4. Sprawdź, czy powiadomienia zostały wysłane

### Integracja z systemem powiadomień

#### Konfiguracja powiadomień email

1. Przejdź do sekcji "Integrations" > "Email"
2. Wprowadź klucz API usługi email (np. SendGrid)
3. Skonfiguruj szablony email:
   - Potwierdzenie rezerwacji
   - Przypomnienie o spotkaniu
   - Potwierdzenie kontaktu z konsultantem
4. Kliknij "Save"

#### Konfiguracja powiadomień SMS

1. Przejdź do sekcji "Integrations" > "SMS"
2. Wprowadź klucz API usługi SMS (np. Twilio)
3. Wprowadź numer telefonu nadawcy
4. Skonfiguruj szablony SMS:
   - Potwierdzenie rezerwacji
   - Przypomnienie o spotkaniu
   - Potwierdzenie kontaktu z konsultantem
5. Kliknij "Save"

## Monitorowanie i analityka

### Dashboard

Dashboard Chatfuel dostarcza ogólny przegląd statystyk i aktywności:

- Liczba rozmów
- Liczba wiadomości
- Liczba użytkowników
- Średni czas rozmowy
- Najczęstsze intencje
- Najczęstsze pytania bez odpowiedzi
- Skuteczność rozpoznawania intencji
- Konwersje (umawianie spotkań, kontakt z konsultantem)

### Raporty

Chatfuel umożliwia generowanie różnych raportów:

- **Raport aktywności** - liczba rozmów, wiadomości, użytkowników w czasie
- **Raport intencji** - najczęstsze intencje, skuteczność rozpoznawania
- **Raport konwersji** - liczba umówionych spotkań, kontaktów z konsultantem
- **Raport kanałów** - porównanie aktywności na różnych kanałach
- **Raport użytkowników** - dane demograficzne, lokalizacja, urządzenia

### Alerty

Chatfuel umożliwia konfigurację alertów:

- **Alert o błędach** - powiadomienie o błędach w działaniu chatbota
- **Alert o pytaniach bez odpowiedzi** - powiadomienie o pytaniach, na które chatbot nie zna odpowiedzi
- **Alert o przekroczeniu limitów** - powiadomienie o przekroczeniu limitów API
- **Alert o spadku skuteczności** - powiadomienie o spadku skuteczności rozpoznawania intencji

## Rozwiązywanie problemów

### Typowe problemy i rozwiązania

#### Chatbot nie odpowiada

1. Sprawdź, czy chatbot jest włączony w panelu administracyjnym
2. Sprawdź, czy kanał komunikacji jest poprawnie skonfigurowany
3. Sprawdź logi błędów w sekcji "Settings" > "Logs"
4. Sprawdź, czy nie przekroczono limitów API
5. Jeśli problem występuje tylko na stronie www, sprawdź, czy kod widgetu jest poprawnie zainstalowany

#### Chatbot nie rozpoznaje intencji

1. Sprawdź, czy intencja jest poprawnie zdefiniowana
2. Sprawdź, czy przykładowe wypowiedzi są wystarczająco różnorodne
3. Dodaj więcej przykładowych wypowiedzi
4. Sprawdź, czy nie ma konfliktu z innymi intencjami
5. Przetrenuj model AI

#### Chatbot nie wyodrębnia encji

1. Sprawdź, czy encja jest poprawnie zdefiniowana
2. Sprawdź, czy wartości encji mają wystarczająco dużo synonimów
3. Dodaj więcej synonimów
4. Sprawdź, czy encja jest poprawnie używana w intencjach
5. Przetrenuj model AI

#### Integracja z monday.com nie działa

1. Sprawdź, czy klucz API jest poprawny
2. Sprawdź, czy mapowanie pól jest poprawne
3. Sprawdź logi błędów w sekcji "Settings" > "Logs"
4. Sprawdź, czy nie przekroczono limitów API monday.com
5. Sprawdź, czy middleware jest uruchomiony i dostępny

#### Integracja z Booksy nie działa

1. Sprawdź, czy klucz API jest poprawny
2. Sprawdź, czy usługi i pracownicy są poprawnie wybrani
3. Sprawdź logi błędów w sekcji "Settings" > "Logs"
4. Sprawdź, czy nie przekroczono limitów API Booksy
5. Sprawdź, czy middleware jest uruchomiony i dostępny

### Logi błędów

Logi błędów są dostępne w sekcji "Settings" > "Logs". Zawierają one informacje o:

- Dacie i czasie błędu
- Typie błędu
- Komunikacie błędu
- Kontekście błędu (rozmowa, intencja, encja)
- Stacktrace (dla błędów technicznych)

### Kontakt z supportem

W przypadku problemów, których nie można rozwiązać samodzielnie, skontaktuj się z supportem Chatfuel:

- Email: support@chatfuel.com
- Formularz kontaktowy: [https://chatfuel.com/contact](https://chatfuel.com/contact)
- Dokumentacja: [https://docs.chatfuel.com](https://docs.chatfuel.com)

## Procedury awaryjne

### Wyłączenie chatbota

W przypadku poważnych problemów, można wyłączyć chatbota:

1. Przejdź do sekcji "Settings" > "General"
2. Przełącz przełącznik "Bot Status" na "Off"
3. Kliknij "Save"

Chatbot zostanie wyłączony na wszystkich kanałach komunikacji.

### Przywrócenie poprzedniej wersji

W przypadku problemów z nową wersją, można przywrócić poprzednią wersję:

1. Przejdź do sekcji "Settings" > "Versions"
2. Wybierz poprzednią wersję z listy
3. Kliknij "Restore"
4. Potwierdź przywrócenie

### Backup i restore

Regularne backupy są wykonywane automatycznie. Aby wykonać manualny backup:

1. Przejdź do sekcji "Settings" > "Backup"
2. Kliknij "Create Backup"
3. Wprowadź nazwę backupu
4. Kliknij "Save"

Aby przywrócić backup:

1. Przejdź do sekcji "Settings" > "Backup"
2. Wybierz backup z listy
3. Kliknij "Restore"
4. Potwierdź przywrócenie

### Plan ciągłości działania

W przypadku długotrwałej niedostępności chatbota:

1. Wyłącz chatbota na wszystkich kanałach
2. Umieść informację o tymczasowej niedostępności na stronie www
3. Przekieruj klientów do alternatywnych kanałów kontaktu (telefon, email)
4. Poinformuj zespół obsługi klienta o zwiększonym obciążeniu
5. Skontaktuj się z supportem Chatfuel

## Rozwój i aktualizacje

### Planowanie rozwoju

Rozwój chatbota NovaHouse powinien być planowany w cyklach kwartalnych:

1. Analiza danych z poprzedniego kwartału
2. Identyfikacja obszarów do poprawy
3. Priorytetyzacja funkcji do dodania
4. Planowanie zasobów i harmonogramu
5. Implementacja i testowanie
6. Wdrożenie i monitorowanie

### Aktualizacja bazy wiedzy

Baza wiedzy powinna być aktualizowana regularnie:

1. Analiza pytań bez odpowiedzi
2. Identyfikacja nowych tematów
3. Przygotowanie odpowiedzi
4. Dodanie nowych intencji i przykładowych wypowiedzi
5. Testowanie i wdrożenie

### Aktualizacja przepływów konwersacji

Przepływy konwersacji powinny być aktualizowane w miarę potrzeb:

1. Analiza danych o konwersjach
2. Identyfikacja punktów tarcia
3. Projektowanie usprawnień
4. Implementacja i testowanie
5. Wdrożenie i monitorowanie

### Aktualizacja integracji

Integracje powinny być aktualizowane w przypadku zmian w systemach zewnętrznych:

1. Monitorowanie zmian w API systemów zewnętrznych
2. Planowanie aktualizacji
3. Implementacja i testowanie
4. Wdrożenie i monitorowanie

---

Przygotował: Michał Marini  
Data: 8 lipca 2025
