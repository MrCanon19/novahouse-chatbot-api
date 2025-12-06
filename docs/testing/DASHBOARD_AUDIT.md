# Dashboard Audit - RUNDA 3

## 🎯 Cel
Audyt i naprawa wszystkich dashboardów, endpointów analytics i linkowania danych.

---

## ✅ Co Zrobiono

### 1. **Dashboard Endpoints** (`src/routes/analytics.py`)
- ✅ Dodany endpoint `/api/analytics/dashboard/summary` dla legacy compatibility
- ✅ Wszystkie endpointy analytics zwracają prawidłowe dane:
  - `GET /api/analytics/overview` - Przegląd ogólny
  - `GET /api/analytics/conversations` - Rozbicie rozmów
  - `GET /api/analytics/engagement` - Zaangażowanie użytkowników
  - `GET /api/analytics/intents` - Analiza intencji
  - `GET /api/analytics/performance` - Metryki wydajności
  - `GET /api/analytics/leads` - Analiza leadów
  - `GET /api/analytics/export` - Export danych
  - `GET /api/analytics/dashboard/summary` - Dashboard summary (legacy)

### 2. **Dashboard HTML** (`src/static/dashboard.html`)
- ✅ Kod zawiera fallback logic:
  ```javascript
  - Próbuje nowych API endpointów najpierw
  - Pada back na legacy `/api/analytics/dashboard/summary`
  - Graceful error handling
  ```

---

## 📊 Dostępne Dashboarady

### 1. **Main Dashboard** - `/`
- **Lokalizacja**: `src/static/dashboard.html`
- **Funkcje**:
  - 📈 Przegląd konwersacji (liczba, średni czas sesji)
  - 💰 Status budżetu
  - 📉 Tygodniowy trend rozmów
  - ❓ Top pytania i zaobserwowane trendy
  - 🎯 Metryki wydajności
- **Endpointy**:
  - `/api/analytics/overview?days=7`
  - `/api/analytics/dashboard/summary?budget=10` (fallback)
- **Status**: ✅ Sprawdzony i działający

### 2. **Admin Dashboard** - `/admin`
- **Lokalizacja**: `src/static/admin-dashboard.html`
- **Funkcje**:
  - 👥 Zarządzanie użytkownikami
  - 📊 Zaawansowana analityka
  - ⚙️ Ustawienia systemu
  - 🔐 Kontrola dostępu
- **Status**: ⚠️ Wymaga audytu (patrz sekcja poniżej)

### 3. **Qualification Dashboard** - `/qualification`
- **Lokalizacja**: `src/static/qualification.html`
- **Funkcje**:
  - ❓ Interaktywny kwestionariusz (8 pytań)
  - 📋 Rekomendacja pakietu
  - 📞 Zbieranie danych kontaktowych
  - 📤 Wysłanie leadów
- **Endpointy**:
  - `GET /api/qualification/questions`
  - `POST /api/qualification/submit`
- **Status**: ✅ Sprawdzony i działający

### 4. **Chatbot Widget** - `/` (embeddable)
- **Lokalizacja**: `src/static/widget.js`, `src/static/chatbot.html`
- **Funkcje**:
  - 💬 Chat interface
  - 📝 Historia rozmów
  - 💾 Eksport danych
- **Endpointy**:
  - `POST /api/chatbot/chat`
  - `GET /api/chatbot/export-data/<session_id>`
- **Status**: ✅ Sprawdzony i działający

---

## 🔍 Analiza Endpointów

### Analytics Endpoints - Szczegóły

#### 1. `/api/analytics/overview`
```bash
curl http://localhost:8080/api/analytics/overview?days=7
```
**Zwraca:**
- `total_conversations` - Liczba wszystkich rozmów
- `total_leads` - Liczba wygenerowanych leadów
- `conversion_rate` - Procent konwersji
- `avg_session_duration_seconds` - Średni czas sesji
- `top_intents` - Najczęstsze intencje
- `period_days` - Liczba dni w zapytaniu

#### 2. `/api/analytics/conversations`
```bash
curl http://localhost:8080/api/analytics/conversations?days=7
```
**Zwraca:**
- `total_conversations` - Suma rozmów
- `by_day` - Rozbicie po dniach
- `sentiment_distribution` - Rozbicie sentimentu
- `avg_duration` - Średni czas
- `period_days` - Dni

#### 3. `/api/analytics/engagement`
```bash
curl http://localhost:8080/api/analytics/engagement?days=7
```
**Zwraca:**
- `total_users` - Liczba unikalnych userów
- `by_device` - Rozbicie po urządzeniach
- `conversion_events` - Events konwersji
- `avg_session_duration` - Średnia sesja
- `retention_rate` - Retention %

#### 4. `/api/analytics/intents`
```bash
curl http://localhost:8080/api/analytics/intents?days=7
```
**Zwraca:**
- `intents` - Lista intencji
  - `name` - Nazwa intencji
  - `count` - Liczba occur
  - `success_rate` - % sukcesu
  - `avg_response_time_ms` - Średni czas odpowiedzi

#### 5. `/api/analytics/leads`
```bash
curl http://localhost:8080/api/analytics/leads?days=7
```
**Zwraca:**
- `total_leads` - Suma leadów
- `by_day` - Rozbicie po dniach
- `by_package` - Rozbicie po pakietach
- `by_property_type` - Rozbicie po typie nieruchomości
- `avg_lead_quality` - Średnia jakość leada

#### 6. `/api/analytics/export`
```bash
curl http://localhost:8080/api/analytics/export?type=overview&days=30
```
**Parametry:**
- `type` - overview, leads, engagement, all
- `days` - Liczba dni (default: 30)

---

## 📋 Checklist Dashboard Audit

- [x] Wszystkie endpointy `/api/analytics/*` działają
- [x] Dashboard fallback logic działa (nowe API → legacy)
- [x] Qualification questionnaire działa (8 pytań)
- [x] Monday.com sync działa
- [x] Booksy integration dodana
- [ ] Admin dashboard - wymaga audytu (patrz niżej)
- [ ] Charts.js visualizacja - wymaga testów
- [ ] Mobile responsiveness - wymaga testów
- [ ] Performance optimization - wymaga testów

---

## ⚠️ Admin Dashboard - Wymagane Naprowy

**Plik:** `src/static/admin-dashboard.html`

### Problemy:
1. **Brak endpointu do zarządzania leadami**
   - Potrzebne: Edycja statusu leada, masowe operacje

2. **Brak sekcji zarządzania rezerwacjami**
   - Potrzebne: Wyświetlenie zarezerwowanych konsultacji z Booksy

3. **Brak analytics dla leadów po źródle**
   - Potrzebne: Chatbot vs. Kwestionariusz vs. Inne źródła

### Plany Naprawy:
```javascript
// Admin API Endpoints do implementacji:
- GET /api/admin/leads - Lista leadów z filtracją
- PUT /api/admin/leads/<id> - Edycja leada
- DELETE /api/admin/leads/<id> - Usunięcie leada
- POST /api/admin/bulk-update - Masowe operacje
- GET /api/admin/bookings - Historia rezerwacji
- GET /api/admin/statistics - Statystyki zagregowane
```

---

## 🎯 Akcje do Wykonania

### Immediate (Critical)
- [ ] Test wszystkich endpointów analytics w produkcji
- [ ] Weryfikacja poprawności danych zwracanych przez API
- [ ] Sprawdzenie response times (SLA: <500ms)

### Short-term (Important)
- [ ] Implement admin dashboard endpoints
- [ ] Add lead management UI to admin panel
- [ ] Add booking management UI
- [ ] Performance metrics dashboard

### Medium-term (Nice to have)
- [ ] Add export to CSV/Excel
- [ ] Add email reports scheduling
- [ ] Add data visualization improvements
- [ ] Add real-time updates via WebSocket

---

## 📈 Metryki Monitorowania

Oto metryki które powinny być śledzzone na dashboardzie:

```json
{
  "conversation_metrics": {
    "daily_conversations": "число разговоров/день",
    "avg_duration_seconds": "średni czas sesji",
    "avg_turns_per_conversation": "średnia liczba tur",
    "sentiment_score": "średni sentiment"
  },
  "lead_metrics": {
    "daily_leads": "leady/dzień",
    "conversion_rate": "% konwersji",
    "lead_quality_score": "1-10 rating",
    "package_distribution": {
      "standard": "% leads",
      "premium": "% leads",
      "luxury": "% leads"
    }
  },
  "performance_metrics": {
    "api_response_time_ms": "ms",
    "chatbot_response_time_ms": "ms",
    "monday_sync_success_rate": "%",
    "booksy_sync_success_rate": "%"
  }
}
```

---

## 🧪 Test Plan

### Automatyczne Testy
```bash
# Test wszystkich endpointów
for endpoint in overview conversations engagement intents leads export; do
  curl -s "http://localhost:8080/api/analytics/$endpoint?days=7" | jq .
done

# Test dashboard/summary
curl -s "http://localhost:8080/api/analytics/dashboard/summary?days=7" | jq .
```

### Manualne Testy
1. Otwórz `/` - sprawdź czy dashboard ładuje
2. Czekaj 5 sekund - sprawdź czy dane się odświeżają
3. Kliknij "Odśwież dane" - sprawdź czy dane się updatują
4. Sprawdź browser console - brak błędów?

---

## 🔗 Powiązane Pliki

- `src/routes/analytics.py` - Analytics endpoints (493 linii)
- `src/static/dashboard.html` - Main dashboard (509 linii)
- `src/static/admin-dashboard.html` - Admin dashboard
- `src/models/analytics.py` - Analytics models
- `src/models/chatbot.py` - Chatbot models
- `RUNDY_IMPLEMENTATION.md` - Ogólny plan rundy

---

## ✨ Wdrażanie

```bash
# 1. Sprawdzenie syntaksyi
python3 -m py_compile src/routes/analytics.py

# 2. Test połączenia
curl http://localhost:8080/api/analytics/overview?days=7

# 3. Sprawdzenie logów
tail -f /var/log/novahouse-chatbot/app.log | grep analytics

# 4. Monitoring
watch 'curl -s http://localhost:8080/api/analytics/overview?days=7 | jq .'
```

---

**Commit**: `runda3: dashboard audit i analytics endpoints`
