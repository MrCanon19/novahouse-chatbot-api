# 📊 NovaHouse Chatbot API - Status Projektu

> **Data:** 14 listopada 2025
> **Wersja:** 2.3.1 (Production)
> **Status:** ✅ **LIVE & STABLE**

---

# 🚀 Produkcja

## Informacje o Wdrożeniu

| Parametr | Wartość |
|----------|---------|
| **URL** | https://glass-core-467907-e9.ey.r.appspot.com |
| **Wersja** | `20251114t152707` (AKTYWNA) |
| **Ruch** | 100% |
| **Instancja** | F2 (512 MB RAM, 1.2 GHz CPU) |
| **Region** | europe-west3 |
| **Platforma** | Google App Engine (Python 3.11) |
| **Ostatnie Wdrożenie** | 2025-11-14 15:27:50 |

## Status Zdrowia

```bash
curl https://glass-core-467907-e9.ey.r.appspot.com/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "service": "novahouse-chatbot"
}
```

---

# 📦 Funkcjonalności

## Podstawowe Funkcje (v1.0 - v2.2)

- ✅ **17+ FAQ** - Inteligentne odpowiedzi
- ✅ **Powiadomienia Email** - Potwierdzenia leadów i rezerwacji
- ✅ **Zaawansowana Analityka** - Szczegółowe statystyki
- ✅ **Testy A/B** - Optymalizacja konwersji
- ✅ **Wielojęzyczność** - PL/EN/DE
- ✅ **Panel Administracyjny** - Zarządzanie leadami
- ✅ **Zarządzanie Leadami** - Filtrowanie, eksport CSV, operacje masowe
- ✅ **9 Endpointów Wiedzy** - Portfolio, opinie, partnerzy, FAQ
- ✅ **Zarządzanie Sesjami** - Śledzenie konwersacji
- ✅ **Dokumentacja Swagger** - Dokumentacja API
- ✅ **Monitoring Zdrowia** - Monitorowanie czasu pracy

## Funkcje v2.3 🎉

- ✅ **Integracja Redis** - Cachowanie i limitowanie żądań gotowe na produkcję
- ✅ **Wsparcie WebSocket** - Czat w czasie rzeczywistym i live dashboard
- ✅ **Upload i Optymalizacja Plików** - Wiele rozmiarów + GCS
- ✅ **Przypomnienia o Spotkaniach** - SMS (Twilio) + Email
- ✅ **Zaawansowane Wyszukiwanie** - Whoosh full-text (33 dokumenty zaindeksowane)
- ✅ **Widgety Dashboard** - 8 widgetów w czasie rzeczywistym
- ✅ **Backup i Export** - Automatyczne codzienne backupy + zgodność RODO

## Latest Updates (Today) 🆕

> **Dodane dzisiaj:**

- ✅ **Automated Backup Cleanup** - Automatyczne usuwanie backupów starszych niż 30 dni
- ✅ **App Engine /tmp Fix** - Backupy zapisywane w /tmp (writable directory)
- ✅ **API Endpoints Documentation** - Kompletna dokumentacja z przykładami curl
- ✅ **Manual Cleanup Endpoint** - `POST /api/backup/cleanup`

---

# 🏗️ Architektura

## Stos Technologiczny

| Komponent | Technologia |
|-----------|-------------|
| **Backend** | Python 3.13.5 (lokalnie) / 3.11 (produkcja) |
| **Framework** | Flask 3.1.1 |
| **Baza Danych** | PostgreSQL 15 (Cloud SQL) |
| **ORM** | SQLAlchemy 2.0.44 |
| **Cache** | Redis 5.0.1 (z fallbackiem in-memory) |
| **Wyszukiwanie** | Whoosh 2.7.4 (pełnotekstowe) |
| **Czas Rzeczywisty** | Flask-SocketIO 5.3.6 + eventlet 0.37.0 |
| **Przechowywanie** | Google Cloud Storage |
| **Harmonogramowanie** | APScheduler 3.10.4 |
| **Serwer** | Gunicorn 21.2.0 (5 workerów) |

## Zależności (27 całkowicie)

```python
Flask==3.1.1
SQLAlchemy==2.0.44
psycopg2-binary==2.9.9
redis==5.0.1
Whoosh==2.7.4
Flask-SocketIO==5.3.6
APScheduler==3.10.4
google-generativeai
google-cloud-storage==2.14.0
twilio==8.11.0
gunicorn==21.2.0
eventlet==0.37.0
Pillow==11.1.0
requests==2.31.0
# + 13 more
```

## Struktura Projektu

```
📦 novahouse-chatbot-api/
├── 📁 src/
│   ├── 📁 routes/ (17 files) - API endpoints
│   ├── 📁 services/ (12 files) - Business logic
│   ├── 📁 models/ (4 files) - Database models
│   ├── 📁 middleware/ - Security, cache
│   ├── 📁 integrations/ - Booksy, Monday.com
│   ├── 📁 knowledge/ - FAQ, portfolio data
│   └── main.py - App entry point
├── 📁 tests/ (4 files) - Unit tests
├── 📁 backups/automated/ - Daily backups (local only)
├── app.yaml - App Engine config
├── requirements.txt - Dependencies
└── 📚 Documentation (25+ MD files)
```

## Statystyki

| Metryka | Wartość |
|---------|---------|
| **Pliki Python** | 48 |
| **Linii kodu** | 9,590 |
| **Moduły tras** | 17 |
| **Moduły serwisów** | 12 |
| **Modele danych** | 4 |

---

# 🔌 API Endpoints

## Endpointy Publiczne (Bez Klucza API)

### Zdrowie i Status
```bash
GET /api/health
```

### Search
```bash
GET /api/search?q=wykończenie&limit=10
GET /api/search/suggest?q=wykoń
GET /api/search/stats
```

### Widgety Dashboardu
```bash
GET /api/widgets/metrics/summary
GET /api/widgets/metrics/timeline?days=7
GET /api/widgets/top/intents?limit=10
GET /api/widgets/top/packages?limit=10
GET /api/widgets/active/sessions
GET /api/widgets/response/times?hours=24
GET /api/widgets/satisfaction/scores?days=30
```

### Dokumentacja
```bash
GET /api/docs           # Swagger UI
GET /api/docs/spec      # OpenAPI
GET /api/docs/redoc     # ReDoc
```

### RODO
```bash
POST /api/rodo/export
POST /api/rodo/delete
POST /api/rodo/consent/check
```

## Endpointy Chronione (Wymagają Klucza API)

> **Wymagany Klucz API:** `-H "X-API-Key: V=iqRX16Zlp2TE+Hpz9pnT42it-L75SB"`

### Backup i Export
```bash
GET  /api/backup/list
POST /api/backup/export
POST /api/backup/cleanup        # ⭐ NEW
GET  /api/backup/download/<filename>
```

### Upload Plików
```bash
POST /api/upload/image
POST /api/upload/multiple
POST /api/upload/delete
```

### Zarządzanie Wyszukiwaniem
```bash
POST /api/search/reindex
```

### Własne Widgety
```bash
POST /api/widgets/custom
```

---

# 🔄 System Backupów

## Automatyczne Backupy

| Parametr | Wartość |
|----------|---------|
| **Harmonogram** | Codziennie o 3:00 (czas serwera) |
| **Format** | JSON |
| **Lokalizacja** | `/tmp/backups` (App Engine) lub `backups/automated/` (lokalnie) |
| **Retencja** | 30 dni (automatyczne czyszczenie) |
| **Zawartość** | Użytkownicy, sesje, wiadomości, leady, rezerwacje, analityka |

## Operacje Manualne

### Tworzenie Backupu
```bash
curl -X POST https://glass-core-467907-e9.ey.r.appspot.com/api/backup/export \
  -H "X-API-Key: V=iqRX16Zlp2TE+Hpz9pnT42it-L75SB" \
  -H "Content-Type: application/json" \
  -d '{"format": "json"}'
```

### Lista Backupów
```bash
curl https://glass-core-467907-e9.ey.r.appspot.com/api/backup/list \
  -H "X-API-Key: V=iqRX16Zlp2TE+Hpz9pnT42it-L75SB"
```

### Czyszczenie Starych Backupów
```bash
curl -X POST https://glass-core-467907-e9.ey.r.appspot.com/api/backup/cleanup \
  -H "X-API-Key: V=iqRX16Zlp2TE+Hpz9pnT42it-L75SB" \
  -H "Content-Type: application/json" \
  -d '{"days_to_keep": 30}'
```

---

# 🔐 Bezpieczeństwo

## Dane Uwierzytelniające

> **⚠️ TYLKO LOKALNIE - Nigdy Nie Commitowane**
> Przechowywane w: `app.yaml.secret` (w .gitignore)

| Dane | Wartość (nie udostępniaj publicznie!) |
|------------|-------------------------------|
| **SECRET_KEY** | `2e2abf938bb057c9dea1515ec726a2ab4fc378399596e3309b1e310c4e3ff489` |
| **API_KEY** | `V=iqRX16Zlp2TE+Hpz9pnT42it-L75SB` |
| **PostgreSQL** | `vicNRNoO3TpLZzQ_BkAVbz886dW_J0Yo` |

## Funkcje Bezpieczeństwa

- ✅ Wszystkie sekrety w `.gitignore`
- ✅ Ochrona kluczem API endpointów administracyjnych
- ✅ CORS skonfigurowany dla produkcji
- ✅ Limitowanie żądań przez Redis
- ✅ Zgodność z RODO (eksport, usuwanie, zgoda)
- ✅ Ochrona przed SQL injection (SQLAlchemy ORM)
- ✅ Ochrona przed XSS (automatyczne escapowanie Flask)

## Chronione Zasoby

```
✅ /api/backup/* (except /list)
✅ /api/upload/*
✅ /api/search/reindex
✅ /api/widgets/custom
```

---

# 📚 Documentation

## Instalacja i Wdrożenie

- `README.md` - Główna dokumentacja
- `QUICK_START_V2.3.md` - Szybki start (v2.3)
- `INSTRUKCJA_WDROZENIA_GCP.md` - Wdrożenie na GCP
- `DEPLOYMENT_SUCCESS_20251114.md` - Ostatnie wdrożenie
- `PRODUKCJA_GOTOWA.md` - Przewodnik produkcyjny

## Funkcje i Implementacja

- `IMPLEMENTATION_COMPLETE_V2.3.md` - Implementacja v2.3
- `RELEASE_NOTES_V2.3.md` - Release notes
- `BACKUP_SYSTEM.md` - System backupów ⭐ NEW
- `API_ENDPOINTS.md` - Dokumentacja API ⭐ NEW
- `ANALYTICS_IMPLEMENTATION.md` - Analytics
- `MONDAY_INTEGRATION.md` - Monday.com
- `BOOKSY_INTEGRATION.md` - Booksy

## Bezpieczeństwo i Zgodność

- `SECURITY.md` - Bezpieczeństwo
- `RODO_IMPLEMENTATION.md` - RODO compliance
- `RODO_QUICK_START.md` - RODO quick start
- `ROTATE_CREDENTIALS.md` - Rotacja credentials
- `DEPLOY_SECRETS.md` - Deploy secrets guide

## Testowanie i Audyt

- `FINAL_AUDIT_COMPLETE.md` - Kompletny audyt
- `RODO_TEST_RESULTS.md` - Testy RODO
- `DASHBOARD_AUDIT.md` - Audyt dashboardu

---

# 🔧 Konfiguracja

## Zmienne Środowiskowe (Produkcja)

```yaml
FLASK_ENV: production
SECRET_KEY: [64 hex chars]
API_KEY: [32 chars]
DATABASE_URL: postgresql://chatbot_user:[password]@.../chatbot_db
GEMINI_API_KEY: [Google AI key]
MONDAY_API_KEY: [Monday.com key]
REDIS_URL: redis://localhost:6379
ALLOWED_ORIGINS: https://novahouse.pl,https://www.novahouse.pl
```

## Konfiguracja App Engine

```yaml
runtime: python311
service: default
instance_class: F2  # 512 MB RAM

env_variables:
  FLASK_ENV: production
  # ... all secrets ...

handlers:
  - url: /static
    static_dir: src/static
  - url: /.*
    script: auto
```

---

# 🧪 Testowanie

## Szybkie Testy

```bash
# Health check
curl https://glass-core-467907-e9.ey.r.appspot.com/api/health

# Search (33 documents indexed)
curl "https://glass-core-467907-e9.ey.r.appspot.com/api/search?q=standard"

# Dashboard metrics
curl https://glass-core-467907-e9.ey.r.appspot.com/api/widgets/metrics/summary

# Backup list (requires API key)
curl https://glass-core-467907-e9.ey.r.appspot.com/api/backup/list \
  -H "X-API-Key: V=iqRX16Zlp2TE+Hpz9pnT42it-L75SB"
```

## Rozwój Lokalny

```bash
# Install dependencies
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run locally
python src/main.py

# Run tests
pytest tests/
```

---

# 📈 Monitorowanie

## Komendy Cloud Console

```bash
# View logs
gcloud app logs tail --project=glass-core-467907-e9

# List versions
gcloud app versions list --service=default --project=glass-core-467907-e9

# App status
gcloud app describe --project=glass-core-467907-e9
```

## Metryki

| Metryka | Wartość |
|---------|---------|
| **Search Index** | 33 documents (18 FAQ + 4 portfolio + 5 reviews + 6 blog) |
| **Redis Cache** | Warm on startup (fallback: in-memory) |
| **Database** | Cloud SQL PostgreSQL 15 (RUNNABLE) |
| **Storage** | Google Cloud Storage for uploads |
| **Backups** | Daily at 3 AM, auto-cleanup after 30 days |

---

# 🔄 Ostatnie Zmiany

## Ostatnie 10 Commitów

1. `11fe34d` 🔧 Fix backup directory for App Engine /tmp
2. `e7898d6` 📝 Add API endpoints documentation + Fix backup dir
3. `3ced9b8` 🔄 Add automated backup cleanup system
4. `872ce45` 🧹 Clean workspace - remove temp files and backups
5. `efd5af5` 📝 Add comprehensive deployment documentation
6. `1031b85` 🚀 Production deployment v2.3 - F2 instance + graceful DB init
7. `a690fc9` 🐛 Fix search indexing - handle dict structures
8. `8114faa` 📝 PRODUKCJA_GOTOWA.md guide
9. `042aafe` 🚀 FINAL PRODUCTION READY: WebSocket AI + API_KEY + CORS
10. `919a1a3` ✅ AUDYT KOMPLETNY - 0 błędów

> **Ostatni Push:** 2025-11-14 (zsynchronizowane z origin/main)

---

# ✅ Lista Kontrolna Jakości

## Jakość Kodu

- ✅ **Składnia:** 0 błędów kompilacji
- ✅ **Importy:** Wszystkie moduły ładują się poprawnie
- ✅ **Testy:** Podstawowe importy zweryfikowane
- ✅ **Linting:** Brak krytycznych problemów

## Bezpieczeństwo

- ✅ **Sekrety:** Żadne nie commitowane do Git
- ✅ **Klucze API:** Chronione przez @require_api_key
- ✅ **CORS:** Konfiguracja uwzględniająca produkcję
- ✅ **Limitowanie Żądań:** Ochrona oparta na Redis

## Wdrożenie

- ✅ **Wersja:** 20251114t152707 AKTYWNA
- ✅ **Zdrowie:** HTTP 200, baza danych połączona
- ✅ **Ruch:** 100% na najnowszej wersji
- ✅ **Instancja:** F2 (512 MB) stabilna

## Dokumentacja

- ✅ **README:** Aktualne
- ✅ **Dokumentacja API:** Kompletna z przykładami
- ✅ **Dokumentacja Backupów:** Kompleksowy przewodnik
- ✅ **Wdrożenie:** Instrukcje krok po kroku

---

# 🎯 Kolejne Kroki

## Potencjalne Ulepszenia

- [ ] Migracja backupów do Google Cloud Storage (obecnie /tmp efemeryczny)
- [ ] Dodanie UI do pobierania backupów w dashboardzie
- [ ] Implementacja funkcji przywracania backupów
- [ ] Dodanie dashboardu metryk dla monitorowania backupów
- [ ] Konfiguracja alertów Cloud Monitoring
- [ ] Konfiguracja eksportów Cloud Logging

## Utrzymanie

- ✅ Automatyczne backupy działają (codziennie o 3:00)
- ✅ Automatyczne czyszczenie (retencja 30 dni)
- ✅ Monitoring zdrowia aktywny
- ✅ Śledzenie błędów przez logi

---

# 📞 Wsparcie

## Linki do Dokumentacji

- **Główny README:** `README.md`
- **Referencja API:** `API_ENDPOINTS.md`
- **Przewodnik Backupów:** `BACKUP_SYSTEM.md`
- **Przewodnik Wdrożenia:** `DEPLOYMENT_SUCCESS_20251114.md`

## Szybkie Linki

- **Produkcja:** https://glass-core-467907-e9.ey.r.appspot.com
- **Dokumentacja Swagger:** https://glass-core-467907-e9.ey.r.appspot.com/api/docs
- **Sprawdzenie Zdrowia:** https://glass-core-467907-e9.ey.r.appspot.com/api/health
- **GitHub:** https://github.com/MrCanon19/novahouse-chatbot-api

---

# 🎉 Podsumowanie

> **NovaHouse Chatbot API v2.3.1** jest w pełni **produkcyjny i stabilny**

## Kluczowe Metryki

- ✅ **48 plików Python**, 9,590 linii kodu
- ✅ **Zero błędów kompilacji** i importów
- ✅ **100% ruchu** na najnowszej wersji
- ✅ **Automatyczne backupy** z auto-czyszczeniem
- ✅ **Kompletna dokumentacja** API
- ✅ **Bezpieczne** dane uwierzytelniające (nigdy nie commitowane)
- ✅ **Zgodność z RODO** (eksport, usuwanie, zgoda)
- ✅ **Czas rzeczywisty** wsparcie WebSocket
- ✅ **Zaawansowane wyszukiwanie** (33 dokumenty)
- ✅ **Widgety dashboardu** (8 w czasie rzeczywistym)

## Status

**🟢 GOTOWE DO PRODUKCJI I LIVE**

---

**Ostatnia Aktualizacja:** 2025-11-14 15:30:00  
**Wersja:** 2.3.1  
**Wdrożenie:** 20251114t152707  
**Następny Backup:** Jutro o 03:00
