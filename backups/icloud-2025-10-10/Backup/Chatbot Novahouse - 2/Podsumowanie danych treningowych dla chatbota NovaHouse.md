# Podsumowanie danych treningowych dla chatbota NovaHouse

## Zawartość pakietu danych treningowych

Przygotowany pakiet danych treningowych dla chatbota NovaHouse zawiera następujące elementy:

1. **Baza wiedzy (baza_wiedzy.md)**
   - Ustrukturyzowane pary pytanie-odpowiedź (Q&A)
   - Informacje o firmie, ofercie, procesie realizacji
   - Szczegółowe opisy pakietów wykończeniowych
   - Informacje o domach pasywnych
   - Dane dotyczące rabatów, gwarancji i innych korzyści

2. **Intencje NLU (intencje.md)**
   - 13 głównych intencji z ponad 30 przykładowymi wypowiedziami dla każdej
   - Różnorodne konstrukcje zdaniowe i sformułowania
   - Pokrycie wszystkich kluczowych obszarów komunikacji z klientem

3. **Encje NLU (encje.md)**
   - 5 głównych typów encji: pakiet_wykonczeniowy, metraz_lokalu, typ_nieruchomosci, miasto, element_wykonczenia
   - Liczne warianty dla każdej encji
   - Pokrycie wszystkich istotnych parametrów dla branży wykończenia wnętrz

4. **Przykładowe odpowiedzi chatbota (odpowiedzi.md)**
   - Standardowe odpowiedzi dla każdej intencji (po 3 warianty)
   - Odpowiedzi na pytania uzupełniające
   - Przykłady przekierowania do formularza kontaktowego, konsultacji z architektem i działu sprzedaży
   - Odpowiedzi na pytania edge case (nietypowe, dwuznaczne, agresywne)

5. **Scenariusze testowe (scenariusze_testowe.md)**
   - 6 kompletnych scenariuszy konwersacji
   - Typowe ścieżki użytkownika
   - Scenariusze edge case
   - Przykłady wieloetapowych interakcji

## Sugerowane dodatkowe intencje i encje

Na podstawie analizy danych i typowych interakcji z klientami, sugerujemy rozważenie dodania następujących intencji:

1. **pytanie_o_portfolio** - pytania o zdjęcia, wizualizacje i przykłady zrealizowanych projektów
2. **pytanie_o_finansowanie** - pytania o możliwości rozłożenia płatności na raty, kredyty, leasing
3. **pytanie_o_smart_home** - pytania o inteligentne rozwiązania dla domu
4. **pytanie_o_ekologiczne_rozwiazania** - pytania o materiały ekologiczne, zrównoważone budownictwo
5. **pytanie_o_pozwolenia** - pytania o formalności, pozwolenia na budowę/remont

Sugerowane dodatkowe encje:

1. **styl_wnetrza** - np. skandynawski, industrialny, minimalistyczny, klasyczny
2. **material_wykonczeniowy** - np. drewno, płytki, kamień, szkło, beton
3. **budzet** - przedziały cenowe, np. do 50 tys., 50-100 tys., powyżej 100 tys.

## Wskazówki implementacyjne

1. **Priorytetyzacja intencji**
   - Najważniejsze intencje to: zapytanie_o_pakiety, pytanie_o_ceny, darmowa_wycena, umowienie_konsultacji
   - Te intencje powinny mieć najwyższy priorytet w systemie rozpoznawania

2. **Obsługa kontekstu**
   - Chatbot powinien pamiętać wcześniej podane informacje (np. metraż, wybrany pakiet)
   - Warto zaimplementować mechanizm śledzenia kontekstu rozmowy

3. **Przekierowanie do człowieka**
   - Należy zdefiniować sytuacje, w których chatbot powinien przekazać rozmowę konsultantowi
   - Przykłady: skomplikowane pytania techniczne, prośby o szczegółową wycenę, niezadowolenie klienta

4. **Personalizacja**
   - Warto dostosować ton komunikacji do etapu lejka sprzedażowego
   - Dla nowych klientów: informacyjny i edukacyjny
   - Dla zainteresowanych: bardziej perswazyjny
   - Dla zdecydowanych: konkretny i zorientowany na działanie

5. **Rozszerzenia**
   - Warto rozważyć dodanie modułu kalkulatora kosztów
   - Możliwość umówienia konsultacji bezpośrednio przez chatbota
   - Integracja z systemem CRM do śledzenia leadów

## Format danych

Wszystkie dane zostały przygotowane w formacie Markdown, który jest czytelny dla człowieka i łatwy do konwersji na inne formaty. W zależności od wybranego systemu chatbotowego, dane mogą wymagać konwersji na:

- JSON (dla większości nowoczesnych platform chatbotowych)
- CSV (dla prostszych systemów lub importu do arkuszy kalkulacyjnych)
- YAML (dla niektórych systemów opartych na regułach)

Przykładowa konwersja intencji do formatu JSON:

```json
{
  "intents": [
    {
      "name": "zapytanie_o_pakiety",
      "examples": [
        "Jakie pakiety wykończeniowe oferujecie?",
        "Chciałbym poznać dostępne pakiety wykończeniowe",
        "Czy możesz mi powiedzieć, jakie macie pakiety?"
      ]
    },
    {
      "name": "pytanie_o_ceny",
      "examples": [
        "Ile kosztuje wykończenie mieszkania pod klucz?",
        "Jaka jest cena pakietu Waniliowego?",
        "Ile kosztuje pakiet Cynamonowy?"
      ]
    }
  ]
}
```

## Zalecenia dotyczące testowania

1. **Testy jednostkowe**
   - Testowanie rozpoznawania pojedynczych intencji i encji
   - Sprawdzenie poprawności odpowiedzi dla prostych zapytań

2. **Testy scenariuszowe**
   - Testowanie pełnych ścieżek konwersacji
   - Weryfikacja zachowania chatbota w dłuższych interakcjach

3. **Testy edge case**
   - Testowanie nietypowych pytań i sytuacji
   - Sprawdzenie odporności na literówki i błędy językowe

4. **Testy A/B**
   - Porównanie różnych wariantów odpowiedzi
   - Optymalizacja konwersji (np. umówienie konsultacji, wypełnienie formularza)

5. **Testy użyteczności**
   - Testy z udziałem rzeczywistych użytkowników
   - Zbieranie feedbacku i iteracyjne ulepszanie chatbota
