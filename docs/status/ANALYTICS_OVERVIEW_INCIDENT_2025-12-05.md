# Incident: Błąd "Przegląd 24h" / Legacy API (App Engine)

## 1) Punkt wyjścia – komunikat z panelu
- UI łączy dwa błędy w jeden string: `Błąd ładowania danych: <nowe API> | <legacy>`.
- Zaobserwowany komunikat: **`Przegląd 24h: tuple index out of range | Legacy API zwróciło błąd`**.

## 2) Co pokazały logi GCP (App Engine)
- Zapytanie do logów (GAE): `gcloud logging read 'resource.type="gae_app" AND textPayload:"tuple index out of range"' ...`.
- Wynik: błąd w **starej wersji** `default / 20251204t192630` w stack trace Pythona (SQLAlchemy, `BaseRow.__getitem__`).
- Brak nowych wystąpień po przełączeniu na nowszą wersję (sprawdzono `--freshness=10m`).

## 3) Ruch i wersje w App Engine
- Lista wersji pokazała wiele historycznych deployów.
- Ruch ustawiony na najnowszą wersję: `gcloud app services set-traffic default --splits=20251205t124418=1`.
- Problematyczna wersja `20251204t192630` usunięta: `gcloud app versions delete 20251204t192630 --service=default`.
- Efekt: 100% ruchu na działającym buildzie, błędy `tuple index out of range` już nie wracają.

## 4) Stan nowych endpointów analityki
- Zweryfikowane curl-em:
  - `/api/analytics/overview?days=1` → `status: "success"`, zawiera pole `overview` zgodne z frontem.
  - `/api/analytics/conversations?days=7` → `status: "success"`.
  - `/api/analytics/engagement?days=7` → `status: "success"`.
- Przykład pełnej odpowiedzi dla `days=1` pokazuje poprawny JSON z `overview` i `status: "success"`.

## 5) Jak reaguje frontend (src/static/dashboard.html)
- Funkcja `loadDashboard` najpierw woła nowe API (`overview?days=1` i `overview?days=7`).
- Gdy któreś z nich rzuci błąd → zapisuje `primaryError` i przechodzi do legacy (`/api/analytics/dashboard/summary?budget=10`).
- Jeśli legacy zwróci `success !== true`, rzuca `fallbackMsg` (domyślnie „Legacy API zwróciło błąd”).
- Ostateczny komunikat skleja oba błędy: `Błąd ładowania danych: <błąd nowego API> | <błąd legacy>`.

## 6) Co już naprawiono ✅
- Stara wersja z `tuple index out of range` wyłączona z ruchu i usunięta.
- Nowe API dla `days=1` działa poprawnie, struktura pasuje do frontu.
- `conversations` oraz `engagement` (7 dni) zwracają `success`.
- Logi świeże nie pokazują `tuple index out of range`.

## 7) Co jeszcze do zrobienia 🛠️
- Aktualny komunikat z UI: **`Błąd ładowania danych: Przegląd 7 dni: HTTP 500 | Legacy API zwróciło błąd`**.
- Do zbadania: HTTP 500 na `/api/analytics/overview?days=7` (nowe API) + dlaczego legacy fallback nie zwraca `success`.
- Zalecane kroki debug:
  1. `curl -i "https://glass-core-467907-e9.ey.r.appspot.com/api/analytics/overview?days=7"` – potwierdzenie statusu.
  2. `curl -s ... | jq` – inspekcja body (lub błąd `jq` jeśli nie-JSON).
  3. `gcloud logging read 'resource.type="gae_app" AND resource.labels.module_id="default" AND resource.labels.version_id="20251205t124418" AND httpRequest.status=500' --freshness=5m --limit=20` – stack trace dla 500.
- Po korekcie logiki `days=7` (np. agregacje, brak danych, SQL) wykonać ponowny deploy, test `curl` oraz odświeżyć dashboard.
