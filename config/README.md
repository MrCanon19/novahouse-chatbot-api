# ⚙️ Configuration Files

> **Wszystkie pliki konfiguracyjne projektu w jednym miejscu**

---

## 📁 Struktura

```
config/
├── README.md                    # ← Ten plik
│
├── environments/                # Konfiguracje środowiskowe
│   ├── .env.example            # Template .env
│   ├── .env.development        # Development config
│   ├── .env.staging            # Staging config
│   └── .env.production         # Production config
│
├── app.yaml                    # Google App Engine config
├── cloudbuild.yaml             # Cloud Build CI/CD
├── docker-compose.yml          # Docker Compose setup
├── Dockerfile                  # Docker image definition
│
├── alembic.ini                 # Database migrations
├── gunicorn.conf.py           # Gunicorn server config
├── pytest.ini                  # Test configuration
├── .pre-commit-config.yaml    # Pre-commit hooks
├── .coveragerc                # Coverage settings
├── .editorconfig              # Editor settings
└── .flake8                    # Linting rules
```

---

## 🌍 Pliki Środowiskowe (`environments/`)

### `.env.example`

Template z wszystkimi wymaganymi zmiennymi. Kopiuj ten plik jako bazę.

```bash
# Użycie
cp config/environments/.env.example .env
```

### `.env.development`

```python
FLASK_ENV=development
DATABASE_URL=sqlite:///development.db
DEBUG=True
REDIS_URL=redis://localhost:6379  # Optional
```

### `.env.staging`

```python
FLASK_ENV=staging
DATABASE_URL=postgresql://user:pass@host/staging_db
DEBUG=False
REDIS_URL=redis://staging-redis:6379
```

### `.env.production`

```python
FLASK_ENV=production
DATABASE_URL=postgresql://user:pass@host/prod_db
DEBUG=False
REDIS_URL=redis://prod-redis:6379
SENTRY_DSN=https://...  # Error tracking
```

**Ważne:** Pliki `.env.*` są w `.gitignore` - nigdy nie commituj ich!

---

## 🚀 Deployment (`app.yaml`, `cloudbuild.yaml`)

### `app.yaml` - Google App Engine

```yaml
runtime: python311
service: default
instance_class: F2

env_variables:
  FLASK_ENV: production
  # ... wszystkie secrets
```

### `cloudbuild.yaml` - Cloud Build

```yaml
steps:
  - name: "gcr.io/cloud-builders/gcloud"
    args: ["app", "deploy", "config/app.yaml"]
```

**Deployment:**

```bash
# Z głównego katalogu
gcloud app deploy config/app.yaml

# Lub użyj Makefile
make deploy
```

---

## 🐳 Docker (`docker-compose.yml`, `Dockerfile`)

### `docker-compose.yml`

Definiuje multi-container setup:

- App (Flask)
- PostgreSQL
- Redis

**Użycie:**

```bash
# Z głównego katalogu
docker-compose -f config/docker-compose.yml up -d

# Lub użyj Makefile
make docker
make docker-down
make docker-logs
```

### `Dockerfile`

Buduje obraz aplikacji Flask.

---

## 🗄️ Database (`alembic.ini`)

### Alembic - Migracje bazy danych

```bash
# Tworzenie migracji
alembic -c config/alembic.ini revision --autogenerate -m "Description"

# Aplikowanie migracji
alembic -c config/alembic.ini upgrade head

# Lub użyj Makefile
make db-migrate msg="Description"
make db-upgrade
```

**Konfiguracja:**

```ini
[alembic]
script_location = migrations
sqlalchemy.url = ${DATABASE_URL}
file_template = %%(year)d%%(month).2d%%(day).2d_%%(hour).2d%%(minute).2d_%%(rev)s_%%(slug)s
```

---

## 🖥️ Server (`gunicorn.conf.py`)

### Gunicorn - Production server

```python
bind = "0.0.0.0:8080"
workers = 5
worker_class = "eventlet"
timeout = 120
keepalive = 5
```

**Użycie:**

```bash
gunicorn -c config/gunicorn.conf.py src.main:app
```

---

## 🧪 Testing (`pytest.ini`)

### Pytest configuration

```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

**Użycie:**

```bash
pytest -c config/pytest.ini
# lub po prostu
pytest
```

---

## 🔧 Code Quality

### `.pre-commit-config.yaml`

Automatyczne sprawdzanie przed commitem:

- black (formatting)
- isort (import sorting)
- flake8 (linting)

```bash
# Instalacja
pre-commit install

# Manual run
pre-commit run --all-files
```

### `.coveragerc`

Konfiguracja coverage testów:

```ini
[run]
source = src
omit = */tests/*
```

### `.flake8`

Reguły lintingu:

```ini
[flake8]
max-line-length = 120
exclude = .git,__pycache__,venv
```

### `.editorconfig`

Ustawienia edytora:

```ini
[*]
indent_style = space
indent_size = 4
```

---

## 🔄 Zmiana Środowiska

### Development → Staging

```bash
# 1. Skopiuj config
cp config/environments/.env.staging .env

# 2. Uruchom z nowym configiem
python main.py
```

### Staging → Production

```bash
# 1. Użyj production config
cp config/environments/.env.production .env

# 2. Deploy
make deploy
```

---

## 📝 Najczęstsze Użycia

### Setup Development

```bash
# Krok 1: Kopiuj environment
cp config/environments/.env.development .env

# Krok 2: Uruchom z Dockerem
docker-compose -f config/docker-compose.yml up -d

# Lub lokalnie
python main.py
```

### Deploy to Production

```bash
# Deploy do GCP
gcloud app deploy config/app.yaml --quiet

# Lub użyj Makefile
make deploy
```

### Database Migrations

```bash
# Utwórz migrację
alembic -c config/alembic.ini revision --autogenerate -m "Add new column"

# Aplikuj
alembic -c config/alembic.ini upgrade head

# Rollback
alembic -c config/alembic.ini downgrade -1
```

### Running Tests

```bash
# Wszystkie testy
pytest -c config/pytest.ini

# Z coverage
pytest --cov=src --cov-report=html
```

---

## 🔐 Bezpieczeństwo

### ⚠️ Nigdy nie commituj:

- `.env` (aktualny plik środowiskowy)
- `.env.production` (production secrets)
- `app.yaml.secret` (jeśli istnieje)
- Jakiekolwiek pliki z hasłami/kluczami

### ✅ Można commitować:

- `.env.example` (template bez secrets)
- `app.yaml` (jeśli używasz GCP Secret Manager)
- Wszystkie inne pliki konfiguracyjne

---

## 📚 Dokumentacja Powiązana

- **[Main README](../README.md)** - Główna dokumentacja
- **[Deployment Guide](../docs/deployment/PRODUKCJA_GOTOWA.md)** - Przewodnik wdrożenia
- **[Docker Documentation](../docs/features/DOCKER.md)** - Szczegóły Docker
- **[Security Policy](../docs/security/SECURITY.md)** - Polityka bezpieczeństwa

---

**Ostatnia aktualizacja:** 18 listopada 2025  
**Reorganizacja struktury:** Wszystkie konfiguracje w `config/`
