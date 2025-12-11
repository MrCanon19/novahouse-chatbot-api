# 🚨 Runbook: Disaster Recovery

**Data utworzenia:** 11 grudnia 2025  
**Cel:** Procedury odtwarzania systemu po awarii

---

## 📋 Scenariusze awarii

### 1. Awaria bazy danych

#### Symptomy
- Błędy 503 "Database temporarily unavailable"
- Logi: `Database connection error`
- Aplikacja nie może połączyć się z PostgreSQL

#### Procedura odtwarzania

**Krok 1: Sprawdź status bazy**
```bash
# Sprawdź czy baza działa
psql -h [DB_HOST] -U [DB_USER] -d [DB_NAME] -c "SELECT 1"

# Sprawdź logi GCP Cloud SQL
gcloud sql operations list --instance=[INSTANCE_NAME]
```

**Krok 2: Przywróć z backupu**
```bash
# Lista dostępnych backupów
curl -H "X-API-Key: $ADMIN_API_KEY" https://[APP_URL]/api/backup/list

# Przywróć najnowszy backup
# (wymaga dostępu do Cloud SQL)
gcloud sql backups restore [BACKUP_ID] --backup-instance=[INSTANCE_NAME]
```

**Krok 3: Zweryfikuj przywrócenie**
```bash
# Uruchom smoke-testy
pytest tests/test_api.py tests/test_chatbot.py -v

# Sprawdź health check
curl https://[APP_URL]/api/health/deep
```

**Krok 4: Monitoruj**
- Sprawdź metryki: `/api/monitoring/metrics`
- Sprawdź logi błędów w GCP Console
- Monitoruj Sentry (jeśli skonfigurowane)

---

### 2. Awaria Redis

#### Symptomy
- Rate limiting nie działa
- Cache nie działa
- Logi: `Redis unavailable, using fallback`

#### Procedura odtwarzania

**Krok 1: Sprawdź status Redis**
```bash
# Sprawdź połączenie
redis-cli -h [REDIS_HOST] ping

# Sprawdź metryki
redis-cli -h [REDIS_HOST] INFO stats
```

**Krok 2: Restart Redis (jeśli potrzebne)**
```bash
# GCP Memorystore
gcloud redis instances describe [INSTANCE_NAME] --region=[REGION]

# Restart (jeśli dostępne)
gcloud redis instances restart [INSTANCE_NAME] --region=[REGION]
```

**Krok 3: Aplikacja działa bez Redis**
- ✅ Aplikacja automatycznie przełącza się na fallback (in-memory)
- ✅ Rate limiting działa lokalnie
- ✅ Cache działa lokalnie
- ⚠️  Sesje mogą stracić część danych telemetrycznych

**Krok 4: Monitoruj**
- Sprawdź logi: `Redis unavailable, using fallback`
- Sprawdź metryki: `/api/monitoring/metrics`
- Po przywróceniu Redis, aplikacja automatycznie przełączy się z powrotem

---

### 3. Awaria aplikacji (crash)

#### Symptomy
- 502 Bad Gateway
- Aplikacja nie odpowiada
- Logi: `Application error`

#### Procedura odtwarzania

**Krok 1: Sprawdź status aplikacji**
```bash
# GCP App Engine
gcloud app versions list --service=[SERVICE_NAME]

# Sprawdź logi
gcloud app logs read --service=[SERVICE_NAME] --limit=50
```

**Krok 2: Przywróć poprzednią wersję**
```bash
# Lista wersji
gcloud app versions list --service=[SERVICE_NAME]

# Przywróć poprzednią wersję
gcloud app versions migrate [PREVIOUS_VERSION] --service=[SERVICE_NAME]
```

**Krok 3: Uruchom nową instancję**
```bash
# Deploy nowej wersji
gcloud app deploy app.yaml --version=[NEW_VERSION]

# Przełącz ruch na nową wersję
gcloud app versions migrate [NEW_VERSION] --service=[SERVICE_NAME]
```

**Krok 4: Zweryfikuj**
```bash
# Health check
curl https://[APP_URL]/api/health/deep

# Smoke-testy
pytest tests/test_api.py -v
```

---

### 4. Pełna katastrofa (utrata całego środowiska)

#### Procedura odtwarzania

**Krok 1: Utwórz nowe środowisko**
```bash
# Utwórz nowy projekt GCP (jeśli potrzebne)
gcloud projects create [NEW_PROJECT_ID]

# Utwórz Cloud SQL instance
gcloud sql instances create [INSTANCE_NAME] \
  --database-version=POSTGRES_14 \
  --tier=db-f1-micro \
  --region=[REGION]

# Utwórz bazę danych
gcloud sql databases create [DB_NAME] --instance=[INSTANCE_NAME]
```

**Krok 2: Przywróć bazę z backupu**
```bash
# Lista backupów w GCS
gsutil ls gs://[BACKUP_BUCKET]/backups/

# Przywróć najnowszy backup
gcloud sql import sql [INSTANCE_NAME] gs://[BACKUP_BUCKET]/backups/[BACKUP_FILE] \
  --database=[DB_NAME]
```

**Krok 3: Skonfiguruj aplikację**
```bash
# Ustaw zmienne środowiskowe
gcloud app deploy app.yaml --set-env-vars \
  DATABASE_URL=postgresql://[USER]:[PASS]@[HOST]/[DB_NAME] \
  REDIS_URL=redis://[REDIS_HOST]:6379 \
  OPENAI_API_KEY=[KEY] \
  ADMIN_API_KEY=[KEY]

# Deploy aplikacji
gcloud app deploy app.yaml
```

**Krok 4: Zmień DNS / Load Balancer**
```bash
# Jeśli używasz własnej domeny
# Zaktualizuj DNS A record na nowy IP App Engine

# Jeśli używasz Cloud Load Balancer
gcloud compute backend-services update [BACKEND_SERVICE] \
  --add-backend group=[NEW_INSTANCE_GROUP]
```

**Krok 5: Zweryfikuj**
```bash
# Health check
curl https://[APP_URL]/api/health/deep

# Smoke-testy
pytest tests/test_api.py tests/test_chatbot.py -v

# Sprawdź metryki
curl https://[APP_URL]/api/monitoring/metrics
```

---

## 🔧 Narzędzia i komendy

### Backup i restore

```bash
# Utwórz backup ręcznie
curl -X POST -H "X-API-Key: $ADMIN_API_KEY" \
  https://[APP_URL]/api/backup/export \
  -d '{"format": "json"}'

# Lista backupów
curl -H "X-API-Key: $ADMIN_API_KEY" \
  https://[APP_URL]/api/backup/list

# Pobierz backup
curl -H "X-API-Key: $ADMIN_API_KEY" \
  https://[APP_URL]/api/backup/download/[FILENAME] \
  -o backup.json
```

### Monitoring

```bash
# Health check
curl https://[APP_URL]/api/health/deep

# Metryki
curl https://[APP_URL]/api/monitoring/metrics

# Status
curl https://[APP_URL]/api/monitoring/status
```

### Logi

```bash
# GCP App Engine logi
gcloud app logs read --service=[SERVICE_NAME] --limit=100

# GCP Cloud SQL logi
gcloud sql operations list --instance=[INSTANCE_NAME]

# Filtruj błędy
gcloud app logs read --service=[SERVICE_NAME] --severity=ERROR
```

---

## 📞 Kontakty

- **DevOps:** [EMAIL]
- **Database Admin:** [EMAIL]
- **On-call:** [PHONE]

---

## ✅ Checklist odtwarzania

- [ ] Zidentyfikowano przyczynę awarii
- [ ] Przywrócono backup bazy danych
- [ ] Zweryfikowano przywrócenie (smoke-testy)
- [ ] Sprawdzono health check
- [ ] Sprawdzono metryki
- [ ] Powiadomiono zespół
- [ ] Zaktualizowano dokumentację (jeśli potrzebne)

---

**Ostatnia aktualizacja:** 11 grudnia 2025

