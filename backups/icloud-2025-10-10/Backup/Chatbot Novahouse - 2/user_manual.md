# Instrukcja obsługi i zarządzania chatbotem NovaHouse

## Spis treści

1. [Wprowadzenie](#1-wprowadzenie)
2. [Panel administracyjny](#2-panel-administracyjny)
3. [Zarządzanie bazą wiedzy](#3-zarządzanie-bazą-wiedzy)
4. [Obsługa rozmów przekazanych](#4-obsługa-rozmów-przekazanych)
5. [Integracja z monday.com](#5-integracja-z-mondaycom)
6. [Analiza wydajności chatbota](#6-analiza-wydajności-chatbota)
7. [Rozwiązywanie typowych problemów](#7-rozwiązywanie-typowych-problemów)
8. [Najczęściej zadawane pytania](#8-najczęściej-zadawane-pytania)

## 1. Wprowadzenie

### 1.1. Cel dokumentu

Niniejsza instrukcja ma na celu dostarczenie zespołowi NovaHouse niezbędnej wiedzy do efektywnego zarządzania chatbotem. Dokument został przygotowany z myślą o osobach bez wcześniejszego doświadczenia w obsłudze systemów chatbotowych.

### 1.2. Przegląd funkcjonalności chatbota

Chatbot NovaHouse to inteligentny asystent, który:
- Odpowiada na pytania klientów dotyczące oferty firmy
- Zbiera dane kontaktowe potencjalnych klientów
- Automatycznie tworzy leady w systemie monday.com
- Przekazuje rozmowy do konsultantów w przypadku złożonych zapytań
- Działa na stronie internetowej i w mediach społecznościowych

### 1.3. Role i odpowiedzialności

W systemie chatbota wyróżniamy następujące role:

**Administrator** - osoba odpowiedzialna za:
- Konfigurację chatbota
- Zarządzanie bazą wiedzy
- Monitorowanie wydajności
- Rozwiązywanie problemów technicznych

**Konsultant** - osoba odpowiedzialna za:
- Obsługę rozmów przekazanych przez chatbota
- Kontakt z potencjalnymi klientami
- Udzielanie specjalistycznych odpowiedzi

**Menedżer** - osoba odpowiedzialna za:
- Analizę raportów i statystyk
- Podejmowanie decyzji o rozwoju chatbota
- Ocenę efektywności chatbota

## 2. Panel administracyjny

### 2.1. Logowanie do panelu

1. Otwórz przeglądarkę i przejdź do adresu: `https://admin.novahouse-chatbot.pl`
2. Wprowadź swoje dane logowania (login i hasło)
3. Kliknij przycisk "Zaloguj się"

![Panel logowania](images/login_panel.png)

### 2.2. Interfejs panelu administracyjnego

Po zalogowaniu zobaczysz główny panel administracyjny składający się z następujących sekcji:

1. **Pulpit** - przegląd najważniejszych statystyk i informacji
2. **Rozmowy** - lista aktywnych i zakończonych rozmów
3. **Baza wiedzy** - zarządzanie odpowiedziami chatbota
4. **Integracje** - konfiguracja integracji z zewnętrznymi systemami
5. **Statystyki** - szczegółowe raporty i analizy
6. **Ustawienia** - konfiguracja chatbota i zarządzanie użytkownikami

![Panel administracyjny](images/admin_panel.png)

### 2.3. Podstawowe ustawienia

#### 2.3.1. Zmiana hasła

1. Kliknij na swoją nazwę użytkownika w prawym górnym rogu
2. Wybierz opcję "Moje konto"
3. Kliknij przycisk "Zmień hasło"
4. Wprowadź aktualne hasło oraz nowe hasło (dwukrotnie)
5. Kliknij "Zapisz zmiany"

#### 2.3.2. Zarządzanie użytkownikami

1. Przejdź do sekcji "Ustawienia"
2. Wybierz zakładkę "Użytkownicy"
3. Aby dodać nowego użytkownika:
   - Kliknij przycisk "Dodaj użytkownika"
   - Wypełnij formularz (imię, nazwisko, email, rola)
   - Kliknij "Zapisz"
4. Aby edytować istniejącego użytkownika:
   - Kliknij ikonę edycji przy wybranym użytkowniku
   - Wprowadź zmiany
   - Kliknij "Zapisz"

#### 2.3.3. Konfiguracja godzin pracy

1. Przejdź do sekcji "Ustawienia"
2. Wybierz zakładkę "Godziny pracy"
3. Ustaw godziny pracy dla każdego dnia tygodnia
4. Zaznacz opcję "Automatyczne przekazywanie rozmów poza godzinami pracy" (jeśli potrzebne)
5. Kliknij "Zapisz zmiany"

## 3. Zarządzanie bazą wiedzy

### 3.1. Struktura bazy wiedzy

Baza wiedzy chatbota składa się z:
- **Intencji** - co użytkownik chce osiągnąć (np. "zapytanie_o_pakiety")
- **Wypowiedzi** - przykładowe zdania wyrażające daną intencję
- **Encji** - kluczowe informacje w wypowiedziach (np. "pakiet_wykonczeniowy")
- **Odpowiedzi** - treści, które chatbot prezentuje użytkownikowi

### 3.2. Przeglądanie bazy wiedzy

1. Przejdź do sekcji "Baza wiedzy"
2. Zobaczysz listę wszystkich intencji
3. Kliknij na wybraną intencję, aby zobaczyć szczegóły:
   - Przykładowe wypowiedzi
   - Powiązane encje
   - Skonfigurowane odpowiedzi

![Przeglądanie bazy wiedzy](images/knowledge_base.png)

### 3.3. Dodawanie nowych odpowiedzi

1. Przejdź do sekcji "Baza wiedzy"
2. Wybierz intencję, do której chcesz dodać odpowiedź
3. Kliknij przycisk "Dodaj odpowiedź"
4. Wypełnij formularz:
   - Treść odpowiedzi
   - Warunki wyświetlania (opcjonalnie)
   - Przyciski szybkiej odpowiedzi (opcjonalnie)
5. Kliknij "Zapisz"

### 3.4. Edycja istniejących odpowiedzi

1. Przejdź do sekcji "Baza wiedzy"
2. Wybierz intencję zawierającą odpowiedź do edycji
3. Znajdź odpowiedź na liście i kliknij ikonę edycji
4. Wprowadź zmiany
5. Kliknij "Zapisz"

### 3.5. Testowanie odpowiedzi

1. Przejdź do sekcji "Baza wiedzy"
2. Kliknij przycisk "Tryb testowy" w prawym górnym rogu
3. Wpisz przykładowe pytanie w polu tekstowym
4. Kliknij "Testuj"
5. System pokaże:
   - Rozpoznaną intencję
   - Wykryte encje
   - Wybraną odpowiedź

![Testowanie odpowiedzi](images/test_mode.png)

## 4. Obsługa rozmów przekazanych

### 4.1. Powiadomienia o nowych rozmowach

Gdy chatbot przekaże rozmowę do konsultanta:
1. Otrzymasz powiadomienie email
2. Zobaczysz powiadomienie w panelu administracyjnym
3. Jeśli skonfigurowano, otrzymasz powiadomienie w monday.com

### 4.2. Przejmowanie rozmowy

1. Przejdź do sekcji "Rozmowy"
2. Znajdź rozmowę oznaczoną jako "Oczekująca" i kliknij na nią
3. Kliknij przycisk "Przejmij rozmowę"
4. System poinformuje użytkownika, że konsultant dołączył do rozmowy

![Przejmowanie rozmowy](images/take_conversation.png)

### 4.3. Prowadzenie rozmowy

1. Po przejęciu rozmowy zobaczysz historię konwersacji użytkownika z chatbotem
2. Wpisz swoją odpowiedź w polu tekstowym na dole
3. Możesz korzystać z gotowych szablonów odpowiedzi (przycisk "Szablony")
4. Kliknij "Wyślij" lub naciśnij Enter

### 4.4. Korzystanie z informacji o kliencie

Podczas rozmowy masz dostęp do:
1. Historii konwersacji
2. Danych kontaktowych (jeśli zostały podane)
3. Informacji o zainteresowaniach klienta
4. Notatek z poprzednich rozmów (jeśli istnieją)

Te informacje są widoczne w panelu bocznym po prawej stronie.

### 4.5. Zakończenie rozmowy

1. Po udzieleniu wszystkich niezbędnych informacji kliknij przycisk "Zakończ rozmowę"
2. Wypełnij krótki formularz podsumowujący:
   - Status rozmowy (np. "Lead pozyskany", "Wymaga follow-up")
   - Notatki dla zespołu
   - Priorytet follow-up (opcjonalnie)
3. Kliknij "Zapisz i zakończ"

## 5. Integracja z monday.com

### 5.1. Przeglądanie leadów w monday.com

1. Zaloguj się do monday.com
2. Przejdź do tablicy "Leady z chatbota"
3. Zobaczysz listę wszystkich leadów pozyskanych przez chatbota
4. Każdy lead zawiera:
   - Dane kontaktowe
   - Źródło (np. strona www, Facebook)
   - Zainteresowania (np. pakiet wykończeniowy, dom pasywny)
   - Priorytet
   - Status

![Leady w monday.com](images/monday_leads.png)

### 5.2. Aktualizacja statusu leadów

1. W monday.com kliknij na lead, który chcesz zaktualizować
2. Zmień status w kolumnie "Status" (np. z "Nowy" na "W kontakcie")
3. Dodaj notatki w kolumnie "Notatki"
4. System automatycznie zapisze zmiany

### 5.3. Przypisywanie zadań

1. W monday.com kliknij na lead, dla którego chcesz utworzyć zadanie
2. Kliknij przycisk "+" w kolumnie "Zadania"
3. Wypełnij formularz:
   - Tytuł zadania
   - Opis
   - Osoba odpowiedzialna
   - Termin wykonania
4. Kliknij "Zapisz"

### 5.4. Rozwiązywanie problemów z integracją

Jeśli zauważysz, że leady nie są prawidłowo przekazywane do monday.com:

1. Sprawdź status integracji w panelu administracyjnym chatbota:
   - Przejdź do sekcji "Integracje"
   - Wybierz "monday.com"
   - Sprawdź status połączenia
2. Jeśli status pokazuje błąd:
   - Sprawdź poprawność tokenu API
   - Upewnij się, że struktura tablicy w monday.com nie została zmieniona
   - Kliknij przycisk "Testuj połączenie"
3. Jeśli problem nie ustępuje, skontaktuj się z administratorem systemu

## 6. Analiza wydajności chatbota

### 6.1. Dostęp do statystyk

1. Przejdź do sekcji "Statystyki" w panelu administracyjnym
2. Wybierz zakres dat dla analizy
3. Kliknij "Generuj raport"

### 6.2. Kluczowe wskaźniki wydajności

W sekcji statystyk znajdziesz następujące wskaźniki:

1. **Liczba rozmów** - całkowita liczba interakcji z chatbotem
2. **Średni czas rozmowy** - przeciętny czas trwania konwersacji
3. **Wskaźnik rozpoznania intencji** - procent poprawnie rozpoznanych zapytań
4. **Wskaźnik konwersji** - procent rozmów zakończonych pozyskaniem leada
5. **Wskaźnik przekazania** - procent rozmów przekazanych do konsultanta
6. **Najczęstsze intencje** - ranking popularnych tematów rozmów
7. **Najczęstsze nierozpoznane zapytania** - pytania, których chatbot nie zrozumiał

![Panel statystyk](images/statistics.png)

### 6.3. Generowanie raportów

1. Przejdź do sekcji "Statystyki"
2. Ustaw parametry raportu:
   - Zakres dat
   - Typ raportu (np. "Wydajność chatbota", "Analiza leadów")
   - Format (PDF, Excel, CSV)
3. Kliknij "Generuj raport"
4. Pobierz wygenerowany raport lub wyślij go emailem

### 6.4. Interpretacja danych

**Wskaźnik rozpoznania intencji:**
- Powyżej 85% - bardzo dobry
- 70-85% - dobry
- Poniżej 70% - wymaga poprawy bazy wiedzy

**Wskaźnik konwersji:**
- Powyżej 25% - bardzo dobry
- 15-25% - dobry
- Poniżej 15% - wymaga optymalizacji

**Wskaźnik przekazania:**
- Poniżej 15% - bardzo dobry
- 15-30% - dobry
- Powyżej 30% - chatbot może wymagać rozszerzenia bazy wiedzy

## 7. Rozwiązywanie typowych problemów

### 7.1. Chatbot nie odpowiada poprawnie

**Problem:** Chatbot udziela nieprawidłowych lub niezwiązanych z tematem odpowiedzi.

**Rozwiązanie:**
1. Sprawdź, czy pytanie zostało poprawnie rozpoznane:
   - Przejdź do sekcji "Baza wiedzy"
   - Użyj trybu testowego, aby sprawdzić rozpoznaną intencję
2. Jeśli intencja jest niepoprawna:
   - Dodaj nowe przykładowe wypowiedzi do właściwej intencji
   - Upewnij się, że nie ma konfliktu między podobnymi intencjami
3. Jeśli intencja jest poprawna, ale odpowiedź nieodpowiednia:
   - Edytuj odpowiedź dla danej intencji
   - Dodaj warunki wyświetlania, jeśli to konieczne

### 7.2. Problemy z przekazywaniem rozmów

**Problem:** Rozmowy nie są przekazywane do konsultantów lub przekazywanie trwa zbyt długo.

**Rozwiązanie:**
1. Sprawdź ustawienia przekazywania:
   - Przejdź do sekcji "Ustawienia"
   - Wybierz zakładkę "Przekazywanie rozmów"
   - Upewnij się, że warunki przekazywania są poprawne
2. Sprawdź dostępność konsultantów:
   - Upewnij się, że są zalogowani konsultanci
   - Sprawdź ich status (dostępny/zajęty)
3. Sprawdź powiadomienia:
   - Upewnij się, że powiadomienia email są włączone
   - Sprawdź, czy adresy email są poprawne

### 7.3. Problemy z integracją monday.com

**Problem:** Leady nie są przekazywane do monday.com lub są przekazywane z niepełnymi danymi.

**Rozwiązanie:**
1. Sprawdź status integracji:
   - Przejdź do sekcji "Integracje"
   - Wybierz "monday.com"
   - Sprawdź logi błędów
2. Weryfikacja konfiguracji:
   - Sprawdź poprawność tokenu API
   - Upewnij się, że mapowanie pól jest poprawne
3. Testowanie połączenia:
   - Kliknij przycisk "Testuj połączenie"
   - Sprawdź wynik testu

### 7.4. Chatbot nie rozpoznaje specyficznych terminów branżowych

**Problem:** Chatbot nie rozumie specjalistycznych terminów związanych z wykończeniem wnętrz.

**Rozwiązanie:**
1. Dodaj nowe encje:
   - Przejdź do sekcji "Baza wiedzy"
   - Wybierz zakładkę "Encje"
   - Dodaj nową encję lub rozszerz istniejącą
2. Dodaj synonimy:
   - Dla każdego terminu branżowego dodaj popularne synonimy
   - Uwzględnij różne formy gramatyczne
3. Trenuj model:
   - Po wprowadzeniu zmian kliknij przycisk "Trenuj model"
   - Poczekaj na zakończenie procesu trenowania

## 8. Najczęściej zadawane pytania

### 8.1. Ogólne

**P: Jak często należy aktualizować bazę wiedzy chatbota?**

O: Zalecamy przegląd i aktualizację bazy wiedzy co najmniej raz w miesiącu. Dodatkowo, po każdej znaczącej zmianie w ofercie firmy (np. nowe pakiety, zmiana cen) należy natychmiast zaktualizować odpowiednie odpowiedzi.

**P: Czy chatbot może obsługiwać rozmowy w języku angielskim?**

O: Tak, chatbot może obsługiwać rozmowy w języku angielskim, jeśli zostanie odpowiednio skonfigurowany. Wymaga to dodania angielskich intencji, wypowiedzi i odpowiedzi w bazie wiedzy.

**P: Czy można zmienić wygląd widgetu chatbota na stronie?**

O: Tak, wygląd chatbota można dostosować w sekcji "Ustawienia" > "Wygląd". Możesz zmienić kolory, czcionki, ikony oraz teksty powitalne.

### 8.2. Techniczne

**P: Co zrobić, gdy chatbot przestanie działać na stronie?**

O: Sprawdź następujące elementy:
1. Czy skrypt chatbota jest poprawnie załadowany na stronie (sprawdź konsolę przeglądarki)
2. Czy serwer chatbota działa (sprawdź status w panelu administracyjnym)
3. Czy nie ma problemów z połączeniem internetowym
4. Jeśli problem nie ustępuje, skontaktuj się z administratorem systemu

**P: Jak często tworzone są kopie zapasowe danych?**

O: Automatyczne kopie zapasowe są tworzone codziennie i przechowywane przez 30 dni. Dodatkowo, przed każdą większą aktualizacją systemu tworzona jest manualna kopia zapasowa.

**P: Czy można eksportować dane z chatbota?**

O: Tak, w sekcji "Ustawienia" > "Eksport danych" możesz wyeksportować:
- Historię rozmów
- Bazę wiedzy
- Statystyki
- Dane leadów

### 8.3. Operacyjne

**P: Jak długo konsultant powinien odpowiedzieć na przekazaną rozmowę?**

O: Zalecamy odpowiadanie na przekazane rozmowy w ciągu maksymalnie 5 minut w godzinach pracy. Jeśli nie jest to możliwe, system automatycznie poinformuje użytkownika o przewidywanym czasie oczekiwania.

**P: Czy można zaplanować automatyczne odpowiedzi poza godzinami pracy?**

O: Tak, w sekcji "Ustawienia" > "Godziny pracy" możesz skonfigurować automatyczne odpowiedzi dla rozmów rozpoczętych poza godzinami pracy. Możesz ustawić różne odpowiedzi dla różnych dni tygodnia i świąt.

**P: Jak często należy analizować statystyki chatbota?**

O: Zalecamy cotygodniowy przegląd podstawowych statystyk oraz miesięczną szczegółową analizę wszystkich wskaźników wydajności. Po wprowadzeniu znaczących zmian w bazie wiedzy warto również przeanalizować statystyki po 1-2 tygodniach, aby ocenić wpływ zmian.
