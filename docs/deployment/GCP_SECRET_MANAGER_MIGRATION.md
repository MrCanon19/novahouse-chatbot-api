# 🔐 Migracja sekretów do GCP Secret Manager

## 📋 Przegląd

Obecnie sekrety są przechowywane w `app.yaml` (który jest w `.gitignore`).  
Dla większego bezpieczeństwa, rekomendujemy migrację do **GCP Secret Manager**.

## ✅ Zalety GCP Secret Manager

1. **Centralne zarządzanie** - wszystkie sekrety w jednym miejscu
2. **Wersjonowanie** - możliwość rotacji bez zmiany kodu
3. **Audyt** - pełna historia dostępu do sekretów
4. **Automatyczna rotacja** - możliwość automatycznego odświeżania
5. **Bezpieczeństwo** - szyfrowanie w spoczynku i transporcie

## 🚀 Krok 1: Utwórz sekrety w GCP Secret Manager

### Przez GCP Console (zalecane)

1. Otwórz: https://console.cloud.google.com/security/secret-manager?project=glass-core-467907-e9
2. Kliknij **"CREATE SECRET"**
3. Dla każdego sekretu:

#### SECRET_KEY
- **Name:** `SECRET_KEY`
- **Value:** `2e2abf938bb057c9dea1515ec726a2ab4fc378399596e3309b1e310c4e3ff489`
- **Replication:** Automatic

#### ADMIN_API_KEY
- **Name:** `ADMIN_API_KEY`
- **Value:** `V=iqRX16Zlp2TE+Hpz9pnT42it-L75SB`

#### OPENAI_API_KEY
- **Name:** `OPENAI_API_KEY`
- **Value:** `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`

#### MONDAY_API_KEY
- **Name:** `MONDAY_API_KEY`
- **Value:** `eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjU2MTI0OTM2MiwiYWFpIjoxMSwidWlkIjo2NzA0MDY5NCwiaWFkIjoiMjAyNS0wOS0xMlQwNjo1ODoxOC4yNzVaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MjU4NDk4NzEsInJnbiI6ImV1YzEifQ.Z-5M7pm_QZa1YBQ4a5caSg6XZlM4X1_fTcnF5JmQJyw`

#### MONDAY_BOARD_ID
- **Name:** `MONDAY_BOARD_ID`
- **Value:** `2145240699`

#### DATABASE_URL
- **Name:** `DATABASE_URL`
- **Value:** `postgresql://chatbot_user:NovaH0use2025!DB@/chatbot?host=/cloudsql/glass-core-467907-e9:europe-west1:novahouse-chatbot-db`

### Przez gcloud CLI (szybsze)

```bash
# Ustaw projekt
gcloud config set project glass-core-467907-e9

# Utwórz sekrety
echo -n "2e2abf938bb057c9dea1515ec726a2ab4fc378399596e3309b1e310c4e3ff489" | \
  gcloud secrets create SECRET_KEY --data-file=-

echo -n "V=iqRX16Zlp2TE+Hpz9pnT42it-L75SB" | \
  gcloud secrets create ADMIN_API_KEY --data-file=-

echo -n "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" | \
  gcloud secrets create OPENAI_API_KEY --data-file=-

echo -n "eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjU2MTI0OTM2MiwiYWFpIjoxMSwidWlkIjo2NzA0MDY5NCwiaWFkIjoiMjAyNS0wOS0xMlQwNjo1ODoxOC4yNzVaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MjU4NDk4NzEsInJnbiI6ImV1YzEifQ.Z-5M7pm_QZa1YBQ4a5caSg6XZlM4X1_fTcnF5JmQJyw" | \
  gcloud secrets create MONDAY_API_KEY --data-file=-

echo -n "2145240699" | \
  gcloud secrets create MONDAY_BOARD_ID --data-file=-

echo -n "postgresql://chatbot_user:NovaH0use2025!DB@/chatbot?host=/cloudsql/glass-core-467907-e9:europe-west1:novahouse-chatbot-db" | \
  gcloud secrets create DATABASE_URL --data-file=-
```

## 🔑 Krok 2: Nadaj uprawnienia App Engine Service Account

App Engine automatycznie używa service account do dostępu do sekretów.

```bash
# Pobierz service account email
SERVICE_ACCOUNT=$(gcloud app describe --format="value(serviceAccount)")

# Nadaj uprawnienia do odczytu sekretów
gcloud secrets add-iam-policy-binding SECRET_KEY \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding ADMIN_API_KEY \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding OPENAI_API_KEY \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding MONDAY_API_KEY \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding MONDAY_BOARD_ID \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/secretmanager.secretAccessor"

gcloud secrets add-iam-policy-binding DATABASE_URL \
  --member="serviceAccount:${SERVICE_ACCOUNT}" \
  --role="roles/secretmanager.secretAccessor"
```

## 📝 Krok 3: Zaktualizuj app.yaml

Zamień hardcoded sekrety na referencje do Secret Manager:

```yaml
runtime: python311
service: default
instance_class: F2

entrypoint: gunicorn -c config/gunicorn.conf.py main:app

runtime_config:
  python_version: 3.11

env_variables:
  FLASK_ENV: production

# Sekrety z GCP Secret Manager
# Format: projects/PROJECT_ID/secrets/SECRET_NAME/versions/latest
env:
  - name: SECRET_KEY
    value_from:
      secret_key_ref:
        name: projects/glass-core-467907-e9/secrets/SECRET_KEY/versions/latest
  - name: ADMIN_API_KEY
    value_from:
      secret_key_ref:
        name: projects/glass-core-467907-e9/secrets/ADMIN_API_KEY/versions/latest
  - name: OPENAI_API_KEY
    value_from:
      secret_key_ref:
        name: projects/glass-core-467907-e9/secrets/OPENAI_API_KEY/versions/latest
  - name: MONDAY_API_KEY
    value_from:
      secret_key_ref:
        name: projects/glass-core-467907-e9/secrets/MONDAY_API_KEY/versions/latest
  - name: MONDAY_BOARD_ID
    value_from:
      secret_key_ref:
        name: projects/glass-core-467907-e9/secrets/MONDAY_BOARD_ID/versions/latest
  - name: DATABASE_URL
    value_from:
      secret_key_ref:
        name: projects/glass-core-467907-e9/secrets/DATABASE_URL/versions/latest

automatic_scaling:
  min_instances: 0
  max_instances: 2
  target_cpu_utilization: 0.7
  target_throughput_utilization: 0.7
  max_concurrent_requests: 25
  min_idle_instances: 0
  max_idle_instances: 0

beta_settings:
  cloud_sql_instances: "glass-core-467907-e9:europe-west1:novahouse-chatbot-db"
```

## ⚠️ UWAGA: App Engine Standard Environment

**App Engine Standard Environment NIE obsługuje bezpośrednio Secret Manager w `app.yaml`!**

Musisz użyć jednej z tych opcji:

### Opcja A: Runtime Secret Access (Python)

Dodaj kod w `src/main.py` do pobierania sekretów:

```python
from google.cloud import secretmanager

def get_secret(secret_id: str) -> str:
    """Pobierz sekret z GCP Secret Manager"""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/glass-core-467907-e9/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")

# W main.py, przed użyciem os.getenv():
if os.getenv("FLASK_ENV") == "production":
    # Pobierz sekrety z Secret Manager
    os.environ["SECRET_KEY"] = get_secret("SECRET_KEY")
    os.environ["ADMIN_API_KEY"] = get_secret("ADMIN_API_KEY")
    os.environ["OPENAI_API_KEY"] = get_secret("OPENAI_API_KEY")
    os.environ["MONDAY_API_KEY"] = get_secret("MONDAY_API_KEY")
    os.environ["MONDAY_BOARD_ID"] = get_secret("MONDAY_BOARD_ID")
    os.environ["DATABASE_URL"] = get_secret("DATABASE_URL")
```

### Opcja B: Pozostań przy env_variables (obecne rozwiązanie)

**To jest OK!** `app.yaml` jest w `.gitignore`, więc sekrety są bezpieczne.

Migracja do Secret Manager jest **opcjonalna** i wymaga:
- Dodania `google-cloud-secret-manager` do `requirements.txt`
- Zmiany kodu w `main.py`
- Testowania na staging

## 🧪 Krok 4: Testowanie

```bash
# Deploy na staging
gcloud app deploy app.yaml --version=staging --project=glass-core-467907-e9

# Sprawdź logi
gcloud app logs tail -s default --version=staging

# Test health endpoint
curl https://staging-dot-glass-core-467907-e9.ey.r.appspot.com/api/health
```

## 📊 Podsumowanie

| Metoda | Bezpieczeństwo | Łatwość | Rekomendacja |
|--------|----------------|---------|--------------|
| **app.yaml (obecne)** | ✅ OK (w .gitignore) | ✅ Łatwe | ✅ **Wystarczające** |
| **Secret Manager** | ✅✅ Najlepsze | ⚠️ Wymaga zmian w kodzie | ⚠️ **Opcjonalne** |

**Rekomendacja:** Jeśli `app.yaml` jest w `.gitignore` i nie jest commitowany, obecne rozwiązanie jest **wystarczające**.  
Secret Manager warto rozważyć dla:
- Większych projektów z wieloma sekretami
- Wymagań compliance (GDPR, SOC2)
- Automatycznej rotacji sekretów

