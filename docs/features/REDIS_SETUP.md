# Redis Cache Configuration for Production

## 🎯 Opcje konfiguracji Redis w GCP

### Opcja 1: Google Cloud Memorystore (Polecana)

**Koszt:** ~$25/month (1GB, basic tier)  
**Czas setup:** 10-15 min

```bash
# 1. Stwórz Redis instance
gcloud redis instances create novahouse-cache \
    --size=1 \
    --region=europe-west1 \
    --redis-version=redis_6_x \
    --tier=basic

# 2. Pobierz connection string
gcloud redis instances describe novahouse-cache --region=europe-west1

# 3. Dodaj do app.yaml (skopiuj host z output)
env_variables:
  REDIS_URL: "redis://REDIS_HOST:6379/0"
```

### Opcja 2: Redis Labs (External)

**Koszt:** Free do 30MB, $7/month dla 100MB  
**Czas setup:** 5 min

1. Zarejestruj się: https://redis.com/try-free/
2. Utwórz nową bazę (wybierz Europe region)
3. Skopiuj Redis URL
4. Dodaj do `app.yaml`:

```yaml
env_variables:
  REDIS_URL: "redis://:PASSWORD@HOST:PORT/0"
```

### Opcja 3: Upstash (Serverless Redis)

**Koszt:** Free do 10k commands/day, $0.20 per 100k potem  
**Czas setup:** 3 min

1. https://upstash.com/ -> Create Database
2. Region: Europe (eu-west-1)
3. Skopiuj REST URL
4. Dodaj do `app.yaml`

---

## 📝 Aktualna implementacja

W `src/middleware/cache.py` masz już:

- ✅ Fallback do in-memory jeśli Redis nie dostępny
- ✅ Funkcje: `cache_get()`, `cache_set()`, `cache_delete()`
- ✅ TTL support

**Wystarczy dodać REDIS_URL do app.yaml i zadziała automatycznie!**

---

## 🚀 Quick Setup (Upstash - FREE)

```bash
# 1. Zarejestruj się na Upstash
open https://upstash.com/

# 2. Create Database -> Region: eu-west-1

# 3. Skopiuj Redis URL (format: redis://default:PASSWORD@HOST:PORT)

# 4. Dodaj do app.yaml
# REDIS_URL: "redis://default:TWOJ_PASSWORD@eu-west-1.upstash.io:6379"

# 5. Deploy
gcloud app deploy

# 6. Test
curl https://glass-core-467907-e9.ey.r.appspot.com/api/chatbot/health
```

Sprawdź w health check czy Redis działa: `"cache_status": "redis"` zamiast `"in-memory"`.

---

**Rekomendacja:** Zacznij od Upstash (FREE), później upgrade na Memorystore jeśli będzie potrzeba.
