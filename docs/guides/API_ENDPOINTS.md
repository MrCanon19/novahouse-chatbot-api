# 🔌 API Endpoints - Quick Reference

**Base URL:** `https://glass-core-467907-e9.ey.r.appspot.com`  
**Version:** 20251114t152149 (Latest)

## 🏥 Health & Status

### Health Check
```bash
GET /api/health
# Sprawdza czy API działa + połączenie z bazą

curl https://glass-core-467907-e9.ey.r.appspot.com/api/health
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-11-14T15:22:49Z"
}
```

---

## 🔄 Backup & Export

### 1. Lista Backupów
```bash
GET /api/backup/list
Headers: X-API-Key: YOUR_KEY

curl https://glass-core-467907-e9.ey.r.appspot.com/api/backup/list \
  -H "X-API-Key: V=iqRX16Zlp2TE+Hpz9pnT42it-L75SB"
```

### 2. Tworzenie Backupu
```bash
POST /api/backup/export
Headers: X-API-Key: YOUR_KEY
Body: {"format": "json"}

curl -X POST https://glass-core-467907-e9.ey.r.appspot.com/api/backup/export \
  -H "X-API-Key: V=iqRX16Zlp2TE+Hpz9pnT42it-L75SB" \
  -H "Content-Type: application/json" \
  -d '{"format": "json"}'
```

### 3. Czyszczenie Starych Backupów ⭐ NOWE
```bash
POST /api/backup/cleanup
Headers: X-API-Key: YOUR_KEY
Body: {"days_to_keep": 30}

curl -X POST https://glass-core-467907-e9.ey.r.appspot.com/api/backup/cleanup \
  -H "X-API-Key: V=iqRX16Zlp2TE+Hpz9pnT42it-L75SB" \
  -H "Content-Type: application/json" \
  -d '{"days_to_keep": 30}'
```

### 4. Pobranie Backupu
```bash
GET /api/backup/download/<filename>
Headers: X-API-Key: YOUR_KEY

curl https://glass-core-467907-e9.ey.r.appspot.com/api/backup/download/backup_20251114_030000.json \
  -H "X-API-Key: V=iqRX16Zlp2TE+Hpz9pnT42it-L75SB" \
  -O
```

---

## 🔍 Search (Whoosh)

### 1. Wyszukiwanie
```bash
GET /api/search?q=wykończenie&type=all&limit=10

curl "https://glass-core-467907-e9.ey.r.appspot.com/api/search?q=wykończenie&type=all&limit=10"
```

### 2. Sugestie
```bash
GET /api/search/suggest?q=wykoń

curl "https://glass-core-467907-e9.ey.r.appspot.com/api/search/suggest?q=wykoń"
```

### 3. Statystyki
```bash
GET /api/search/stats

curl https://glass-core-467907-e9.ey.r.appspot.com/api/search/stats
```

### 4. Reindeksowanie
```bash
POST /api/search/reindex
Headers: X-API-Key: YOUR_KEY

curl -X POST https://glass-core-467907-e9.ey.r.appspot.com/api/search/reindex \
  -H "X-API-Key: V=iqRX16Zlp2TE+Hpz9pnT42it-L75SB"
```

---

## 📊 Dashboard Widgets (v2.3)

### 1. Podsumowanie Metryki
```bash
GET /api/widgets/metrics/summary

curl https://glass-core-467907-e9.ey.r.appspot.com/api/widgets/metrics/summary
```

### 2. Timeline Metryki
```bash
GET /api/widgets/metrics/timeline?days=7

curl "https://glass-core-467907-e9.ey.r.appspot.com/api/widgets/metrics/timeline?days=7"
```

### 3. Top Intencje
```bash
GET /api/widgets/top/intents?limit=10

curl "https://glass-core-467907-e9.ey.r.appspot.com/api/widgets/top/intents?limit=10"
```

### 4. Top Pakiety
```bash
GET /api/widgets/top/packages?limit=10

curl "https://glass-core-467907-e9.ey.r.appspot.com/api/widgets/top/packages?limit=10"
```

### 5. Aktywne Sesje
```bash
GET /api/widgets/active/sessions

curl https://glass-core-467907-e9.ey.r.appspot.com/api/widgets/active/sessions
```

### 6. Czasy Odpowiedzi
```bash
GET /api/widgets/response/times?hours=24

curl "https://glass-core-467907-e9.ey.r.appspot.com/api/widgets/response/times?hours=24"
```

### 7. Oceny Satysfakcji
```bash
GET /api/widgets/satisfaction/scores?days=30

curl "https://glass-core-467907-e9.ey.r.appspot.com/api/widgets/satisfaction/scores?days=30"
```

### 8. Custom Widget
```bash
POST /api/widgets/custom
Headers: X-API-Key: YOUR_KEY
Body: {"widget_type": "custom_chart", "data": {...}}

curl -X POST https://glass-core-467907-e9.ey.r.appspot.com/api/widgets/custom \
  -H "X-API-Key: V=iqRX16Zlp2TE+Hpz9pnT42it-L75SB" \
  -H "Content-Type: application/json" \
  -d '{"widget_type": "custom_chart", "data": {}}'
```

---

## 📤 File Upload (v2.3)

### 1. Upload Obrazu
```bash
POST /api/upload/image
Headers: X-API-Key: YOUR_KEY
Body: multipart/form-data with 'file'

curl -X POST https://glass-core-467907-e9.ey.r.appspot.com/api/upload/image \
  -H "X-API-Key: V=iqRX16Zlp2TE+Hpz9pnT42it-L75SB" \
  -F "file=@image.jpg"
```

### 2. Upload Wielu Plików
```bash
POST /api/upload/multiple
Headers: X-API-Key: YOUR_KEY
Body: multipart/form-data with multiple 'files'

curl -X POST https://glass-core-467907-e9.ey.r.appspot.com/api/upload/multiple \
  -H "X-API-Key: V=iqRX16Zlp2TE+Hpz9pnT42it-L75SB" \
  -F "files=@image1.jpg" \
  -F "files=@image2.jpg"
```

### 3. Usunięcie Pliku
```bash
POST /api/upload/delete
Headers: X-API-Key: YOUR_KEY
Body: {"file_url": "https://..."}

curl -X POST https://glass-core-467907-e9.ey.r.appspot.com/api/upload/delete \
  -H "X-API-Key: V=iqRX16Zlp2TE+Hpz9pnT42it-L75SB" \
  -H "Content-Type: application/json" \
  -d '{"file_url": "https://storage.googleapis.com/..."}'
```

---

## 🔐 RODO Compliance

### 1. Export Danych Użytkownika
```bash
POST /api/rodo/export
Body: {"user_identifier": "user@example.com"}

curl -X POST https://glass-core-467907-e9.ey.r.appspot.com/api/rodo/export \
  -H "Content-Type: application/json" \
  -d '{"user_identifier": "user@example.com"}'
```

### 2. Usunięcie Danych (Right to be Forgotten)
```bash
POST /api/rodo/delete
Body: {"user_identifier": "user@example.com", "confirm": true}

curl -X POST https://glass-core-467907-e9.ey.r.appspot.com/api/rodo/delete \
  -H "Content-Type: application/json" \
  -d '{"user_identifier": "user@example.com", "confirm": true}'
```

### 3. Sprawdzenie Zgody
```bash
POST /api/rodo/consent/check
Body: {"user_identifier": "user@example.com"}

curl -X POST https://glass-core-467907-e9.ey.r.appspot.com/api/rodo/consent/check \
  -H "Content-Type: application/json" \
  -d '{"user_identifier": "user@example.com"}'
```

---

## 📚 Dokumentacja

### 1. Swagger UI
```bash
GET /api/docs

# Otwórz w przeglądarce:
https://glass-core-467907-e9.ey.r.appspot.com/api/docs
```

### 2. OpenAPI Spec
```bash
GET /api/docs/spec

curl https://glass-core-467907-e9.ey.r.appspot.com/api/docs/spec
```

### 3. ReDoc
```bash
GET /api/docs/redoc

# Otwórz w przeglądarce:
https://glass-core-467907-e9.ey.r.appspot.com/api/docs/redoc
```

---

## 🧪 Przykładowe Testy

### Test 1: Sprawdź czy API działa
```bash
curl https://glass-core-467907-e9.ey.r.appspot.com/api/health
```

**Expected:** `{"status": "healthy", "database": "connected"}`

### Test 2: Lista backupów
```bash
curl https://glass-core-467907-e9.ey.r.appspot.com/api/backup/list \
  -H "X-API-Key: V=iqRX16Zlp2TE+Hpz9pnT42it-L75SB"
```

**Expected:** `{"success": true, "data": [...], "count": X}`

### Test 3: Wyszukiwanie
```bash
curl "https://glass-core-467907-e9.ey.r.appspot.com/api/search?q=standard&limit=5"
```

**Expected:** `{"success": true, "results": [...], "count": X}`

### Test 4: Czyszczenie backupów ⭐
```bash
curl -X POST https://glass-core-467907-e9.ey.r.appspot.com/api/backup/cleanup \
  -H "X-API-Key: V=iqRX16Zlp2TE+Hpz9pnT42it-L75SB" \
  -H "Content-Type: application/json" \
  -d '{"days_to_keep": 30}'
```

**Expected:** `{"success": true, "deleted_count": X, "days_kept": 30}`

### Test 5: Dashboard metrics
```bash
curl https://glass-core-467907-e9.ey.r.appspot.com/api/widgets/metrics/summary
```

**Expected:** `{"success": true, "data": {"total_leads": X, ...}}`

---

## 🔑 API Key

**Lokalizacja:** `app.yaml.secret` (NIE commituj!)

**Wartość:** `V=iqRX16Zlp2TE+Hpz9pnT42it-L75SB`

**Użycie:**
```bash
-H "X-API-Key: V=iqRX16Zlp2TE+Hpz9pnT42it-L75SB"
```

---

## ⚠️ Ważne Informacje

### Endpointy z API Key:
- ✅ `/api/backup/*` (wszystkie oprócz `/api/backup/list`)
- ✅ `/api/upload/*`
- ✅ `/api/search/reindex`
- ✅ `/api/widgets/custom`

### Endpointy publiczne:
- ✅ `/api/health`
- ✅ `/api/search` (GET)
- ✅ `/api/search/suggest`
- ✅ `/api/search/stats`
- ✅ `/api/widgets/*` (GET endpoints)
- ✅ `/api/rodo/*` (export, delete)
- ✅ `/api/docs`

---

## 🚀 Wersja Produkcyjna

**URL:** https://glass-core-467907-e9.ey.r.appspot.com  
**Version:** 20251114t152149  
**Status:** SERVING ✅  
**Traffic:** 100%  
**Instance:** F2 (512 MB RAM)  
**Region:** europe-west3

---

## 📊 Monitoring

```bash
# Status wersji
gcloud app versions list --service=default --project=glass-core-467907-e9

# Logi live
gcloud app logs tail --project=glass-core-467907-e9

# Health check
curl https://glass-core-467907-e9.ey.r.appspot.com/api/health
```

---

**Ostatnia aktualizacja:** 2025-11-14 15:22:49  
**Changelog:** Dodano automatyczne czyszczenie backupów (30 dni)
