# 🔐 GitHub Secrets - Instrukcja Konfiguracji

## ⚠️ WYMAGANE: Skonfiguruj Sekrety dla CI/CD

Po purge historii git, CI/CD wymaga sekretów w GitHub Settings.

## 📋 Lista Wymaganych Sekretów

Przejdź do: **GitHub → Settings → Secrets and variables → Actions → New repository secret**

### 1. GCP Deployment (Już skonfigurowane ✅)
```
GCP_SA_KEY         - JSON klucza serwisowego (treść pliku .json)
GCP_PROJECT_ID     - ID projektu GCP (np. glass-core-467907-e9)
```

### 2. Database (PostgreSQL Cloud SQL)
```
POSTGRES_HOST      - Pełna ścieżka Cloud SQL
                     Format: PROJECT:REGION:INSTANCE
                     Przykład: glass-core-467907-e9:europe-central2:novahouse-chatbot-db

POSTGRES_USER      - Nazwa użytkownika bazy danych
                     Przykład: chatbot_user

POSTGRES_PASSWORD  - Hasło do bazy danych
                     (skopiuj z app.yaml lokalnie)

POSTGRES_DB        - Nazwa bazy danych
                     Przykład: chatbot
```

### 3. OpenAI API
```
OPENAI_API_KEY     - Klucz API OpenAI
                     Format: sk-proj-...
                     Gdzie znaleźć: https://platform.openai.com/api-keys
```

### 4. Monday.com CRM
```
MONDAY_API_KEY     - Token API Monday.com
                     Gdzie znaleźć: Monday.com → Profile → Developers → API v2 Token

MONDAY_BOARD_ID    - ID tablicy Monday.com
                     (skopiuj z app.yaml lokalnie)
```

### 5. Flask Security
```
SECRET_KEY         - Flask secret key dla sessions
                     Wygeneruj: python3 -c "import secrets; print(secrets.token_hex(32))"
                     Lub użyj wartości z app.yaml lokalnie

API_KEY            - Admin API key dla backupów/dashboardów
                     Wygeneruj: python3 -c "import secrets; print(''.join(__import__('random').choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32)))"
                     Lub użyj wartości z app.yaml lokalnie
```

## 🚀 Jak Dodać Sekrety

### Metoda 1: Web UI (Zalecana)
1. Otwórz: https://github.com/MrCanon19/novahouse-chatbot-api/settings/secrets/actions
2. Kliknij **"New repository secret"**
3. Wpisz nazwę (np. `OPENAI_API_KEY`)
4. Wklej wartość
5. Kliknij **"Add secret"**
6. Powtórz dla wszystkich sekretów

### Metoda 2: GitHub CLI
```bash
# Zainstaluj GitHub CLI jeśli nie masz:
# brew install gh

# Zaloguj się:
gh auth login

# Dodaj sekrety (zamień wartości):
gh secret set OPENAI_API_KEY --body "sk-proj-YOUR_KEY_HERE"
gh secret set MONDAY_API_KEY --body "YOUR_MONDAY_TOKEN"
gh secret set MONDAY_BOARD_ID --body "YOUR_BOARD_ID"
gh secret set POSTGRES_HOST --body "glass-core-467907-e9:europe-central2:novahouse-chatbot-db"
gh secret set POSTGRES_USER --body "chatbot_user"
gh secret set POSTGRES_PASSWORD --body "YOUR_PASSWORD"
gh secret set POSTGRES_DB --body "chatbot"
gh secret set SECRET_KEY --body "YOUR_SECRET_KEY"
gh secret set API_KEY --body "YOUR_API_KEY"
```

## 🔍 Gdzie Znaleźć Wartości Sekretów

### Z Lokalnego app.yaml
```bash
# Otwórz lokalny plik (jest w .gitignore):
cat app.yaml

# Skopiuj wartości z sekcji env_variables:
OPENAI_API_KEY: "sk-proj-..."
MONDAY_API_KEY: "..."
MONDAY_BOARD_ID: "..."
SECRET_KEY: "..."
API_KEY: "..."

# Database URL - rozpakuj na części:
DATABASE_URL: "postgresql://USER:PASSWORD@/DB?host=/cloudsql/HOST"
                           ^^^^  ^^^^^^^^     ^^              ^^^^
                           |     |            |               |
                           |     |            |               POSTGRES_HOST
                           |     |            POSTGRES_DB
                           |     POSTGRES_PASSWORD
                           POSTGRES_USER
```

### Wygeneruj Nowe (Jeśli Chcesz Rotować)
```bash
# SECRET_KEY (64 hex chars):
python3 -c "import secrets; print(secrets.token_hex(32))"

# API_KEY (32 random alphanumeric):
python3 scripts/generate_credentials.py
```

## ✅ Weryfikacja

Po dodaniu wszystkich sekretów:

1. **Sprawdź listę:**
   ```
   GitHub → Settings → Secrets and variables → Actions
   ```
   Powinno być 9 sekretów:
   - GCP_SA_KEY ✅
   - GCP_PROJECT_ID ✅
   - OPENAI_API_KEY ✅
   - MONDAY_API_KEY ✅
   - MONDAY_BOARD_ID ✅
   - POSTGRES_HOST ✅
   - POSTGRES_USER ✅
   - POSTGRES_PASSWORD ✅
   - POSTGRES_DB ✅
   - SECRET_KEY ✅
   - API_KEY ✅

2. **Testuj deployment:**
   ```bash
   # Zrób pusty commit żeby trigger CI/CD:
   git commit --allow-empty -m "test: Trigger CI/CD after secrets setup"
   git push origin main
   ```

3. **Sprawdź GitHub Actions:**
   https://github.com/MrCanon19/novahouse-chatbot-api/actions

   Pipeline powinien:
   - ✅ Pass tests
   - ✅ Pass linting
   - ✅ Pass security scan
   - ✅ Deploy to App Engine (na main branch)

## 🔒 Bezpieczeństwo

- ✅ Sekrety są szyfrowane przez GitHub
- ✅ Nie są widoczne w logach CI/CD
- ✅ Tylko workflow może je odczytać
- ✅ `app.yaml` jest generowany dynamicznie i NIE commitowany

## ⚠️ Błędy i Troubleshooting

### "Deployment skipped: GCP_SA_KEY or GCP_PROJECT_ID secrets are not configured"
**Rozwiązanie:** Dodaj sekrety `GCP_SA_KEY` i `GCP_PROJECT_ID`

### "ERROR: Sekret GCP_SA_KEY nie jest ustawiony"
**Rozwiązanie:** Upewnij się że wartość to **treść JSON**, nie ścieżka do pliku

### "Invalid GCP_SA_KEY format"
**Rozwiązanie:** Skopiuj **CAŁĄ treść** pliku .json klucza serwisowego, włącznie z `{` i `}`

### "Could not connect to database"
**Rozwiązanie:**
1. Sprawdź `POSTGRES_HOST` - musi być format: `PROJECT:REGION:INSTANCE`
2. Sprawdź `POSTGRES_PASSWORD` - bez spacji na początku/końcu
3. Upewnij się że Cloud SQL ma włączone połączenia z App Engine

---

**Utworzone:** 2025-12-03  
**Status:** ⚠️ WYMAGA AKCJI - Dodaj sekrety do GitHub przed następnym deploymentem
