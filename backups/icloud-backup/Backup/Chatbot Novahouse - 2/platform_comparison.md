# Porównanie platform chatbotowych dla NovaHouse

## Wprowadzenie

Niniejszy dokument zawiera porównanie najpopularniejszych platform chatbotowych, które mogą zostać wykorzystane do wdrożenia chatbota dla firmy NovaHouse. Analiza uwzględnia specyficzne wymagania firmy:
- Obsługa zapytań klientów z różnych kanałów
- Odciążenie konsultantów
- Automatyczne zapisywanie leadów do obsługi
- Możliwość integracji z monday.com
- Planowane wdrożenie: wrzesień/październik 2025
- Brak doświadczenia zespołu w zarządzaniu chatbotami

## Porównanie platform

### 1. Dialogflow (Google)

**Zalety:**
- Zaawansowane rozpoznawanie języka naturalnego (NLU) oparte na AI Google
- Łatwa integracja z wieloma kanałami komunikacji (strona www, Facebook, WhatsApp, Telegram)
- Gotowe integracje z popularnymi systemami CRM
- Możliwość integracji z monday.com przez Zapier lub dedykowane API
- Intuicyjny interfejs dla osób bez doświadczenia technicznego
- Możliwość tworzenia złożonych scenariuszy konwersacji
- Wsparcie dla języka polskiego

**Wady:**
- Ograniczenia w darmowym planie (limit zapytań)
- Koszty rosną wraz z liczbą zapytań w planach płatnych
- Mniej elastyczny dla bardzo zaawansowanych przypadków użycia
- Przechowywanie danych na serwerach Google (aspekt RODO)

**Koszty:**
- Plan Essential: od $0.007 za zapytanie (pierwsze 100 zapytań dziennie za darmo)
- Plan Advanced: od $0.02 za zapytanie + dodatkowe funkcje
- Szacowany miesięczny koszt dla średniej firmy: 500-1500 PLN

**Integracja z monday.com:**
- Przez Zapier (automatyzacja bez kodowania)
- Przez dedykowane API (wymaga programisty)
- Możliwość automatycznego tworzenia zadań w monday.com na podstawie rozmów z chatbotem

### 2. Botpress

**Zalety:**
- Open-source z możliwością hostowania na własnych serwerach
- Pełna kontrola nad danymi (zgodność z RODO)
- Wizualny edytor przepływów konwersacji
- Możliwość dostosowania i rozszerzenia funkcjonalności
- Dobra dokumentacja i aktywna społeczność
- Możliwość integracji z monday.com przez webhooks
- Jednorazowy koszt wdrożenia zamiast opłat subskrypcyjnych (w wersji self-hosted)

**Wady:**
- Wymaga więcej wiedzy technicznej do wdrożenia i utrzymania
- Mniej gotowych integracji niż komercyjne rozwiązania
- Wsparcie dla języka polskiego wymaga dodatkowej konfiguracji
- Mniej zaawansowane NLU w porównaniu do rozwiązań Google czy Microsoft

**Koszty:**
- Wersja open-source: za darmo (koszty hostingu we własnym zakresie)
- Botpress Cloud: od $50/miesiąc (ok. 200 PLN)
- Szacowany całkowity koszt wdrożenia: 10,000-20,000 PLN (jednorazowo) + hosting

**Integracja z monday.com:**
- Przez webhooks (wymaga programisty)
- Przez dedykowane API (wymaga programisty)
- Możliwość tworzenia niestandardowych integracji

### 3. Microsoft Bot Framework / Power Virtual Agents

**Zalety:**
- Zaawansowane możliwości NLU dzięki LUIS (Language Understanding)
- Doskonała integracja z ekosystemem Microsoft (jeśli firma go używa)
- Gotowe konektory do wielu systemów biznesowych
- Power Automate umożliwia integrację z monday.com bez kodowania
- Skalowalne rozwiązanie dla firm każdej wielkości
- Zaawansowane funkcje analityczne
- Wsparcie dla języka polskiego

**Wady:**
- Wyższe koszty w porównaniu do niektórych alternatyw
- Złożoność ekosystemu Microsoft może być przytłaczająca
- Pełne wykorzystanie możliwości wymaga znajomości produktów Microsoft
- Przechowywanie danych na serwerach Microsoft (aspekt RODO)

**Koszty:**
- Power Virtual Agents: od $1000/miesiąc za 2000 sesji (ok. 4000 PLN)
- Bot Framework: koszty zależne od wykorzystanych usług Azure
- Szacowany miesięczny koszt: 2000-5000 PLN

**Integracja z monday.com:**
- Przez Power Automate (bez kodowania)
- Przez dedykowane API (wymaga programisty)
- Gotowe szablony przepływów pracy

### 4. Rasa

**Zalety:**
- Open-source z możliwością hostowania na własnych serwerach
- Pełna kontrola nad danymi (zgodność z RODO)
- Zaawansowane możliwości NLU, porównywalne z komercyjnymi rozwiązaniami
- Wysoka elastyczność i możliwość dostosowania
- Możliwość trenowania modeli na własnych danych
- Wsparcie dla języka polskiego
- Aktywna społeczność i dobra dokumentacja

**Wady:**
- Wymaga znacznej wiedzy technicznej do wdrożenia i utrzymania
- Stroma krzywa uczenia dla zespołów bez doświadczenia
- Wymaga więcej pracy przy początkowej konfiguracji
- Mniej gotowych integracji niż komercyjne rozwiązania

**Koszty:**
- Wersja open-source: za darmo (koszty hostingu we własnym zakresie)
- Rasa Enterprise: ceny na zapytanie (zwykle od $1000/miesiąc)
- Szacowany całkowity koszt wdrożenia: 15,000-30,000 PLN (jednorazowo) + hosting

**Integracja z monday.com:**
- Przez webhooks (wymaga programisty)
- Przez dedykowane API (wymaga programisty)
- Wymaga niestandardowego rozwoju

### 5. Chatfuel / ManyChat (specjalizacja w mediach społecznościowych)

**Zalety:**
- Specjalizacja w chatbotach dla mediów społecznościowych (Facebook, Instagram)
- Bardzo prosty w użyciu, nie wymaga wiedzy technicznej
- Szybkie wdrożenie (możliwe w ciągu kilku dni)
- Gotowe szablony dla branży nieruchomości i wykończenia wnętrz
- Dobre narzędzia do generowania i zarządzania leadami
- Integracja z popularnymi narzędziami marketingowymi

**Wady:**
- Ograniczone możliwości NLU w porównaniu do zaawansowanych platform
- Głównie skupione na mediach społecznościowych, mniej elastyczne dla strony www
- Ograniczone możliwości tworzenia złożonych scenariuszy konwersacji
- Mniej zaawansowane możliwości integracji z systemami biznesowymi

**Koszty:**
- Chatfuel: od $15/miesiąc (ok. 60 PLN) do $625/miesiąc (ok. 2500 PLN)
- ManyChat: od $15/miesiąc (ok. 60 PLN) do $250/miesiąc (ok. 1000 PLN)
- Szacowany miesięczny koszt: 250-1000 PLN

**Integracja z monday.com:**
- Przez Zapier (automatyzacja bez kodowania)
- Przez webhooks (wymaga podstawowej wiedzy technicznej)
- Ograniczone możliwości niestandardowej integracji

## Rekomendacja dla NovaHouse

Biorąc pod uwagę specyficzne wymagania NovaHouse, rekomendujemy następujące rozwiązania:

### Rekomendacja podstawowa: Dialogflow

**Uzasadnienie:**
- Najlepszy stosunek możliwości do łatwości wdrożenia i utrzymania
- Zaawansowane NLU zapewni wysoką jakość obsługi klienta
- Łatwa integracja z monday.com przez Zapier
- Intuicyjny interfejs dla zespołu bez doświadczenia
- Rozsądne koszty dla średniej wielkości firmy
- Możliwość obsługi wielu kanałów komunikacji

**Szacowany budżet wdrożenia:**
- Konfiguracja i wdrożenie: 15,000-25,000 PLN (jednorazowo)
- Miesięczne utrzymanie: 500-1500 PLN
- Integracja z monday.com: 5,000-10,000 PLN (jednorazowo)

### Alternatywa ekonomiczna: Botpress

**Uzasadnienie:**
- Niższe koszty długoterminowe (brak opłat subskrypcyjnych w wersji self-hosted)
- Pełna kontrola nad danymi i możliwość hostowania na własnych serwerach
- Wystarczające możliwości NLU dla typowych zapytań klientów
- Możliwość rozbudowy w przyszłości

**Szacowany budżet wdrożenia:**
- Konfiguracja i wdrożenie: 20,000-30,000 PLN (jednorazowo)
- Miesięczne utrzymanie: 200-500 PLN (hosting)
- Integracja z monday.com: 8,000-15,000 PLN (jednorazowo)

### Alternatywa dla mediów społecznościowych: Chatfuel + Dialogflow

**Uzasadnienie:**
- Chatfuel do obsługi zapytań z Facebooka i Instagrama
- Dialogflow do obsługi strony www i innych kanałów
- Optymalne wykorzystanie zalet obu platform
- Szybsze wdrożenie dla mediów społecznościowych

**Szacowany budżet wdrożenia:**
- Konfiguracja i wdrożenie: 20,000-35,000 PLN (jednorazowo)
- Miesięczne utrzymanie: 750-2000 PLN
- Integracja z monday.com: 8,000-15,000 PLN (jednorazowo)

## Następne kroki

1. Prezentacja porównania platform dla decydentów
2. Wybór preferowanej platformy
3. Szczegółowa specyfikacja techniczna dla wybranego rozwiązania
4. Opracowanie planu wdrożenia z harmonogramem
5. Przygotowanie materiałów szkoleniowych dla zespołu
6. Implementacja i integracja z monday.com
7. Testy i optymalizacja
8. Szkolenie zespołu
9. Uruchomienie produkcyjne

## Dodatkowe uwagi

- Niezależnie od wybranej platformy, kluczowe znaczenie ma jakość danych treningowych (już przygotowanych)
- Warto rozważyć fazowe wdrożenie (np. najpierw strona www, potem media społecznościowe)
- Rekomendujemy zaplanowanie regularnych aktualizacji bazy wiedzy chatbota
- Dla wszystkich platform należy uwzględnić koszty związane z RODO i przetwarzaniem danych osobowych
