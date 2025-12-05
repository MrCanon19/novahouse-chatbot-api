# System Kwalifikacji Klienta (admin) i formularz kwalifikacyjny

## 1. Panel administratora – System Kwalifikacji Klienta (`/admin`)
- **Cel:** zaawansowane zarządzanie kwalifikacją leadów oraz nadzór nad systemem.
- **Typowe użycie:** analiza wskaźników, przegląd wyników A/B testów, wykonywanie backupów, szybka diagnostyka.
- **Główne funkcje:**
  - Widgety analityczne (podgląd trendów, wskaźniki skuteczności kwalifikacji).
  - Panel A/B testingu (wyniki eksperymentów i szybkie przełączanie wariantów).
  - Akcje utrzymaniowe: podgląd statusu backupów, logów, monitoringu.
- **Jak używać (skrót):**
  1) Wejdź na `https://glass-core-467907-e9.ey.r.appspot.com/admin` (po zalogowaniu, jeśli wymagane).
  2) W zakładkach/sekcjach sprawdź: metryki kwalifikacji, wyniki A/B, statusy backupów.
  3) W razie błędów/alertów skorzystaj z dostępnych widoków diagnostycznych.

## 2. Formularz kwalifikacyjny dla klientów (`/qualification`)
- **Cel:** zebranie szczegółowych informacji od potencjalnych klientów i dobór pakietu.
- **Typowe użycie:** onboarding leadów, automatyczne rekomendacje ofert, integracja z CRM.
- **Główne funkcje:**
  - Formularz z pytaniami biznesowymi/technologicznymi (zakres projektu, budżet, timeline).
  - Generowanie rekomendacji pakietów na podstawie odpowiedzi.
  - Integracja z CRM – zapis pozyskanych danych i statusu kwalifikacji.
- **Jak używać (skrót):**
  1) Otwórz `https://glass-core-467907-e9.ey.r.appspot.com/qualification`.
  2) Wypełnij formularz krok po kroku; pola obowiązkowe są walidowane na bieżąco.
  3) Po wysłaniu sprawdź rekomendację pakietu; dane trafiają do CRM do dalszej obsługi.

## 3. Dokumentacja API (Swagger UI)
- **Cel:** interaktywna dokumentacja i testowanie endpointów API w przeglądarce.
- **Adres produkcyjny:** `https://glass-core-467907-e9.ey.r.appspot.com/docs` (Swagger UI z pełną specyfikacją OpenAPI).
- **Jak używać (skrót):**
  1) Wejdź na `/docs` i wybierz interesujący endpoint z listy.
  2) Kliknij **Authorize** (jeśli wymagane) i podaj klucz/sekret.
  3) W sekcji „Try it out” uzupełnij parametry i wykonaj zapytanie, żeby zobaczyć odpowiedź API.
- **Przydatne linki powiązane:**
  - Lokalnie: `http://localhost:5000/api-docs` (po uruchomieniu aplikacji).
  - Specyfikacja OpenAPI: `src/docs/openapi.yaml` (można edytować, aby dodać nowe endpointy).
