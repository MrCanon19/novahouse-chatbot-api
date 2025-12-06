# 🔑 Admin API Key Setup

## Czym Jest API_KEY?

API_KEY to hasło używane do autoryzacji dostępu do admin endpoints:
- Backup/Export endpointy (`/api/backup/*`)
- Dashboard widgets (`/api/widgets/*`)
- A/B testing management (`/api/ab-testing/*`)

**Bez API_KEY w produkcji = admin endpoints NIEDOSTĘPNE!**

---

## 🚀 Setup dla Środowisk

### 1. Development (Lokalne Testy)

**Opcja A: Brak API_KEY (tylko dla testów)**
```bash
# NIE ustawiaj API_KEY w .env
# Middleware automatycznie pozwoli na dostęp (development mode)
```

**Opcja B: Z API_KEY (rekomendowane)**
```bash
# W pliku .env:
API_KEY=dev-test-key-123

# Lub:
ADMIN_API_KEY=dev-test-key-123
```

Testowanie:
```bash
# Bez klucza (zostanie odrzucone jeśli API_KEY ustawiony):
curl http://localhost:8080/api/backup/list

# Z kluczem:
curl -H "X-API-Key: dev-test-key-123" \
  http://localhost:8080/api/backup/list
```

---

### 2. Production (Google Cloud)

**KROK 1: Wygeneruj silny klucz**
```bash
# 32 znaki, alfanumeryczne + special chars
python3 -c 'import secrets, string; chars = string.ascii_letters + string.digits + "_-+="; print("".join(secrets.choice(chars) for _ in range(32)))'

# Przykładowy output:
# uZ8vN-xQw3TpLmK9rY2fA+jH5cV=Bn4D
```

**KROK 2: Dodaj do app.yaml.secret**
```yaml
env_variables:
  SECRET_KEY: "2e2abf938bb057c9dea1515ec726a2ab4fc378399596e3309b1e310c4e3ff489"
  DATABASE_URL: "postgresql://..."
  MONDAY_API_KEY: "..."

  # ✅ Dodaj admin API key:
  API_KEY: "uZ8vN-xQw3TpLmK9rY2fA+jH5cV=Bn4D"

  # Optional services:
  REDIS_URL: "redis://..."
  TWILIO_ACCOUNT_SID: "..."
```

**KROK 3: Deploy**
```bash
cd /Users/michalmarini/Projects/manus/novahouse-chatbot-api
cp app.yaml.secret app.yaml.prod
gcloud app deploy app.yaml.prod
rm app.yaml.prod  # Usuń natychmiast!
```

**KROK 4: Test w produkcji**
```bash
# Bez klucza (zostanie odrzucone):
curl https://glass-core-467907-e9.ey.r.appspot.com/api/backup/list
# Response: {"error": "Unauthorized", "message": "Valid API key required"}

# Z kluczem:
curl -H "X-API-Key: uZ8vN-xQw3TpLZzQ_BkAVbz886dW_J0Yo" \
  https://glass-core-467907-e9.ey.r.appspot.com/api/backup/list
# Response: {"success": true, "backups": [...]}
```

---

## 🛡️ Jak Działa @require_api_key?

Middleware w `src/middleware/security.py`:

```python
def require_api_key(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        import os

        # Sprawdź czy API_KEY jest skonfigurowany
        api_key = os.getenv('API_KEY') or os.getenv('ADMIN_API_KEY')
        if not api_key:
            # Development mode - allow access
            return f(*args, **kwargs)

        # Sprawdź klucz w headerach
        provided_key = request.headers.get('X-API-Key') or request.headers.get('X-ADMIN-API-KEY')

        if not provided_key or provided_key != api_key:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Valid API key required'
            }), 401

        return f(*args, **kwargs)

    return wrapped
```

**Logika:**
1. **Brak API_KEY w environment** → Dostęp dozwolony (development)
2. **API_KEY ustawiony + brak X-API-Key w request** → HTTP 401
3. **API_KEY ustawiony + niepoprawny X-API-Key** → HTTP 401
4. **API_KEY ustawiony + poprawny X-API-Key** → Dostęp dozwolony

---

## 📋 Które Endpointy Wymagają API_KEY?

### Backup & Export (`src/routes/backup.py`)
- `POST /api/backup/export` - Tworzenie backup
- `GET /api/backup/list` - Lista backupów
- `GET /api/backup/download/<filename>` - Download backup
- `POST /api/backup/schedule` - Scheduled backups

### Dashboard Widgets (`src/routes/dashboard_widgets.py`)
- `GET /api/widgets/metrics/summary` - Metryki ogólne
- `GET /api/widgets/metrics/timeline` - Timeline
- `GET /api/widgets/top/intents` - Top intents
- `GET /api/widgets/top/packages` - Popularne pakiety
- `GET /api/widgets/active/sessions` - Aktywne sesje
- `GET /api/widgets/response/times` - Czasy odpowiedzi
- `GET /api/widgets/satisfaction/scores` - Oceny
- `POST /api/widgets/custom` - Custom widgets

### A/B Testing (`src/routes/ab_testing.py`)
- `POST /api/ab-testing/experiments` - Tworzenie eksperymentów
- `GET /api/ab-testing/experiments` - Lista
- `GET /api/ab-testing/experiments/<id>/results` - Wyniki
- `PUT /api/ab-testing/experiments/<id>` - Update
- `DELETE /api/ab-testing/experiments/<id>` - Usunięcie
- `POST /api/ab-testing/experiments/<id>/winner` - Wybór zwycięzcy

**UWAGA:** Endpointy RODO (`/api/rodo/*`) NIE wymagają API_KEY - są dostępne dla użytkowników końcowych.

---

## 🔐 Bezpieczeństwo

### ✅ DOBRZE:
- Używaj silnego klucza (32+ znaków, random)
- Trzymaj klucz w `app.yaml.secret` (NIE w Git!)
- Rotuj co 90 dni
- Użyj różnych kluczy dla staging/production

### ❌ ŹLE:
```yaml
# NIE rób tego!
API_KEY: "admin123"  # Za słaby
API_KEY: "test"  # Za krótki
API_KEY: "NovaHouseAPI2024"  # Łatwy do zgadnięcia
```

### 🚨 Jeśli Klucz Wycieknie:

1. **Natychmiast wygeneruj nowy**:
   ```bash
   python3 -c 'import secrets, string; chars = string.ascii_letters + string.digits + "_-+="; print("".join(secrets.choice(chars) for _ in range(32)))'
   ```

2. **Zastąp w app.yaml.secret**

3. **Redeploy aplikacji**:
   ```bash
   cp app.yaml.secret app.yaml.prod
   gcloud app deploy app.yaml.prod
   rm app.yaml.prod
   ```

4. **Zweryfikuj stary klucz NIE działa**:
   ```bash
   curl -H "X-API-Key: OLD_KEY_HERE" https://your-app.com/api/backup/list
   # Powinno zwrócić: 401 Unauthorized
   ```

---

## 📚 Przykłady Użycia

### Python
```python
import requests

API_KEY = "uZ8vN-xQw3TpLmK9rY2fA+jH5cV=Bn4D"
BASE_URL = "https://glass-core-467907-e9.ey.r.appspot.com"

headers = {"X-API-Key": API_KEY}

# Backup export
response = requests.post(
    f"{BASE_URL}/api/backup/export",
    json={"format": "json"},
    headers=headers
)
print(response.json())

# Dashboard metrics
response = requests.get(
    f"{BASE_URL}/api/widgets/metrics/summary?days=30",
    headers=headers
)
print(response.json())
```

### cURL
```bash
# Backup list
curl -H "X-API-Key: uZ8vN-xQw3TpLmK9rY2fA+jH5cV=Bn4D" \
  https://glass-core-467907-e9.ey.r.appspot.com/api/backup/list

# Dashboard summary
curl -H "X-API-Key: uZ8vN-xQw3TpLmK9rY2fA+jH5cV=Bn4D" \
  "https://glass-core-467907-e9.ey.r.appspot.com/api/widgets/metrics/summary?days=7"
```

### JavaScript (fetch)
```javascript
const API_KEY = 'uZ8vN-xQw3TpLmK9rY2fA+jH5cV=Bn4D';
const BASE_URL = 'https://glass-core-467907-e9.ey.r.appspot.com';

// Backup export
fetch(`${BASE_URL}/api/backup/export`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-API-Key': API_KEY
  },
  body: JSON.stringify({ format: 'json' })
})
.then(res => res.json())
.then(data => console.log(data));

// Dashboard widgets
fetch(`${BASE_URL}/api/widgets/metrics/summary?days=30`, {
  headers: {
    'X-API-Key': API_KEY
  }
})
.then(res => res.json())
.then(data => console.log(data));
```

---

## ⚙️ Troubleshooting

### Problem: "Valid API key required"
**Rozwiązanie:**
1. Sprawdź czy API_KEY ustawiony w environment:
   ```bash
   gcloud app deploy --version=test --no-promote
   gcloud app logs read --service=default --limit=50
   # Szukaj: "API_KEY" lub "ADMIN_API_KEY"
   ```

2. Zweryfikuj header w request:
   ```bash
   curl -v -H "X-API-Key: YOUR_KEY" https://your-app.com/api/backup/list
   # Sprawdź sekcję > Request Headers
   ```

### Problem: Development mode nie działa lokalnie
**Rozwiązanie:**
- Usuń `API_KEY` z `.env` całkowicie (nie ustawiaj na pustą wartość)
- Restart aplikacji: `gunicorn -c gunicorn.conf.py src.main:app`

### Problem: Stary klucz nadal działa po rotacji
**Rozwiązanie:**
- Sprawdź czy deploy zakończył się sukcesem:
  ```bash
  gcloud app versions list
  # Zweryfikuj czy nowa wersja ma traffic: 100%
  ```
- Force restart instancji:
  ```bash
  gcloud app instances list
  gcloud app instances delete INSTANCE_ID
  ```

---

## 📝 Changelog

- **2025-11-14**: Utworzono dokumentację API_KEY
- **2025-11-14**: Dodano @require_api_key do backup.py (4 endpoints)
- **2025-11-14**: Dodano @require_api_key do dashboard_widgets.py (8 endpoints)
- **2025-11-14**: ab_testing.py już miał @require_api_key (6 endpoints)

**Total:** 18 admin endpoints chronionych API_KEY
