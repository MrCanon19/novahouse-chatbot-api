# Plan testów funkcjonalnych i akceptacyjnych dla chatbota NovaHouse
## Instrukcja techniczna

## Spis treści
1. [Przegląd procesu testowania](#przegląd-procesu-testowania)
2. [Testy funkcjonalne](#testy-funkcjonalne)
3. [Testy integracji](#testy-integracji)
4. [Testy wydajnościowe](#testy-wydajnościowe)
5. [Testy użyteczności](#testy-użyteczności)
6. [Testy akceptacyjne](#testy-akceptacyjne)
7. [Raportowanie błędów](#raportowanie-błędów)
8. [Kryteria akceptacji](#kryteria-akceptacji)
9. [Harmonogram testów](#harmonogram-testów)
10. [Najlepsze praktyki](#najlepsze-praktyki)

## Przegląd procesu testowania

Proces testowania chatbota NovaHouse opartego na platformie Chatfuel z modułem Fuely AI składa się z następujących etapów:

1. **Testy funkcjonalne** - weryfikacja poprawności działania poszczególnych funkcji chatbota
2. **Testy integracji** - weryfikacja poprawności integracji z systemami zewnętrznymi
3. **Testy wydajnościowe** - weryfikacja wydajności chatbota pod obciążeniem
4. **Testy użyteczności** - weryfikacja łatwości użycia i satysfakcji użytkowników
5. **Testy akceptacyjne** - weryfikacja zgodności z wymaganiami biznesowymi

### Środowiska testowe

Testy będą przeprowadzane w trzech środowiskach:

1. **Środowisko deweloperskie** - do testów funkcjonalnych i integracyjnych
2. **Środowisko testowe** - do testów wydajnościowych i użyteczności
3. **Środowisko produkcyjne** - do testów akceptacyjnych

### Role i odpowiedzialności

| Rola | Odpowiedzialność |
|------|-----------------|
| Deweloper | Implementacja chatbota, poprawki błędów |
| Tester | Przeprowadzanie testów, raportowanie błędów |
| Product Owner | Definiowanie wymagań, akceptacja testów |
| Użytkownik końcowy | Udział w testach użyteczności i akceptacyjnych |

## Testy funkcjonalne

### Testy bazy wiedzy

| ID | Nazwa testu | Opis | Kroki | Oczekiwany wynik |
|----|------------|------|-------|-----------------|
| F01 | Test rozpoznawania intencji | Weryfikacja poprawności rozpoznawania intencji użytkownika | 1. Wprowadź pytanie o pakiety wykończeniowe<br>2. Wprowadź pytanie o proces realizacji<br>3. Wprowadź pytanie o cennik | Chatbot poprawnie rozpoznaje intencje i udziela odpowiednich odpowiedzi |
| F02 | Test wyodrębniania encji | Weryfikacja poprawności wyodrębniania encji z wypowiedzi użytkownika | 1. Wprowadź pytanie zawierające nazwę pakietu<br>2. Wprowadź pytanie zawierające metraż<br>3. Wprowadź pytanie zawierające typ nieruchomości | Chatbot poprawnie wyodrębnia encje i wykorzystuje je w odpowiedziach |
| F03 | Test odpowiedzi na pytania | Weryfikacja poprawności odpowiedzi na pytania użytkownika | 1. Zadaj pytanie o pakiet waniliowy<br>2. Zadaj pytanie o proces realizacji<br>3. Zadaj pytanie o lokalizację | Chatbot udziela poprawnych, kompletnych i spójnych odpowiedzi |
| F04 | Test obsługi pytań złożonych | Weryfikacja poprawności obsługi pytań złożonych | 1. Zadaj pytanie zawierające kilka intencji<br>2. Zadaj pytanie z wieloma encjami<br>3. Zadaj pytanie z negacją | Chatbot poprawnie obsługuje złożone pytania lub prosi o doprecyzowanie |
| F05 | Test obsługi pytań niezrozumiałych | Weryfikacja poprawności obsługi pytań niezrozumiałych | 1. Wprowadź losowy ciąg znaków<br>2. Wprowadź pytanie spoza domeny<br>3. Wprowadź pytanie z błędami | Chatbot informuje o niezrozumieniu i sugeruje alternatywne tematy |

### Testy umawiania spotkań

| ID | Nazwa testu | Opis | Kroki | Oczekiwany wynik |
|----|------------|------|-------|-----------------|
| F06 | Test inicjacji umawiania spotkania | Weryfikacja poprawności inicjacji procesu umawiania spotkania | 1. Wprowadź prośbę o umówienie spotkania<br>2. Wybierz cel spotkania | Chatbot rozpoczyna proces umawiania spotkania i pyta o cel |
| F07 | Test wyboru terminu | Weryfikacja poprawności wyboru terminu spotkania | 1. Wybierz cel spotkania<br>2. Wybierz datę<br>3. Wybierz godzinę | Chatbot poprawnie prowadzi przez proces wyboru terminu |
| F08 | Test podania danych kontaktowych | Weryfikacja poprawności zbierania danych kontaktowych | 1. Wybierz termin<br>2. Podaj imię i nazwisko<br>3. Podaj email<br>4. Podaj telefon | Chatbot poprawnie zbiera dane kontaktowe |
| F09 | Test potwierdzenia spotkania | Weryfikacja poprawności potwierdzenia spotkania | 1. Podaj dane kontaktowe<br>2. Potwierdź spotkanie | Chatbot potwierdza spotkanie i wysyła potwierdzenie |
| F10 | Test zmiany terminu | Weryfikacja poprawności zmiany terminu spotkania | 1. Poproś o zmianę terminu<br>2. Wybierz nowy termin<br>3. Potwierdź zmianę | Chatbot poprawnie obsługuje zmianę terminu |
| F11 | Test odwołania spotkania | Weryfikacja poprawności odwołania spotkania | 1. Poproś o odwołanie spotkania<br>2. Potwierdź odwołanie | Chatbot poprawnie obsługuje odwołanie spotkania |

### Testy przekierowania do konsultanta

| ID | Nazwa testu | Opis | Kroki | Oczekiwany wynik |
|----|------------|------|-------|-----------------|
| F12 | Test inicjacji przekierowania | Weryfikacja poprawności inicjacji procesu przekierowania do konsultanta | 1. Wprowadź prośbę o kontakt z konsultantem<br>2. Potwierdź chęć kontaktu | Chatbot rozpoczyna proces przekierowania i informuje o kolejnych krokach |
| F13 | Test zbierania danych do przekierowania | Weryfikacja poprawności zbierania danych do przekierowania | 1. Potwierdź chęć kontaktu<br>2. Podaj imię i nazwisko<br>3. Podaj email<br>4. Podaj telefon<br>5. Podaj temat | Chatbot poprawnie zbiera dane do przekierowania |
| F14 | Test potwierdzenia przekierowania | Weryfikacja poprawności potwierdzenia przekierowania | 1. Podaj dane do przekierowania<br>2. Potwierdź przekierowanie | Chatbot potwierdza przekierowanie i informuje o czasie odpowiedzi |
| F15 | Test automatycznego przekierowania | Weryfikacja poprawności automatycznego przekierowania po nieudanych odpowiedziach | 1. Zadaj pytanie spoza bazy wiedzy<br>2. Zadaj kolejne pytanie spoza bazy wiedzy<br>3. Zadaj trzecie pytanie spoza bazy wiedzy | Chatbot proponuje przekierowanie do konsultanta po trzech nieudanych próbach |

### Testy interfejsu użytkownika

| ID | Nazwa testu | Opis | Kroki | Oczekiwany wynik |
|----|------------|------|-------|-----------------|
| F16 | Test widgetu na stronie | Weryfikacja poprawności wyświetlania widgetu na stronie | 1. Otwórz stronę NovaHouse<br>2. Sprawdź widoczność widgetu<br>3. Kliknij widget | Widget jest widoczny i reaguje na kliknięcie |
| F17 | Test responsywności | Weryfikacja poprawności wyświetlania na różnych urządzeniach | 1. Otwórz stronę na komputerze<br>2. Otwórz stronę na tablecie<br>3. Otwórz stronę na smartfonie | Widget poprawnie dostosowuje się do różnych rozmiarów ekranu |
| F18 | Test przycisków szybkich odpowiedzi | Weryfikacja poprawności działania przycisków szybkich odpowiedzi | 1. Rozpocznij rozmowę<br>2. Otrzymaj przyciski szybkich odpowiedzi<br>3. Kliknij przycisk | Przyciski są widoczne i reagują na kliknięcie |
| F19 | Test załączników | Weryfikacja poprawności wyświetlania załączników | 1. Zadaj pytanie o pakiety<br>2. Otrzymaj odpowiedź z załącznikiem<br>3. Kliknij załącznik | Załączniki są widoczne i reagują na kliknięcie |
| F20 | Test historii rozmowy | Weryfikacja poprawności zapisywania i wyświetlania historii rozmowy | 1. Przeprowadź rozmowę<br>2. Zamknij widget<br>3. Otwórz widget ponownie | Historia rozmowy jest zachowana |

## Testy integracji

### Testy integracji z monday.com

| ID | Nazwa testu | Opis | Kroki | Oczekiwany wynik |
|----|------------|------|-------|-----------------|
| I01 | Test tworzenia leada | Weryfikacja poprawności tworzenia leada w monday.com | 1. Przeprowadź rozmowę z chatbotem<br>2. Wypełnij formularz kontaktowy<br>3. Sprawdź monday.com | Lead jest poprawnie utworzony w monday.com z wszystkimi danymi |
| I02 | Test aktualizacji leada | Weryfikacja poprawności aktualizacji leada w monday.com | 1. Przeprowadź rozmowę z istniejącym leadem<br>2. Podaj nowe informacje<br>3. Sprawdź monday.com | Lead jest poprawnie zaktualizowany w monday.com |
| I03 | Test tworzenia zadania | Weryfikacja poprawności tworzenia zadania w monday.com | 1. Poproś o kontakt z konsultantem<br>2. Podaj dane kontaktowe<br>3. Sprawdź monday.com | Zadanie jest poprawnie utworzone w monday.com |

### Testy integracji z Booksy

| ID | Nazwa testu | Opis | Kroki | Oczekiwany wynik |
|----|------------|------|-------|-----------------|
| I04 | Test sprawdzania dostępności | Weryfikacja poprawności sprawdzania dostępności terminów w Booksy | 1. Rozpocznij proces umawiania spotkania<br>2. Wybierz usługę<br>3. Sprawdź dostępne terminy | Chatbot poprawnie wyświetla dostępne terminy z Booksy |
| I05 | Test tworzenia rezerwacji | Weryfikacja poprawności tworzenia rezerwacji w Booksy | 1. Wybierz termin<br>2. Podaj dane kontaktowe<br>3. Potwierdź rezerwację<br>4. Sprawdź Booksy | Rezerwacja jest poprawnie utworzona w Booksy |
| I06 | Test zmiany rezerwacji | Weryfikacja poprawności zmiany rezerwacji w Booksy | 1. Poproś o zmianę terminu<br>2. Wybierz nowy termin<br>3. Potwierdź zmianę<br>4. Sprawdź Booksy | Rezerwacja jest poprawnie zmieniona w Booksy |
| I07 | Test odwołania rezerwacji | Weryfikacja poprawności odwołania rezerwacji w Booksy | 1. Poproś o odwołanie rezerwacji<br>2. Potwierdź odwołanie<br>3. Sprawdź Booksy | Rezerwacja jest poprawnie odwołana w Booksy |

### Testy integracji z Google Calendar

| ID | Nazwa testu | Opis | Kroki | Oczekiwany wynik |
|----|------------|------|-------|-----------------|
| I08 | Test tworzenia wydarzenia | Weryfikacja poprawności tworzenia wydarzenia w Google Calendar | 1. Umów spotkanie<br>2. Potwierdź rezerwację<br>3. Sprawdź Google Calendar | Wydarzenie jest poprawnie utworzone w Google Calendar |
| I09 | Test zmiany wydarzenia | Weryfikacja poprawności zmiany wydarzenia w Google Calendar | 1. Zmień termin spotkania<br>2. Potwierdź zmianę<br>3. Sprawdź Google Calendar | Wydarzenie jest poprawnie zmienione w Google Calendar |
| I10 | Test odwołania wydarzenia | Weryfikacja poprawności odwołania wydarzenia w Google Calendar | 1. Odwołaj spotkanie<br>2. Potwierdź odwołanie<br>3. Sprawdź Google Calendar | Wydarzenie jest poprawnie odwołane w Google Calendar |

### Testy integracji z systemem powiadomień

| ID | Nazwa testu | Opis | Kroki | Oczekiwany wynik |
|----|------------|------|-------|-----------------|
| I11 | Test powiadomień email | Weryfikacja poprawności wysyłania powiadomień email | 1. Umów spotkanie<br>2. Potwierdź rezerwację<br>3. Sprawdź skrzynkę email | Email z potwierdzeniem jest poprawnie wysłany |
| I12 | Test powiadomień SMS | Weryfikacja poprawności wysyłania powiadomień SMS | 1. Umów spotkanie<br>2. Potwierdź rezerwację<br>3. Sprawdź telefon | SMS z potwierdzeniem jest poprawnie wysłany |
| I13 | Test przypomnień | Weryfikacja poprawności wysyłania przypomnień | 1. Umów spotkanie na następny dzień<br>2. Poczekaj na przypomnienie<br>3. Sprawdź email i telefon | Przypomnienia są poprawnie wysłane |

### Testy integracji z kanałami komunikacji

| ID | Nazwa testu | Opis | Kroki | Oczekiwany wynik |
|----|------------|------|-------|-----------------|
| I14 | Test integracji z Instagram | Weryfikacja poprawności integracji z Instagram | 1. Wyślij wiadomość na Instagram NovaHouse<br>2. Sprawdź odpowiedź chatbota<br>3. Przeprowadź rozmowę | Chatbot poprawnie odpowiada na wiadomości na Instagram |
| I15 | Test integracji z WhatsApp | Weryfikacja poprawności integracji z WhatsApp | 1. Wyślij wiadomość na WhatsApp NovaHouse<br>2. Sprawdź odpowiedź chatbota<br>3. Przeprowadź rozmowę | Chatbot poprawnie odpowiada na wiadomości na WhatsApp |
| I16 | Test integracji z formularzami | Weryfikacja poprawności integracji z formularzami na stronie | 1. Wypełnij formularz na stronie<br>2. Sprawdź odpowiedź chatbota<br>3. Sprawdź monday.com | Chatbot poprawnie obsługuje formularze i tworzy leady |

## Testy wydajnościowe

### Testy obciążeniowe

| ID | Nazwa testu | Opis | Kroki | Oczekiwany wynik |
|----|------------|------|-------|-----------------|
| P01 | Test wielu równoczesnych rozmów | Weryfikacja poprawności obsługi wielu równoczesnych rozmów | 1. Symuluj 10 równoczesnych rozmów<br>2. Symuluj 50 równoczesnych rozmów<br>3. Symuluj 100 równoczesnych rozmów | Chatbot poprawnie obsługuje wszystkie rozmowy bez znaczącego spadku wydajności |
| P02 | Test czasu odpowiedzi | Weryfikacja czasu odpowiedzi chatbota | 1. Zmierz czas odpowiedzi dla prostych pytań<br>2. Zmierz czas odpowiedzi dla złożonych pytań<br>3. Zmierz czas odpowiedzi dla pytań wymagających integracji | Czas odpowiedzi nie przekracza 2 sekund dla prostych pytań i 5 sekund dla złożonych |
| P03 | Test długotrwały | Weryfikacja stabilności chatbota w długim okresie | 1. Uruchom chatbota na 24 godziny<br>2. Monitoruj zużycie zasobów<br>3. Monitoruj stabilność | Chatbot działa stabilnie przez 24 godziny bez wycieków pamięci i spadku wydajności |

### Testy limitów

| ID | Nazwa testu | Opis | Kroki | Oczekiwany wynik |
|----|------------|------|-------|-----------------|
| P04 | Test limitów API | Weryfikacja obsługi limitów API | 1. Symuluj intensywne korzystanie z API<br>2. Monitoruj limity API<br>3. Sprawdź obsługę przekroczenia limitów | Chatbot poprawnie obsługuje limity API i informuje o problemach |
| P05 | Test długich wiadomości | Weryfikacja obsługi długich wiadomości | 1. Wyślij bardzo długą wiadomość<br>2. Wyślij wiadomość z wieloma pytaniami<br>3. Wyślij wiadomość z dużą ilością danych | Chatbot poprawnie obsługuje długie wiadomości |
| P06 | Test dużej liczby załączników | Weryfikacja obsługi dużej liczby załączników | 1. Wyślij wiadomość z prośbą o wiele załączników<br>2. Sprawdź odpowiedź chatbota<br>3. Sprawdź załączniki | Chatbot poprawnie obsługuje dużą liczbę załączników |

## Testy użyteczności

### Testy z udziałem zespołu NovaHouse

| ID | Nazwa testu | Opis | Kroki | Oczekiwany wynik |
|----|------------|------|-------|-----------------|
| U01 | Test intuicyjności interfejsu | Weryfikacja intuicyjności interfejsu chatbota | 1. Poproś członków zespołu o przeprowadzenie rozmowy<br>2. Zbierz opinie na temat interfejsu<br>3. Zidentyfikuj problemy | Interfejs jest intuicyjny i łatwy w użyciu |
| U02 | Test jakości odpowiedzi | Weryfikacja jakości odpowiedzi chatbota | 1. Poproś członków zespołu o zadanie różnych pytań<br>2. Zbierz opinie na temat jakości odpowiedzi<br>3. Zidentyfikuj problemy | Odpowiedzi są wysokiej jakości, dokładne i pomocne |
| U03 | Test przepływu konwersacji | Weryfikacja płynności przepływu konwersacji | 1. Poproś członków zespołu o przeprowadzenie złożonych rozmów<br>2. Zbierz opinie na temat przepływu konwersacji<br>3. Zidentyfikuj problemy | Przepływ konwersacji jest płynny i naturalny |

### Testy z udziałem potencjalnych klientów

| ID | Nazwa testu | Opis | Kroki | Oczekiwany wynik |
|----|------------|------|-------|-----------------|
| U04 | Test satysfakcji użytkowników | Weryfikacja satysfakcji użytkowników z chatbota | 1. Poproś potencjalnych klientów o przeprowadzenie rozmowy<br>2. Zbierz opinie na temat satysfakcji<br>3. Zidentyfikuj problemy | Użytkownicy są zadowoleni z interakcji z chatbotem |
| U05 | Test realizacji celów | Weryfikacja skuteczności realizacji celów użytkowników | 1. Poproś potencjalnych klientów o realizację konkretnych celów<br>2. Zmierz skuteczność realizacji celów<br>3. Zidentyfikuj problemy | Użytkownicy skutecznie realizują swoje cele |
| U06 | Test porównawczy | Porównanie chatbota z innymi metodami kontaktu | 1. Poproś potencjalnych klientów o porównanie chatbota z innymi metodami kontaktu<br>2. Zbierz opinie na temat porównania<br>3. Zidentyfikuj przewagi i słabości | Chatbot jest preferowany lub równie dobry jak inne metody kontaktu |

## Testy akceptacyjne

### Testy zgodności z wymaganiami

| ID | Nazwa testu | Opis | Kroki | Oczekiwany wynik |
|----|------------|------|-------|-----------------|
| A01 | Test zgodności z wymaganiami funkcjonalnymi | Weryfikacja zgodności chatbota z wymaganiami funkcjonalnymi | 1. Przejrzyj listę wymagań funkcjonalnych<br>2. Sprawdź realizację każdego wymagania<br>3. Zidentyfikuj braki | Chatbot spełnia wszystkie wymagania funkcjonalne |
| A02 | Test zgodności z wymaganiami niefunkcjonalnymi | Weryfikacja zgodności chatbota z wymaganiami niefunkcjonalnymi | 1. Przejrzyj listę wymagań niefunkcjonalnych<br>2. Sprawdź realizację każdego wymagania<br>3. Zidentyfikuj braki | Chatbot spełnia wszystkie wymagania niefunkcjonalne |
| A03 | Test zgodności z wymaganiami biznesowymi | Weryfikacja zgodności chatbota z wymaganiami biznesowymi | 1. Przejrzyj listę wymagań biznesowych<br>2. Sprawdź realizację każdego wymagania<br>3. Zidentyfikuj braki | Chatbot spełnia wszystkie wymagania biznesowe |

### Testy scenariuszowe

| ID | Nazwa testu | Opis | Kroki | Oczekiwany wynik |
|----|------------|------|-------|-----------------|
| A04 | Test scenariusza informacyjnego | Weryfikacja poprawności obsługi scenariusza informacyjnego | 1. Przeprowadź rozmowę informacyjną o pakietach<br>2. Zadaj pytania o szczegóły<br>3. Poproś o materiały | Chatbot poprawnie obsługuje scenariusz informacyjny |
| A05 | Test scenariusza sprzedażowego | Weryfikacja poprawności obsługi scenariusza sprzedażowego | 1. Przeprowadź rozmowę o zakupie pakietu<br>2. Umów spotkanie<br>3. Potwierdź rezerwację | Chatbot poprawnie obsługuje scenariusz sprzedażowy |
| A06 | Test scenariusza obsługi klienta | Weryfikacja poprawności obsługi scenariusza obsługi klienta | 1. Przeprowadź rozmowę o problemie<br>2. Poproś o kontakt z konsultantem<br>3. Potwierdź przekierowanie | Chatbot poprawnie obsługuje scenariusz obsługi klienta |

### Testy akceptacji użytkownika

| ID | Nazwa testu | Opis | Kroki | Oczekiwany wynik |
|----|------------|------|-------|-----------------|
| A07 | Test akceptacji przez zespół NovaHouse | Weryfikacja akceptacji chatbota przez zespół NovaHouse | 1. Przeprowadź prezentację chatbota dla zespołu<br>2. Zbierz opinie i uwagi<br>3. Przeprowadź głosowanie akceptacyjne | Chatbot jest zaakceptowany przez zespół NovaHouse |
| A08 | Test akceptacji przez kierownictwo | Weryfikacja akceptacji chatbota przez kierownictwo NovaHouse | 1. Przeprowadź prezentację chatbota dla kierownictwa<br>2. Przedstaw wyniki testów<br>3. Uzyskaj formalną akceptację | Chatbot jest zaakceptowany przez kierownictwo NovaHouse |
| A09 | Test akceptacji przez klientów | Weryfikacja akceptacji chatbota przez klientów NovaHouse | 1. Udostępnij chatbota wybranej grupie klientów<br>2. Zbierz opinie i uwagi<br>3. Przeprowadź ankietę satysfakcji | Chatbot jest zaakceptowany przez klientów NovaHouse |

## Raportowanie błędów

### Proces raportowania błędów

1. **Identyfikacja błędu** - podczas testów, zidentyfikuj błąd i jego kroki reprodukcji
2. **Dokumentacja błędu** - udokumentuj błąd, w tym:
   - ID błędu
   - Nazwa błędu
   - Opis błędu
   - Kroki reprodukcji
   - Oczekiwany wynik
   - Aktualny wynik
   - Priorytet
   - Waga
   - Zrzuty ekranu lub nagrania
3. **Zgłoszenie błędu** - zgłoś błąd w systemie śledzenia błędów
4. **Weryfikacja poprawki** - po naprawie błędu, zweryfikuj poprawkę

### Szablon raportu błędu

```
ID: BUG-001
Nazwa: Niepoprawne rozpoznawanie intencji dla pytań o pakiet waniliowy
Opis: Chatbot nie rozpoznaje intencji dla pytań o pakiet waniliowy, gdy użytkownik używa określenia "podstawowy" zamiast "waniliowy".
Kroki reprodukcji:
1. Rozpocznij rozmowę z chatbotem
2. Zadaj pytanie "Jakie są szczegóły pakietu podstawowego?"
3. Sprawdź odpowiedź chatbota
Oczekiwany wynik: Chatbot rozpoznaje intencję "info_pakiet_szczegoly" z encją "pakiet_wykonczeniowy" o wartości "waniliowy" i udziela informacji o pakiecie waniliowym.
Aktualny wynik: Chatbot nie rozpoznaje intencji i odpowiada "Przepraszam, nie rozumiem pytania. Czy możesz sformułować je inaczej?".
Priorytet: Wysoki
Waga: Krytyczna
Zrzuty ekranu: [link do zrzutu ekranu]
```

### Priorytety błędów

| Priorytet | Opis |
|-----------|------|
| Krytyczny | Błąd uniemożliwiający korzystanie z chatbota lub powodujący utratę danych |
| Wysoki | Błąd znacząco utrudniający korzystanie z chatbota lub powodujący niepoprawne działanie kluczowych funkcji |
| Średni | Błąd utrudniający korzystanie z chatbota, ale możliwy do obejścia |
| Niski | Błąd kosmetyczny lub niewpływający znacząco na korzystanie z chatbota |

## Kryteria akceptacji

### Kryteria akceptacji dla testów funkcjonalnych

- 100% testów funkcjonalnych zakończonych sukcesem
- Brak błędów krytycznych i wysokich
- Maksymalnie 5 błędów średnich
- Maksymalnie 10 błędów niskich

### Kryteria akceptacji dla testów integracji

- 100% testów integracji zakończonych sukcesem
- Brak błędów krytycznych
- Maksymalnie 3 błędy wysokie
- Maksymalnie 7 błędów średnich
- Maksymalnie 15 błędów niskich

### Kryteria akceptacji dla testów wydajnościowych

- Czas odpowiedzi poniżej 2 sekund dla 95% zapytań
- Obsługa minimum 50 równoczesnych rozmów bez spadku wydajności
- Stabilna praca przez minimum 24 godziny
- Zużycie zasobów w granicach limitów platformy

### Kryteria akceptacji dla testów użyteczności

- Minimum 80% pozytywnych opinii od zespołu NovaHouse
- Minimum 70% pozytywnych opinii od potencjalnych klientów
- Minimum 80% skuteczności realizacji celów przez użytkowników

### Kryteria akceptacji dla testów akceptacyjnych

- 100% zgodności z wymaganiami funkcjonalnymi
- Minimum 90% zgodności z wymaganiami niefunkcjonalnymi
- 100% zgodności z wymaganiami biznesowymi
- Formalna akceptacja przez kierownictwo NovaHouse

## Harmonogram testów

### Faza 1: Testy funkcjonalne (1-2 dni)

| Dzień | Aktywność |
|-------|-----------|
| Dzień 1 | Testy bazy wiedzy (F01-F05)<br>Testy umawiania spotkań (F06-F11) |
| Dzień 2 | Testy przekierowania do konsultanta (F12-F15)<br>Testy interfejsu użytkownika (F16-F20) |

### Faza 2: Testy integracji (2-3 dni)

| Dzień | Aktywność |
|-------|-----------|
| Dzień 3 | Testy integracji z monday.com (I01-I03)<br>Testy integracji z Booksy (I04-I07) |
| Dzień 4 | Testy integracji z Google Calendar (I08-I10)<br>Testy integracji z systemem powiadomień (I11-I13) |
| Dzień 5 | Testy integracji z kanałami komunikacji (I14-I16) |

### Faza 3: Testy wydajnościowe (1-2 dni)

| Dzień | Aktywność |
|-------|-----------|
| Dzień 6 | Testy obciążeniowe (P01-P03) |
| Dzień 7 | Testy limitów (P04-P06) |

### Faza 4: Testy użyteczności (2-3 dni)

| Dzień | Aktywność |
|-------|-----------|
| Dzień 8 | Testy z udziałem zespołu NovaHouse (U01-U03) |
| Dzień 9-10 | Testy z udziałem potencjalnych klientów (U04-U06) |

### Faza 5: Testy akceptacyjne (1-2 dni)

| Dzień | Aktywność |
|-------|-----------|
| Dzień 11 | Testy zgodności z wymaganiami (A01-A03)<br>Testy scenariuszowe (A04-A06) |
| Dzień 12 | Testy akceptacji użytkownika (A07-A09) |

## Najlepsze praktyki

### Przygotowanie do testów

- Przygotuj środowisko testowe przed rozpoczęciem testów
- Przygotuj dane testowe, w tym przykładowe pytania, dane kontaktowe, terminy spotkań
- Przygotuj narzędzia do testowania, w tym narzędzia do automatyzacji testów, narzędzia do monitorowania wydajności
- Przygotuj dokumentację testową, w tym przypadki testowe, scenariusze testowe, raporty z testów

### Przeprowadzanie testów

- Przeprowadzaj testy w kolejności: funkcjonalne, integracyjne, wydajnościowe, użyteczności, akceptacyjne
- Dokumentuj wszystkie znalezione błędy
- Priorytetyzuj błędy według ich wagi i wpływu na użytkownika
- Weryfikuj poprawki błędów przed przejściem do kolejnej fazy testów

### Raportowanie wyników

- Przygotuj raport z testów po każdej fazie
- Raport powinien zawierać:
  - Podsumowanie wykonanych testów
  - Listę znalezionych błędów
  - Statystyki (liczba testów, liczba błędów, procent sukcesu)
  - Rekomendacje
- Przedstaw raport zespołowi deweloperów i kierownictwu NovaHouse

### Ciągłe doskonalenie

- Zbieraj opinie użytkowników po wdrożeniu
- Monitoruj wydajność chatbota w środowisku produkcyjnym
- Regularnie aktualizuj bazę wiedzy na podstawie nowych pytań
- Planuj regularne testy regresji po każdej aktualizacji

---

Przygotował: Michał Marini  
Data: 8 lipca 2025
