# 🚨 AUDYT BEZPIECZEŃSTWA - KRYTYCZNE PROBLEMY DO NAPRAWY

**Data:** 2025-12-03  
**Audytor:** AI Inspector (40 years experience mode)  
**Status:** 🔴 CRITICAL ISSUES FOUND

---

## 🔥 PROBLEM #1: SECRETS W GIT REPOSITORY (KRYTYCZNY)

### Lokalizacja
`app.yaml` (tracked w git od wielu commitów)

### Co jest ujawnione
```yaml
SECRET_KEY: "2e2abf938bb057c9dea1515ec726a2ab4fc378399596e3309b1e310c4e3ff489"
API_KEY: "V=iqRX16Zlp2TE+Hpz9pnT42it-L75SB"
DATABASE_URL: "postgresql://chatbot_user:vicNRNoO3TpLZzQ_BkAVbz886dW_J0Yo@..."
OPENAI_API_KEY: "sk-proj-8vaVJhu24SUPyleLWEgK..."
MONDAY_API_KEY: "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjU2MTI0OTM2MiwiYWFp..."
```

### Ryzyko
- ✅ **SEVERITY: CRITICAL**
- Każdy z dostępem do GitHub repo ma full access do:
  - Bazy danych produkcyjnej (RODO violation)
  - OpenAI API (nieograniczone koszty)
  - Monday.com CRM (manipulacja danych klientów)
  - Admin panel (pełna kontrola systemu)

### Historia w git
```bash
$ git log --oneline app.yaml | head -3
e40c12e CRITICAL FIX: Usuń Sentry SDK
2e9ff01 CLEANUP: Usunięto GCS
4f35399 FINALNA OPTYMALIZACJA: 55% redukcja kosztów
```

**Secrets są w git history od wielu miesięcy!**

### Co trzeba naprawić NATYCHMIAST

#### 1. Stop tracking app.yaml
```bash
git rm --cached app.yaml
echo "app.yaml" >> .gitignore
git commit -m "SECURITY: Stop tracking app.yaml with secrets"
```

#### 2. Rotate ALL credentials
- [ ] SECRET_KEY → nowy `secrets.token_hex(32)`
- [ ] API_KEY → nowy random string
- [ ] DATABASE_URL → zmień hasło PostgreSQL w Cloud SQL
- [ ] OPENAI_API_KEY → regeneruj w OpenAI dashboard
- [ ] MONDAY_API_KEY → regeneruj w Monday.com settings

#### 3. Use GCP Secret Manager (best practice)
```python
from google.cloud import secretmanager

def get_secret(secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# W app config
os.environ["OPENAI_API_KEY"] = get_secret("openai-api-key")
```

#### 4. CI/CD używa GitHub Secrets (już OK)
Workflow już poprawnie używa secrets dla deployment - to działa dobrze.

---

## 🔥 PROBLEM #2: SQL INJECTION VULNERABILITY

### Lokalizacja
`src/routes/migration.py` linie 219, 287

### Kod podatny
```python
# LINE 219
db.session.execute(
    text(f"ALTER TABLE chat_conversations ADD COLUMN {column_name} {column_type}")
)

# LINE 287
db.session.execute(
    text(f"ALTER TABLE leads ADD COLUMN {column_name} {column_type}")
)
```

### Ryzyko
- **SEVERITY: HIGH**
- String interpolacja w SQL (f-string)
- Jeśli `column_name` lub `column_type` pochodzi z user input → SQL injection
- Endpoint chroniony `@require_api_key` ale klucz jest w git (problem #1)

### Przykład exploitation
```bash
# Request do migration endpoint
POST /api/migration/add-chat-columns
{
  "columns": {
    "malicious; DROP TABLE leads; --": "TEXT"
  }
}
```

Wynik: `ALTER TABLE chat_conversations ADD COLUMN malicious; DROP TABLE leads; -- TEXT`

### Co trzeba naprawić
**NIGDY nie używaj f-strings w SQL!**

#### Option A: Whitelist allowed columns (RECOMMENDED)
```python
ALLOWED_COLUMNS = {
    "context_data": "JSONB",
    "lead_score": "INTEGER",
    "sentiment": "VARCHAR(20)"
}

column_name = request.json.get("column_name")
if column_name not in ALLOWED_COLUMNS:
    return jsonify({"error": "Invalid column"}), 400

column_type = ALLOWED_COLUMNS[column_name]
# Teraz bezpieczne - hardcoded values
db.session.execute(
    text(f"ALTER TABLE chat_conversations ADD COLUMN {column_name} {column_type}")
)
```

#### Option B: Use identifier quoting (SQLAlchemy)
```python
from sqlalchemy.sql import literal_column

# Escape identifiers properly
safe_column = literal_column(column_name)
safe_type = literal_column(column_type)
```

**JEDNAK:** DDL statements (ALTER TABLE) nie powinny przyjmować user input w ogóle!

---

## ⚠️ PROBLEM #3: Rate Limiter tylko in-memory

### Lokalizacja
`src/middleware/security.py`

### Kod
```python
class RateLimiter:
    def __init__(self):
        self.requests = defaultdict(list)  # In-memory dict
```

### Ryzyko
- **SEVERITY: MEDIUM**
- Rate limiting nie działa między instancjami App Engine
- Przy `max_instances: 5` każda instancja ma swój licznik
- Attacker może wysłać 5x więcej requestów niż limit

### Przykład
- Limit: 100 req/min
- App Engine: 3 aktywne instancje
- Faktyczny limit: **300 req/min** (3x100)

### Co trzeba naprawić
**Use Redis dla rate limiting**

```python
import redis
from flask import current_app

class RateLimiter:
    def __init__(self):
        redis_url = os.getenv("REDIS_URL")
        if redis_url:
            self.redis = redis.from_url(redis_url)
        else:
            self.redis = None
            self.requests = defaultdict(list)  # Fallback

    def is_allowed(self, key: str, max_requests: int, window_seconds: int) -> bool:
        if self.redis:
            # Redis atomic increment with TTL
            pipe = self.redis.pipeline()
            pipe.incr(key)
            pipe.expire(key, window_seconds)
            result = pipe.execute()
            return result[0] <= max_requests
        else:
            # Fallback to in-memory (development only)
            # ... existing code ...
```

**UWAGA:** Redis URL nie jest w app.yaml (optional feature) ale powinien być dla production.

---

## 📊 PROBLEM #4: Test Coverage 29.05% (ZBYT NISKI)

### Current state
```
55/58 tests passing
3 integration tests skipped (Monday, OpenAI, Zencal)
Coverage: 29.05%
```

### Ryzyko
- **SEVERITY: MEDIUM**
- 71% kodu nie jest testowane
- Krytyczne ścieżki mogą być broken bez wykrycia
- Integration tests wymagają API keys (nie działają w CI)

### Co trzeba naprawić

#### 1. Mock external services
```python
# tests/test_integrations.py
@pytest.fixture
def mock_openai(monkeypatch):
    def mock_chat(*args, **kwargs):
        return {"choices": [{"message": {"content": "Test response"}}]}

    monkeypatch.setattr("openai.ChatCompletion.create", mock_chat)

def test_chatbot_with_mocked_openai(client, mock_openai):
    # Teraz test działa bez OPENAI_API_KEY
    response = client.post("/api/chat", json={"message": "test"})
    assert response.status_code == 200
```

#### 2. Target 60% coverage minimum
Priorytetowe pliki do pokrycia:
- `src/routes/chatbot.py` (core logic)
- `src/services/message_handler.py` (AI integration)
- `src/middleware/security.py` (auth/rate limiting)
- `src/models/*.py` (data models)

#### 3. CI/CD coverage enforcement
```yaml
# .github/workflows/ci-cd.yml
- name: Check coverage threshold
  run: |
    coverage report --fail-under=60
```

---

## 🔍 PROBLEM #5: Brak monitoring dla secrets rotation

### Lokalizacja
Secrets w app.yaml nie mają expiration date ani alertów

### Ryzyko
- **SEVERITY: LOW**
- Secrets nigdy nie są rotowane (security best practice: 90 days)
- Brak alertów gdy API keys wygasają
- Brak audit logs kto używał secrets

### Co trzeba naprawić

#### 1. Document rotation schedule
```markdown
# docs/SECRETS_ROTATION.md

## Rotation Schedule (każde 90 dni)
- SECRET_KEY: 2025-11-14 (next: 2026-02-12)
- API_KEY: 2025-11-14 (next: 2026-02-12)
- PostgreSQL: 2025-11-14 (next: 2026-02-12)
- OPENAI_API_KEY: sprawdź w dashboard
- MONDAY_API_KEY: sprawdź w settings
```

#### 2. GCP Secret Manager versioning
```bash
# Create secret with automatic rotation
gcloud secrets create openai-api-key \
  --replication-policy="automatic" \
  --rotation-period="7776000s" \  # 90 days
  --next-rotation-time="2026-02-12T00:00:00Z"
```

#### 3. Alert gdy secret wkrótce expire
```python
# src/services/secret_monitor.py
from datetime import datetime, timedelta

def check_secret_expiration():
    """Check if secrets need rotation"""
    rotation_file = "docs/SECRETS_ROTATION.md"
    # Parse rotation dates
    # Send alert if < 7 days to rotation
```

---

## ✅ CO JEST DOBRE

### 1. SQLAlchemy ORM Usage
Większość zapytań używa ORM (parametryzowane zapytania) - to jest OK:
```python
Lead.query.filter_by(email=email).first()  # ✅ Safe
db.session.add(new_lead)  # ✅ Safe
```

### 2. API Key Protection
Endpointy admin chronione `@require_api_key` decorator:
```python
@require_api_key
def backup_endpoint():
    ...
```

**ALE:** API_KEY jest w git (problem #1) więc każdy może go użyć.

### 3. CORS Configuration
```python
CORS(app, origins=["https://glass-core-467907-e9.ey.r.appspot.com"])
```
Production domain whitelisted - OK.

### 4. File Upload Security
```python
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB
```
Extension whitelist + size limit - OK.

### 5. CI/CD Validation
Workflow sprawdza czy GCP_SA_KEY matches GCP_PROJECT_ID - excellent defensive coding!

---

## 📋 PRIORITY ACTION ITEMS

### 🔴 CRITICAL (Fix Today)
1. [ ] Stop tracking `app.yaml` w git
2. [ ] Rotate ALL secrets (SECRET_KEY, API_KEY, DB password, OpenAI, Monday)
3. [ ] Fix SQL injection w `migration.py` (whitelist columns)

### 🟠 HIGH (Fix This Week)
4. [ ] Migrate to GCP Secret Manager
5. [ ] Add Redis for distributed rate limiting
6. [ ] Increase test coverage do 60%+

### 🟡 MEDIUM (Fix This Month)
7. [ ] Document secrets rotation schedule
8. [ ] Add monitoring for secret expiration
9. [ ] Mock external services w integration tests

---

## 🎯 NASTĘPNE KROKI

1. **Zatrzymaj wszystko** - najpierw bezpieczeństwo
2. **Rotate credentials** zanim ktokolwiek ich użyje
3. **Fix SQL injection** przed następnym deploymentem
4. **Migrate to Secret Manager** w następnym sprincie
5. **Increase test coverage** systematycznie (po 5% tygodniowo)

---

**Raport wygenerowany:** 2025-12-03  
**Auditor:** GitHub Copilot (40 years experience mode)  
**Szorstka miłość:** ✅ Delivered
