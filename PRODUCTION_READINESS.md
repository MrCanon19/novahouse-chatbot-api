# 🚀 PRODUCTION READINESS CHECKLIST
## Nova House Chatbot API

**Data utworzenia:** 11 grudnia 2025  
**Status:** W trakcie przygotowania do produkcji  
**Cel:** Kompleksowa lista wymagań produkcyjnych zapewniających stabilność, bezpieczeństwo i zgodność z RODO

---

## 1. Warstwa błędów i stabilność

### Wymagania

Upewnij się, że:

- ✅ Każdy endpoint ma sensowne kody odpowiedzi: 2xx / 4xx / 5xx, zero 200 przy błędach
- ✅ Wyjątki z głównego flow czatu są łapane w jednym miejscu, a nie w losowych fragmentach kodu
- ✅ Logi nie wypisują całego trace dla użytkownika, tylko dla Sentry / logów technicznych

### Konkretne działania

#### Dodaj globalny error handler w `main.py`, który:

- Mapuje znane błędy biznesowe na 4xx
- Niezłapane wyjątki mapuje na 500 + prosty JSON typu:
  ```json
  {
    "error": "internal_error",
    "request_id": "..."
  }
  ```

#### Wprowadź `request_id` w każdym logu i odpowiedzi API

**Status:** ⏳ Do zrobienia

---

## 2. Walidacja wejścia i uploady

### Wymagania

Każdy endpoint typu `POST /chat`, `/leads`, `/faq-learning`:

- ✅ Walidacja schematu (Pydantic, Marshmallow albo własny validator)
- ✅ Twarde limity rozmiaru:
  - Długość wiadomości
  - Rozmiar payloadu JSON
  - Liczba kluczy

### Uploady plików

- ✅ Akceptowane tylko rozsądne typy MIME
- ✅ Brak SVG, brak HTML, brak JS
- ✅ Limit rozmiaru, np. 5 MB na plik
- ✅ Serwis uploadów nie zapisuje plików w katalogu, z którego serwujesz frontend

### Konkretne działania

#### Stwórz moduł `src/utils/validators.py` z funkcjami:

- `validate_chat_payload`
- `validate_lead_payload`
- `validate_uploaded_file`

#### Sprawdź, że testy pokrywają te ścieżki:

- `test_upload_validation`
- `test_validation`
- Dodaj testy negatywne

**Status:** ⏳ Do zrobienia

---

## 3. Bezpieczeństwo HTTP i API

### Sprawdź i popraw

#### CORS

- ✅ Whitelist konkretnych domen (prod, staging), żadnego "*"

#### CSRF

- ✅ Dla panelu webowego z cookie stosuj CSRF token
- ✅ Dla czystego API z Bearer tokenami możesz pominąć CSRF przy braku cookies

#### Headers

- ✅ `X-Content-Type-Options: nosniff`
- ✅ `X-Frame-Options: DENY` lub `SAMEORIGIN`
- ✅ `Content-Security-Policy` dla panelu admina

#### Auth

- ✅ Endpointy `analytics`, `leads`, eksporty, `FAQ learning` zabezpieczone auth, nie publiczne

### Konkretne działania

#### Dodaj moduł `src/middleware/security.py` z:

- Dodawaniem security headers
- Weryfikacją auth dla panelu i endpointów administracyjnych

**Status:** ⏳ Do zrobienia

---

## 4. Rate limiting i ochrona przed spamem

### Wymagania

Masz już przełącznik `RATE_LIMIT_ENABLED` i no-op limiter. Teraz dopnij całość:

#### Konfiguracja

- ✅ Produkcja: sensowne limity per IP / per user / per endpoint
- ✅ CI / lokalnie: `RATE_LIMIT_ENABLED=false`, wszystko działa bez 429

#### Spam

- ✅ Minimalny interwał między wiadomościami w tej samej sesji
- ✅ Blacklista IP / user_id po X naruszeniach

### Konkretne działania

#### Upewnij się, że:

- `configure_rate_limiter` jest jedynym miejscem, gdzie tworzysz limiter
- Wszystkie dekoratory limitujące biorą limiter z jednej instancji, nie tworzą własnych

**Status:** ⏳ Do zrobienia

---

## 5. Sesje, timeouty i nudges

### Cel

- ✅ Sesja wygasa po X minutach braku aktywności
- ✅ Nudge (przypomnienie) jest wysyłany raz
- ✅ Redis może paść bez wywalenia całej aplikacji

### Konkretne działania

#### Określ parametry

- `INACTIVITY_MINUTES_BEFORE_NUDGE`
- `INACTIVITY_MINUTES_BEFORE_TIMEOUT`

#### W `SessionTimeoutService`

- ✅ Priorytet: stan z DB / lokalny w testach, Redis tylko jako cache
- ✅ Jeśli Redis niedostępny, logujesz ostrzeżenie i działasz dalej

#### Dodaj cron lub background job, który:

- Czyści stare sesje z DB
- Oznacza je jako zakończone do analityki

**Status:** ⏳ Do zrobienia

---

## 6. Architektura i podział na moduły

### Docelowa, czytelna struktura

```
src/
├── main.py                 # wejście aplikacji, rejestracja blueprintów
├── api_v1.py               # rejestracja blueprintów, wersjonowanie API
│
├── routes/
│   ├── chatbot.py          # /chat, /status, health
│   ├── analytics.py        # statystyki, wykresy, eksporty
│   ├── leads.py            # leady, walidacja, eksport
│   ├── faq.py              # FAQ, faq-learning
│   └── uploads.py          # uploady plików
│
├── services/
│   ├── chat/
│   │   ├── message_handler.py
│   │   ├── conversation_state_machine.py
│   │   ├── session_timeout.py
│   │   └── rate_limiter.py
│   │
│   ├── analytics/
│   │   ├── analytics_service.py
│   │   └── advanced_analytics.py
│   │
│   ├── integrations/
│   │   ├── zencal_client.py
│   │   ├── monday_client.py
│   │   └── email_service.py
│   │
│   ├── storage/
│   │   ├── redis_service.py
│   │   └── dead_letter_queue.py
│   │
│   ├── security/
│   │   ├── file_upload_service.py
│   │   ├── i18n_service.py
│   │   └── validation_service.py
│   │
│   └── llm/
│       ├── prompt_service.py
│       ├── extraction_service.py
│       ├── summarization_service.py
│       └── regression_detector.py
│
├── middleware/
│   ├── security.py
│   ├── rate_limiting.py
│   └── cache.py
│
├── models/
│   ├── chatbot.py
│   ├── consent_audit_log.py
│   ├── followup_event.py
│   └── user.py
│
├── utils/
│   ├── polish_cities.py
│   ├── polish_declension.py
│   └── validators.py
│
├── migrations/
└── docs/
```

### Cele

- ✅ Brak cyklicznych importów
- ✅ Każdy moduł robi jedną rzecz
- ✅ `main.py` jest cienki. Nie ma logiki biznesowej

**Status:** ⏳ Częściowo zrobione, wymaga reorganizacji

---

## 7. Testy i jakość

### Wymagania

Masz dużo testów. Teraz zrób z nich tarczę, nie statystykę.

### Konkretne działania

#### Zrób smoke-set produkcyjny, który odpalasz przed deployem:

- ✅ `tests/test_api.py`
- ✅ `tests/test_chatbot.py`
- ✅ `tests/test_session_timeout.py`
- ✅ `tests/test_upload_validation.py`
- ✅ `tests/test_validation.py`

#### Dodaj choć podstawowe testy dla:

- ✅ Scenariuszy integracyjnych end-to-end z mockiem zewnętrznych usług
- ✅ Głównych ścieżek LLM (success, timeout, błąd dostawcy)

**Status:** ⏳ Częściowo zrobione, wymaga rozszerzenia

---

## 8. RODO i dane wrażliwe

To już nie jest opcja, tylko obowiązek.

### a) Inwentaryzacja danych

#### Spisz:

- ✅ Co zbierasz: imię, mail, telefon, treść czatu, pliki
- ✅ Po co: cel przetwarzania
- ✅ Jak długo: retencja
- ✅ Gdzie: baza, backupy, logi

### b) Retencja techniczna

#### Dodaj mechanizm, który:

- ✅ Po X miesiącach anonimizuje stare rozmowy
- ✅ Albo je usuwa, a zostawia tylko zagregowane statystyki

#### W modelach:

- ✅ Flagi typu `deleted_at`, `anonymized_at`

#### W logach:

- ✅ Maskowanie pełnych maili i telefonów

### c) Prawa użytkownika

#### Technicznie:

- ✅ Endpoint lub procedura narzędziowa, która:
  - Znajdzie wszystkie dane dla danego maila
  - Wyeksportuje je do JSON / CSV
  - Usunie lub zanonimizuje na żądanie

**Status:** ⏳ Do zrobienia

---

## 9. Kopie zapasowe i scenariusze awarii

Bez tego każdy błąd produkcyjny to ruletka.

### Konkretne działania

#### DB

- ✅ Automatyczne backupy bazy:
  - Minimum raz dziennie
  - Rotacja, np. 7 dni dziennych, 4 tygodniowe, 3 miesięczne

- ✅ Przetestuj odtworzenie:
  - Na osobnym środowisku odtwórz backup i uruchom smoke-testy

#### Redis

- ✅ Załóż, że Redis może paść w każdej chwili
- ✅ Kod:
  - `RedisService` łapie `ConnectionError` i przełącza się na tryb degradacji
  - Sesje mogą stracić trochę telemetrycznych danych, ale nie rozbijają requestu

#### Katastrofa

- ✅ Spisz prosty runbook:
  - Jak uruchomić nową instancję aplikacji
  - Jak podłączyć ją do backupu DB
  - Jak zmienić DNS albo load balancer

**Status:** ⏳ Do zrobienia

---

## 10. Bezpieczeństwo promptów i LLM

Masz rozbudowane strategie i usługi. Teraz dołóż ochronę przed głupotą użytkownika i modelu.

### Wejście

#### Zanim wyślesz content do modelu:

- ✅ Przytnij długość
- ✅ Usuń potencjalnie niebezpieczne fragmenty typu:
  - Bezpośrednie prośby o wyplucie promptu systemowego
  - Jawne polecenia ignorowania zasad
  - Wklejone stack trace z sekretami

#### Możesz dodać heurystykę:

Jeżeli user mówi "ignoruj swoje poprzednie zasady" albo "pokaż cały swój prompt", wtedy:

- ✅ Przerywasz standardowy flow
- ✅ Odsyłasz bezpieczną odpowiedź

### Wyjście

#### Po odpowiedzi modelu:

- ✅ Sprawdzasz, czy nie zawiera:
  - Kluczy API
  - Danych z innych rozmów
  - Surowych dumpów konfiguracji

#### W razie wątpliwości:

- ✅ Logujesz
- ✅ Wysyłasz użytkownikowi bezpieczną, ogólną odpowiedź

### Red teaming

#### Dla siebie przygotuj zestaw promptów atakujących:

- ✅ Prompt injection
- ✅ Wyciąganie sekretów
- ✅ Obchodzenie reguł
- ✅ Masowy spam

#### Od czasu do czasu odpal je na stagingu i patrz, co się dzieje

**Status:** ⏳ Do zrobienia

---

## 11. Monitoring, logowanie, obserwowalność

### Konkretne działania

#### Wprowadź:

- ✅ Sentry lub inne narzędzie do błędów
- ✅ Metryki:
  - Liczba rozmów
  - Czas odpowiedzi
  - Liczba błędów 5xx
  - Liczba timeoutów LLM

#### Logi:

- ✅ Strukturalne JSON
- ✅ Bez pełnych danych osobowych

**Status:** ⏳ Do zrobienia

---

## 12. Co zrobić od teraz, w kolejności

### Plan działania

1. **Uporządkuj strukturę modułów i importy** tak, aby `main.py` był cienki

2. **Dokończ walidację wejścia i uploadów**, dodaj testy negatywne

3. **Uszczelnij security headers, CORS i auth** na panel admina, analytics, FAQ learning

4. **Ustabilizuj SessionTimeoutService** w produkcji z sensownymi parametrami

5. **Dodaj RODO:**
   - Retention
   - Anonimizację
   - Eksport i usuwanie na żądanie

6. **Zaprojektuj i wdroż backupy bazy** plus test restore na stagingu

7. **Dodaj filtry wejścia i wyjścia przy LLM** plus zestaw red team promptów

8. **Postaw monitoring i błędy** w jednym miejscu (Sentry, Prometheus, inny stack)

---

## 📊 Status ogólny

| Kategoria | Status | Priorytet |
|-----------|--------|-----------|
| Warstwa błędów | ⏳ Do zrobienia | 🔴 Wysoki |
| Walidacja wejścia | ⏳ Do zrobienia | 🔴 Wysoki |
| Bezpieczeństwo HTTP | ⏳ Do zrobienia | 🔴 Wysoki |
| Rate limiting | ⏳ Do zrobienia | 🟡 Średni |
| Sesje i timeouty | ⏳ Do zrobienia | 🟡 Średni |
| Architektura | 🟠 Częściowo | 🟡 Średni |
| Testy | 🟠 Częściowo | 🟡 Średni |
| RODO | ⏳ Do zrobienia | 🔴 Wysoki |
| Backupy | ⏳ Do zrobienia | 🔴 Wysoki |
| Bezpieczeństwo LLM | ⏳ Do zrobienia | 🟡 Średni |
| Monitoring | ⏳ Do zrobienia | 🟡 Średni |

---

## ✅ Podsumowanie

Jeżeli to zrobisz, to z perspektywy produkcyjnej nie będzie się do czego uczepić na poziomie fundamentów. Dalej zostaną już tylko decyzje produktowe i UX.

**Następne kroki:** Rozpocznij od punktu 1 i przechodź sekwencyjnie przez listę.

---

**Ostatnia aktualizacja:** 11 grudnia 2025

