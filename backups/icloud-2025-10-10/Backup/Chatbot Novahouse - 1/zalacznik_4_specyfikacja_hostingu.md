# Załącznik nr 4 - Specyfikacja techniczna hostingu

## Specyfikacja techniczna hostingu Cyber Folks WP-GO

### Podstawowe informacje

| Kategoria | Wartość |
|-----------|---------|
| Nazwa produktu | wp_GO! / oekpdgkroa |
| Okres | 12 miesięcy (23 lis 2023 - 22 lis 2024) |
| Typ | Odnowienie |

### Parametry cenowe

| Parametr | Wartość |
|----------|---------|
| Cena (netto) | 749,00 PLN |
| Cena (brutto) | 921,27 PLN |

### Parametry techniczne

| Parametr | Wartość |
|----------|---------|
| Maks. PHP Memory limit | 512.0 MB |
| Liczba plików na serwerze | 1000000 |
| SSH | tak |
| Obsługiwane wersje PHP | od 5.2+ |
| Liczba baz danych MySQL | bez limitu |
| Liczba kont e-mail | bez limitu |
| Transfer danych (m-c) [GB] | bez limitu |
| Liczba domen obsługiwanych | 10 |
| Pojemność konta [GB] | 20.0 GB |

### Analiza kompatybilności z Chatfuel

Hosting Cyber Folks WP-GO jest w pełni wystarczający do wdrożenia chatbota Chatfuel na stronie NovaHouse. Poniżej przedstawiamy analizę kompatybilności:

#### Wymagania Chatfuel vs. parametry hostingu

| Wymaganie Chatfuel | Parametr hostingu | Kompatybilność |
|--------------------|-------------------|----------------|
| Obsługa JavaScript | Pełna obsługa JS | ✅ Kompatybilne |
| Możliwość edycji kodu strony | WordPress + SSH | ✅ Kompatybilne |
| Limit pamięci PHP | 512 MB | ✅ Kompatybilne (wystarczające) |
| Wersja PHP | 5.2+ | ✅ Kompatybilne |
| Przestrzeń dyskowa | 20 GB | ✅ Kompatybilne (wystarczające) |
| Bazy danych | Bez limitu | ✅ Kompatybilne |

#### Uzasadnienie kompatybilności

1. **Chatfuel działa jako zewnętrzna usługa** - główny kod chatbota jest hostowany na serwerach Chatfuel, co oznacza minimalne obciążenie dla hostingu NovaHouse.

2. **Integracja wymaga minimalnych zmian w kodzie strony** - na stronie NovaHouse będzie tylko niewielki fragment kodu JavaScript do osadzenia widgetu, co nie wpłynie znacząco na wydajność strony.

3. **Brak potrzeby instalowania dodatkowych baz danych** - Chatfuel nie wymaga dodatkowych baz danych na hostingu klienta.

4. **Hosting WP-GO jest zoptymalizowany pod WordPress** - co dodatkowo ułatwi integrację, ponieważ Chatfuel oferuje dedykowane wtyczki i instrukcje dla WordPress.

### Instrukcja integracji z WordPress na hostingu Cyber Folks

1. **Metoda 1: Użycie wtyczki "Insert Headers and Footers"**
   - Zainstaluj wtyczkę "Insert Headers and Footers" w panelu WordPress
   - Przejdź do "Settings" > "Insert Headers and Footers"
   - Wklej kod widgetu Chatfuel w sekcji "Scripts in Footer"
   - Zapisz zmiany

2. **Metoda 2: Edycja szablonu przez SSH**
   - Połącz się z serwerem przez SSH (dostępne w hostingu)
   - Przejdź do katalogu z aktywnym motywem WordPress
   - Edytuj plik footer.php
   - Wklej kod widgetu Chatfuel przed zamykającym tagiem `</body>`
   - Zapisz zmiany

### Rekomendacje dotyczące hostingu

1. **Aktualizacja PHP** - zalecamy aktualizację PHP do najnowszej stabilnej wersji (np. PHP 8.1), aby zapewnić najlepszą wydajność i bezpieczeństwo.

2. **Regularne kopie zapasowe** - zalecamy konfigurację automatycznych kopii zapasowych przed wdrożeniem chatbota, aby zabezpieczyć się przed ewentualnymi problemami.

3. **Monitoring wydajności** - zalecamy monitorowanie wydajności strony po wdrożeniu chatbota, aby upewnić się, że nie wpływa on negatywnie na szybkość ładowania strony.

4. **Certyfikat SSL** - upewnij się, że strona korzysta z certyfikatu SSL (HTTPS), co jest wymagane do poprawnego działania niektórych funkcji Chatfuel.

### Podsumowanie

Hosting Cyber Folks WP-GO spełnia wszystkie wymagania techniczne do wdrożenia chatbota Chatfuel na stronie NovaHouse. Nie ma potrzeby zmiany hostingu ani zakupu dodatkowych usług. Integracja będzie przebiegać sprawnie i nie powinna wpłynąć negatywnie na wydajność strony.
