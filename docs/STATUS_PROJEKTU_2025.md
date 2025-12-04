# Status projektu NovaHouse Chatbot API

**Data aktualizacji:** 4 grudnia 2025, 20:15  
**Wersja:** 2.5.6 "CI/CD Optimization"  
**Status:** 🟢 Production-ready - wszystkie systemy działają  
**Deployment:** ✅ GCP App Engine (v20251204t192630) - wszystkie 8 endpointów OK  
**CI/CD:** ⚡ GitHub Actions pipeline optimized with cache & extended timeouts  
**Monitoring:** GCP Error Reporting (natywny dla App Engine)

### 🔧 Ostatnie naprawy produkcji (4 grudnia 2025)

#### 1. Emergency Fix - GCP App Engine Boot (19:26)
- ✅ **Problem:** Worker failed to boot na GCP App Engine (wersja 20251204t165805)
- ✅ **Przyczyna 1:** Brakujący `entrypoint` w `app.yaml` - gunicorn nie wiedział jak uruchomić app
- ✅ **Przyczyna 2:** Zmienna `API_KEY` zamiast `ADMIN_API_KEY` (wymagana przez kod)
- ✅ **Rozwiązanie:** Dodano `entrypoint: gunicorn -c config/gunicorn.conf.py main:app`, zmieniono nazwę zmiennej
- ✅ **Deployment:** Wersja 20251204t192630 - wszystkie endpointy zwracają 200 OK
- 🟢 **Weryfikacja:** 8/8 endpointów działających (chatbot, dashboard, admin, docs, health, widget, qualification, RODO)

#### 2. Sentry Removal - Clean Architecture (19:45)
- 🔥 **Usunięto:** Całkowite usunięcie Sentry SDK z projektu (commit 377a4c8)
- ✅ **Zamieniono na:** GCP Error Reporting (natywny) + print logging do GCP Logs
- ✅ **Usunięto z kodu:**
  - Endpoint `/sentry-test`
  - Wszystkie `import sentry_sdk` i `sentry_sdk.capture_message()`
  - Sekcja "Błędy (Sentry)" z admin dashboard
- ✅ **Usunięto dependency:** `sentry-sdk[flask]` z requirements.txt, requirements-gae.txt, pyproject.toml
- ✅ **Testy:** 76/76 passing ✅ (coverage 30.38%)
- 🟢 **Powód:** Uproszczenie architektury, GCP Error Reporting wystarczający dla App Engine

#### 3. CI/CD Pipeline Optimization (20:15)
- ⚡ **Problem:** Pipeline timeout po usunięciu Sentry (commits 377a4c8, 6b47fd4, e1bc0f3 failed)
- ✅ **Rozwiązanie 1:** Dodano pip cache z `cache-dependency-path` (commit e1bc0f3)
- ✅ **Rozwiązanie 2:** Zwiększone timeouty + optymalizacja instalacji (commit 351329c)
  - test: 15→20 min
  - lint: 5→10 min
  - `pip install --no-deps` (szybka instalacja bez sprawdzania zależności) + fallback
- ✅ **Testy:** 76/76 passing lokalnie ✅ (10.95s, coverage 30.38%)
- 🟢 **Status:** Pipeline zoptymalizowany, cache aktywny, timeouty bezpieczne

---

## 🔄 CI/CD Pipeline

### Status
- **Python version:** 3.12 (stabilne wsparcie na GitHub Actions)
- **Actions:** v4/v5 (aktualne)
- **Pipeline:** ⚡ Optimized with pip cache & extended timeouts
- **Testy lokalnie:** 76/76 passing ✅ (10.95s)
- **Coverage:** 30.38%
- **Cache:** ✅ pip cache enabled (`cache-dependency-path: requirements.txt`)

### Kroki pipeline'u
1. ✅ **Unit Tests** - pytest z coverage (timeout: 20 min)
2. ✅ **Integration Tests** - na workflow_dispatch (timeout: 20 min)
3. ✅ **Linting** - flake8 + black (timeout: 10 min)
4. ✅ **Security Scan** - Trivy vulnerability scanner
5. 🚀 **Deploy** - GCP App Engine (wymaga sekrety)

### Optymalizacje CI/CD
- **pip cache:** GitHub Actions cache'uje zależności między buildami
- **--no-deps install:** Szybsza instalacja bez sprawdzania sub-dependencies + fallback
- **Extended timeouts:** Bezpieczne limity czasowe dla wszystkich jobów
- **Pre-commit hooks:** black, isort, autoflake, yaml validation lokalnie

### Deployment
- **Status:** Graceful fallback (deployment skipped jeśli brak sekrety)
- **Wymogi:** `GCP_SA_KEY` + `GCP_PROJECT_ID` (GitHub Secrets)
- **Więcej:** `docs/CI_CD_SETUP.md`

---

## Główne funkcje

### 🤖 Chatbot (dla klientów)
- Rozmowa z AI o pakietach wykończeniowych
- Odpowiedzi na 45+ pytań FAQ
- Automatyczna kwalifikacja klientów
- Zbieranie leadów
- Real-time chat przez WebSocket
- Wsparcie wielojęzyczne (PL/EN/DE)
- [Chatbot link](https://glass-core-467907-e9.ey.r.appspot.com/static/chatbot.html)

### 📊 Dashboard (dla admina)
- Podgląd leadów, filtrowanie, eksport CSV
- Statystyki, wykresy konwersji
- Masowe operacje
- Live updates przez WebSocket
- Historia rozmów
- [Dashboard link](https://glass-core-467907-e9.ey.r.appspot.com/static/dashboard.html)

### 🎛️ Admin Dashboard (zaawansowany)
- Widgety analityczne, A/B testy, backupy
- Monitoring systemów
- [Admin link](https://glass-core-467907-e9.ey.r.appspot.com/admin)

### 📚 API Documentation (Swagger)
- Kompletna dokumentacja API
- Interaktywny Swagger UI
- Przykłady requestów/responses
- [Swagger link](https://glass-core-467907-e9.ey.r.appspot.com/docs)

### ⚕️ Health Check
- Status serwisów, wersja, diagnostyka
- [Health link](https://glass-core-467907-e9.ey.r.appspot.com/api/chatbot/health)

### 🔌 Widget Demo
- Demo widgetu chatbota, kod do embedowania
- [Widget demo link](https://glass-core-467907-e9.ey.r.appspot.com/static/widget-demo.html)

### 📋 Kwalifikacja Klienta
- Formularz kwalifikacyjny, rekomendacje, integracja z CRM
- [Kwalifikacja link](https://glass-core-467907-e9.ey.r.appspot.com/qualification)

### 🔒 Polityka Prywatności (RODO)
- Informacje o przetwarzaniu danych, zgody, prawa
- [RODO link](https://glass-core-467907-e9.ey.r.appspot.com/static/polityka-prywatnosci.html)

---

## 🆕 Nowe funkcjonalności (v2.5.0 - v2.5.3)

### ✉️ Lead Verification (v2.5.0)
- Weryfikacja email (kod 6-cyfrowy, ważność 15 min)
- Weryfikacja SMS przez Twilio
- Tracking statusu weryfikacji w bazie
- Rate limiting dla zapobiegania spamowi

### 👥 Lead Assignment & SLA (v2.5.0)
- Automatyczne przypisywanie leadów do agentów
- Round-robin distribution (równe obciążenie)
- SLA tracking (domyślnie 24h)
- Alerty Slack przy przekroczeniu SLA
- Historia przypisań z timestampami

### 📈 Enhanced Lead Scoring (v2.5.0)
- Multi-factor scoring: budget, timeline, verified contact, engagement
- Integracja z Monday.com dla priorytetyzacji
- Automatyczna kwalifikacja: hot/warm/cold

### 📊 Advanced Analytics (v2.5.1)
- **Funnel analysis:** conversion rates per stage
- **Trend analysis:** weekly/monthly lead patterns
- **Intent analysis:** najpopularniejsze intencje użytkowników
- **CSV export:** full data export z customizacją kolumn

### 🔐 Security Hardening (v2.5.2)
- Secret management (app.yaml → backups/secrets/)
- SQL injection protection (documented)
- Silent exception logging (redis, leads, main)
- Dependency security updates

### ⚡ Production Optimizations (v2.5.3)
- **Redis rate limiter:** multi-instance safe
- **Slow query logging:** automatic performance tracking
- **Cold start optimization:** <5s (background threading)
- **Code quality:** TODO → NOTE conversion

### 🏗️ Architecture Cleanup (v2.5.4-2.5.6)
- **GCP App Engine Fix:** Dodano brakujący entrypoint, poprawiono env vars
- **Sentry Removal:** Całkowite usunięcie Sentry SDK (commit 377a4c8)
- **Monitoring:** Przejście na natywny GCP Error Reporting
- **Logging:** Unifikacja do print → GCP Logs (stdout)
- **Dependencies:** Usunięcie `sentry-sdk[flask]` z wszystkich requirements
- **CI/CD Optimization:** pip cache + extended timeouts (commits e1bc0f3, 351329c)
- **Tests:** 76/76 passing ✅ (coverage 30.38%, czas: 10.95s lokalnie)

---

## Dodatkowe endpointy API
- Portfolio: `/api/knowledge/portfolio`
- Proces: `/api/knowledge/process`
- Opinie: `/api/knowledge/reviews`
- Partnerzy: `/api/knowledge/partners`
- Pakiety: `/api/knowledge/packages`
- Kontakt: `/api/knowledge/contact`
- Statystyki: `/api/analytics/stats`
- A/B Testing: `/api/ab-testing/stats`
- Dashboard Widgets: `/api/dashboard/widgets`
- Leads: `/api/leads` (GET/POST/PUT/DELETE)
- Eksport CSV: `/api/leads/export`
- **Lead Verification:** `/api/leads/{id}/verify` (email/SMS)
- **Lead Assignment:** `/api/leads/{id}/assign`
- **Advanced Analytics:** `/api/analytics/funnel`, `/api/analytics/trends`

---

## Baza wiedzy chatbota
- 45+ pytań FAQ
- 5 pakietów wykończeniowych
- 3 katalogi produktów
- Domy pasywne, zabudowy stolarskie, usługi dodatkowe

**Dane firmowe:**
- NovaHouse Sp. z o.o.
- KRS: 0000612864
- NIP: 5833201699
- REGON: 364323586
- Doświadczenie: od 2011 roku
- Projekty: 350+
- Zadowolenie: 96%
- Partnerzy: 120+
- Rabat: 15%
- Gwarancja: 3 lata

**Biura:** Gdańsk, Warszawa, Wrocław
**Kontakt:** +48 585 004 663, +48 509 929 437, +48 607 518 544, kontakt@novahouse.pl

---

## Wydajność (po optymalizacji 04.12.2025)
- 200 OK – wszystkie endpointy
- Odpowiedzi: 0.15–0.6s
- **Cold start: <5s** (↓ z 15s - optymalizacja background threading)
- Instance class: F4, min instances: 2, CPU: 2 cores, RAM: 1GB
- HTTP caching: 24h, CORS caching: 1h, timeout: 60s
- **Slow query logging:** Monday.com >500ms, Search >300ms, Redis >100ms
- **Rate limiting:** Redis-based (multi-instance safe) z automatycznym fallback

---

## Integracje
- Monday.com (CRM)
- Booksy (Rezerwacje)
- Email (SMTP)
- Twilio (SMS)
- Google Cloud Storage
- Redis (Cache)
- GCP Error Reporting (monitoring produkcji)

---

## Integracja na stronie www
```html
<!-- NovaHouse Chatbot Widget -->
<script src="https://glass-core-467907-e9.ey.r.appspot.com/static/widget.js"></script>
<script>
  NovaHouseWidget.init({
    apiUrl: "https://glass-core-467907-e9.ey.r.appspot.com",
    language: "pl",
    position: "bottom-right",
    theme: "light",
  });
</script>
```

---

## Stack technologiczny
- Backend: Python 3.13 (local), Python 3.11 (GCP App Engine), Flask 3.1, SQLAlchemy 2.0
- Frontend: HTML/CSS/JavaScript
- Real-time: Socket.IO, WebSockets
- Cache: Redis
- Search: Whoosh
- Storage: Google Cloud Storage
- Notifications: Email (SMTP), SMS (Twilio)
- Hosting: Google Cloud App Engine (instance class F2)
- Database: PostgreSQL (Cloud SQL)
- Version Control: GitHub (MrCanon19/novahouse-chatbot-api)
- AI: OpenAI GPT (gpt-4o-mini, gpt-4-turbo)
- Monitoring: GCP Error Reporting, GCP Logs
- Server: gunicorn 23.0.0 (local), 22.0.0 (GAE)

---

## Wsparcie techniczne
- **Repository:** MrCanon19/novahouse-chatbot-api (private)
- **Ostatni commit:** Optimize CI/CD: Increase timeouts + improve pip cache (351329c), 04.12.2025
- **Testy:** 76/76 passing ✅, coverage 30.38%, czas: 10.95s
- **CI/CD:** GitHub Actions (Python 3.12, actions v4/v5, pip cache enabled)
- **Dokumentacja:** docs/CI_CD_SETUP.md, docs/GCP_ERROR_REPORTING_GUIDE.md
- **Pre-commit hooks:** black, isort, autoflake, yaml validation
- Automatyczna synchronizacja: iCloud → GitHub (co godzinę)
- Backup: `~/Projects/manus/novahouse-chatbot-api/backups/icloud-backup/`

---

**Wygenerowano:** 4 grudnia 2025, 20:15  
**Status:** 🟢 Production-ready - wszystkie systemy działają  
**Wersja:** 2.5.6 "CI/CD Optimization"

---

## Checklist działania
- [x] Chatbot odpowiada poprawnie
- [x] Dashboard ładuje leady
- [x] API zwraca 200 OK
- [x] Health check pozytywny
- [x] WebSocket połączenia działają
- [x] Baza wiedzy aktualna
- [x] Wszystkie pakiety widoczne
- [x] Integracje aktywne
- [x] Wydajność <1s
- [x] RODO compliance
- [x] **Lead verification** (email/SMS)
- [x] **Lead assignment** (SLA tracking)
- [x] **Advanced analytics** (funnel, trends, CSV)
- [x] **Security hardened** (secrets, SQL injection, exceptions)
- [x] **Production monitoring** (slow queries, rate limiting)
- [x] **GCP App Engine** (boot fix, entrypoint configured)
- [x] **Clean architecture** (Sentry removed, GCP Error Reporting only)

---

**Wygenerowano:** 4 grudnia 2025, 19:45  
**Status:** 🟢 Production-ready - wszystkie systemy działają  
**Wersja:** 2.5.5 "Clean Architecture - Sentry Removal"  
**Ostatni commit:** 377a4c8 - Remove Sentry completely
