# Materiały szkoleniowe dla zespołu NovaHouse
## Obsługa i zarządzanie chatbotem Chatfuel z modułem Fuely AI

## Spis treści
1. [Wprowadzenie](#wprowadzenie)
2. [Podstawy obsługi chatbota](#podstawy-obsługi-chatbota)
3. [Panel administracyjny](#panel-administracyjny)
4. [Zarządzanie bazą wiedzy](#zarządzanie-bazą-wiedzy)
5. [Zarządzanie kanałami komunikacji](#zarządzanie-kanałami-komunikacji)
6. [Zarządzanie integracjami](#zarządzanie-integracjami)
7. [Monitorowanie i analityka](#monitorowanie-i-analityka)
8. [Rozwiązywanie problemów](#rozwiązywanie-problemów)
9. [Najlepsze praktyki](#najlepsze-praktyki)
10. [Ćwiczenia praktyczne](#ćwiczenia-praktyczne)

## Wprowadzenie

### Cel szkolenia

Celem szkolenia jest przekazanie wiedzy i umiejętności niezbędnych do efektywnego zarządzania chatbotem NovaHouse opartym na platformie Chatfuel z modułem Fuely AI. Po ukończeniu szkolenia, uczestnicy będą potrafili:

- Logować się do panelu administracyjnego i nawigować po nim
- Zarządzać bazą wiedzy chatbota
- Konfigurować kanały komunikacji
- Zarządzać integracjami z systemami zewnętrznymi
- Monitorować wydajność chatbota i analizować dane
- Rozwiązywać typowe problemy
- Stosować najlepsze praktyki w zarządzaniu chatbotem

### Agenda szkolenia

Szkolenie jest podzielone na 4 moduły, każdy trwający około 2 godzin:

1. **Moduł 1: Podstawy**
   - Wprowadzenie do chatbotów
   - Architektura systemu
   - Panel administracyjny
   - Podstawy obsługi

2. **Moduł 2: Baza wiedzy i kanały komunikacji**
   - Zarządzanie bazą wiedzy
   - Konfiguracja strony internetowej
   - Konfiguracja Instagram
   - Konfiguracja WhatsApp

3. **Moduł 3: Integracje i analityka**
   - Integracja z monday.com
   - Integracja z Booksy
   - Integracja z Google Calendar
   - Monitorowanie i analityka

4. **Moduł 4: Rozwiązywanie problemów i najlepsze praktyki**
   - Typowe problemy i rozwiązania
   - Procedury awaryjne
   - Najlepsze praktyki
   - Ćwiczenia praktyczne

## Podstawy obsługi chatbota

### Czym jest chatbot?

Chatbot to program komputerowy, który symuluje rozmowę z człowiekiem. Chatbot NovaHouse jest oparty na platformie Chatfuel z modułem Fuely AI, co oznacza, że wykorzystuje sztuczną inteligencję do rozpoznawania intencji użytkownika i generowania odpowiedzi.

### Jak działa chatbot NovaHouse?

1. **Użytkownik** inicjuje rozmowę poprzez stronę internetową, Instagram lub WhatsApp
2. **Chatbot** analizuje wiadomość użytkownika i rozpoznaje intencję
3. **Chatbot** generuje odpowiedź na podstawie bazy wiedzy
4. **Użytkownik** kontynuuje rozmowę
5. **Chatbot** prowadzi użytkownika przez proces konwersacji, np. umawianie spotkania

### Główne funkcje chatbota NovaHouse

- **Odpowiadanie na pytania** o ofertę, pakiety wykończeniowe, proces realizacji, ceny itp.
- **Umawianie spotkań** z konsultantami poprzez integrację z Google Calendar i Booksy
- **Przekierowanie do konsultanta** w przypadku złożonych pytań lub na życzenie klienta
- **Tworzenie leadów** w monday.com na podstawie rozmów z klientami
- **Wysyłanie powiadomień** email i SMS do klientów i konsultantów

### Kanały komunikacji

Chatbot NovaHouse działa na trzech kanałach komunikacji:

1. **Strona internetowa** - widget na stronie NovaHouse
2. **Instagram** - poprzez wiadomości prywatne na profilu NovaHouse
3. **WhatsApp** - poprzez numer WhatsApp Business NovaHouse

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

### Podstawowe operacje

- **Włączanie/wyłączanie chatbota** - przejdź do "Settings" > "General" i przełącz przełącznik "Bot Status"
- **Zmiana wyglądu widgetu** - przejdź do "Channels" > "Website" i skonfiguruj wygląd widgetu
- **Przeglądanie rozmów** - przejdź do "Analytics" > "Conversations" i przeglądaj historię rozmów
- **Zarządzanie użytkownikami** - przejdź do "Settings" > "Users" i zarządzaj użytkownikami panelu

## Zarządzanie bazą wiedzy

### Struktura bazy wiedzy

Baza wiedzy chatbota NovaHouse składa się z:

- **Intencji** - reprezentują cel lub zamiar użytkownika
- **Encji** - reprezentują kluczowe informacje w wypowiedziach użytkownika
- **Odpowiedzi** - treści zwracane użytkownikowi
- **Kontekstów** - zarządzają przepływem konwersacji

### Intencje

Intencje reprezentują cel lub zamiar użytkownika. Przykłady intencji w chatbocie NovaHouse:

- **Powitanie** - użytkownik wita się z chatbotem
- **Informacje o firmie** - użytkownik pyta o informacje o NovaHouse
- **Pakiety wykończeniowe** - użytkownik pyta o pakiety wykończeniowe
- **Umówienie spotkania** - użytkownik chce umówić spotkanie
- **Kontakt z konsultantem** - użytkownik chce porozmawiać z konsultantem

#### Dodawanie nowych intencji

1. Przejdź do sekcji "AI" > "Intents"
2. Kliknij "Add Intent"
3. Wprowadź nazwę intencji (np. "info_pakiet_waniliowy")
4. Dodaj przykładowe wypowiedzi (min. 15-20)
5. Skonfiguruj parametry (encje do wyodrębnienia)
6. Skonfiguruj odpowiedzi
7. Kliknij "Save"

#### Edycja istniejących intencji

1. Przejdź do sekcji "AI" > "Intents"
2. Wybierz intencję do edycji
3. Edytuj nazwę, przykładowe wypowiedzi, parametry lub odpowiedzi
4. Kliknij "Save"

### Encje

Encje reprezentują kluczowe informacje w wypowiedziach użytkownika. Przykłady encji w chatbocie NovaHouse:

- **Pakiet wykończeniowy** - waniliowy, cynamonowy, szafranowy, pomarańczowy
- **Metraż lokalu** - mały (do 50m²), średni (50-100m²), duży (powyżej 100m²)
- **Typ nieruchomości** - mieszkanie, dom, biuro, lokal usługowy
- **Miasto** - Gdańsk, Gdynia, Sopot, Warszawa, inne
- **Element wykończenia** - podłogi, ściany, sufity, łazienka, kuchnia, elektryka, hydraulika

#### Dodawanie nowych encji

1. Przejdź do sekcji "AI" > "Entities"
2. Kliknij "Add Entity"
3. Wprowadź nazwę encji (np. "pakiet_wykonczeniowy")
4. Dodaj wartości encji (np. "waniliowy", "cynamonowy", "szafranowy", "pomarańczowy")
5. Dla każdej wartości, dodaj synonimy
6. Kliknij "Save"

#### Edycja istniejących encji

1. Przejdź do sekcji "AI" > "Entities"
2. Wybierz encję do edycji
3. Edytuj nazwę, wartości lub synonimy
4. Kliknij "Save"

### Odpowiedzi

Odpowiedzi to treści zwracane użytkownikowi. Przykłady odpowiedzi w chatbocie NovaHouse:

- **Odpowiedź na powitanie** - "Witaj! Jak mogę Ci pomóc?"
- **Odpowiedź na pytanie o pakiety** - "NovaHouse oferuje cztery pakiety wykończeniowe: Waniliowy (podstawowy), Cynamonowy (rozszerzony), Szafranowy (premium) i Pomarańczowy (luksusowy). Każdy pakiet zawiera różny zakres prac i materiałów."
- **Odpowiedź na prośbę o umówienie spotkania** - "Chętnie umówię Cię na spotkanie z naszym konsultantem. Jaki termin Ci odpowiada?"

#### Dodawanie nowych odpowiedzi

1. Przejdź do sekcji "AI" > "Responses"
2. Kliknij "Add Response"
3. Wprowadź nazwę odpowiedzi
4. Dodaj treść odpowiedzi
5. Dodaj warianty odpowiedzi dla naturalności
6. Kliknij "Save"

#### Edycja istniejących odpowiedzi

1. Przejdź do sekcji "AI" > "Responses"
2. Wybierz odpowiedź do edycji
3. Edytuj nazwę, treść lub warianty
4. Kliknij "Save"

### Testowanie bazy wiedzy

1. Przejdź do sekcji "AI" > "Test"
2. Wprowadź przykładowe wypowiedzi użytkownika
3. Sprawdź, czy intencje są poprawnie rozpoznawane
4. Sprawdź, czy encje są poprawnie wyodrębniane
5. Sprawdź, czy odpowiedzi są poprawne

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

### Procedury awaryjne

#### Wyłączenie chatbota

W przypadku poważnych problemów, można wyłączyć chatbota:

1. Przejdź do sekcji "Settings" > "General"
2. Przełącz przełącznik "Bot Status" na "Off"
3. Kliknij "Save"

Chatbot zostanie wyłączony na wszystkich kanałach komunikacji.

#### Przywrócenie poprzedniej wersji

W przypadku problemów z nową wersją, można przywrócić poprzednią wersję:

1. Przejdź do sekcji "Settings" > "Versions"
2. Wybierz poprzednią wersję z listy
3. Kliknij "Restore"
4. Potwierdź przywrócenie

## Najlepsze praktyki

### Zarządzanie bazą wiedzy

- **Regularnie aktualizuj bazę wiedzy** - analizuj pytania bez odpowiedzi i dodawaj nowe intencje
- **Używaj różnorodnych przykładowych wypowiedzi** - uwzględnij różne sposoby formułowania pytań
- **Dodawaj synonimy do encji** - uwzględnij różne sposoby nazywania tych samych rzeczy
- **Testuj bazę wiedzy** - regularnie testuj, czy chatbot poprawnie rozpoznaje intencje i encje

### Zarządzanie kanałami komunikacji

- **Dostosuj wygląd widgetu do identyfikacji wizualnej NovaHouse** - używaj kolorów i logo firmy
- **Używaj automatycznego powitania** - przywitaj użytkownika po kilku sekundach od otwarcia strony
- **Dostosuj odpowiedzi do kanału komunikacji** - używaj krótszych odpowiedzi na Instagram i WhatsApp
- **Testuj na różnych urządzeniach** - sprawdź, czy widget działa poprawnie na komputerach, tabletach i smartfonach

### Zarządzanie integracjami

- **Regularnie sprawdzaj integracje** - testuj, czy integracje działają poprawnie
- **Monitoruj limity API** - sprawdzaj, czy nie przekraczasz limitów API
- **Aktualizuj klucze API** - regularnie aktualizuj klucze API dla bezpieczeństwa
- **Testuj cały proces** - testuj cały proces od rozmowy z chatbotem do utworzenia leada lub rezerwacji

### Monitorowanie i analityka

- **Regularnie analizuj dane** - sprawdzaj statystyki i raporty
- **Identyfikuj obszary do poprawy** - analizuj pytania bez odpowiedzi i problemy z rozpoznawaniem intencji
- **Monitoruj konwersje** - sprawdzaj, ile rozmów kończy się umówieniem spotkania lub kontaktem z konsultantem
- **Konfiguruj alerty** - ustaw alerty o błędach i problemach

## Ćwiczenia praktyczne

### Ćwiczenie 1: Dodawanie nowej intencji

1. Zaloguj się do panelu administracyjnego Chatfuel
2. Przejdź do sekcji "AI" > "Intents"
3. Kliknij "Add Intent"
4. Wprowadź nazwę intencji "info_lokalizacja_gdansk"
5. Dodaj przykładowe wypowiedzi:
   - "Gdzie znajduje się biuro NovaHouse w Gdańsku?"
   - "Jaki jest adres biura w Gdańsku?"
   - "Jak dojechać do biura w Gdańsku?"
   - "Gdzie was znajdę w Gdańsku?"
   - "Gdzie jest wasze biuro w Gdańsku?"
6. Skonfiguruj odpowiedź:
   - "Nasze biuro w Gdańsku znajduje się przy ul. Grunwaldzkiej 472, 80-309 Gdańsk. Zapraszamy od poniedziałku do piątku w godzinach 9:00-17:00."
7. Kliknij "Save"
8. Przetestuj nową intencję w sekcji "AI" > "Test"

### Ćwiczenie 2: Konfiguracja widgetu na stronie

1. Zaloguj się do panelu administracyjnego Chatfuel
2. Przejdź do sekcji "Channels" > "Website"
3. Skonfiguruj wygląd widgetu:
   - Kolor główny: `#F5A623` (pomarańczowy NovaHouse)
   - Ikona: logo NovaHouse
   - Tekst powitalny: "Witaj! Jak możemy Ci pomóc?"
   - Pozycja: prawy dolny róg
4. Skonfiguruj zachowanie widgetu:
   - Automatyczne powitanie po 5 sekundach
   - Dźwięk powiadomień: włączony
   - Tryb mobilny: zoptymalizowany
5. Kliknij "Save"
6. Wygeneruj kod widgetu i zanotuj go (nie instaluj na stronie produkcyjnej)

### Ćwiczenie 3: Analiza danych

1. Zaloguj się do panelu administracyjnego Chatfuel
2. Przejdź do sekcji "Analytics" > "Dashboard"
3. Przeanalizuj dane:
   - Liczba rozmów
   - Liczba wiadomości
   - Liczba użytkowników
   - Średni czas rozmowy
4. Przejdź do sekcji "Analytics" > "Intents"
5. Przeanalizuj dane:
   - Najczęstsze intencje
   - Skuteczność rozpoznawania intencji
6. Przejdź do sekcji "Analytics" > "Conversations"
7. Przeanalizuj przykładowe rozmowy
8. Przygotuj krótki raport z analizy danych

### Ćwiczenie 4: Rozwiązywanie problemów

1. Zaloguj się do panelu administracyjnego Chatfuel
2. Przejdź do sekcji "Settings" > "Logs"
3. Przeanalizuj logi błędów
4. Zidentyfikuj potencjalne problemy
5. Zaproponuj rozwiązania
6. Przygotuj krótki raport z analizy problemów i propozycji rozwiązań

---

Przygotował: Michał Marini  
Data: 8 lipca 2025
