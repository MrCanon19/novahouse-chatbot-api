# CI/CD Pipeline Setup Guide

## Overview

Pipeline automatycznie uruchamia się na każdy push do `main` i wykonuje:
1. ✅ **Unit Tests** - pytest z coverage
2. ✅ **Linting** - flake8 + black
3. ✅ **Security Scan** - Trivy vulnerability scanner
4. 🚀 **Deployment** - Do GCP App Engine (opcjonalnie)

---

## 🔧 Konfiguracja GitHub Secrets

### Dla testów CI/CD (obowiązkowe)

Nie ma obowiązkowych sekrecie dla testów. Pipeline uruchomi się zawsze dla:
- Unit tests
- Linting
- Security scanning

### Dla deployment'u (opcjonalnie)

Jeśli chcesz aby pipeline automatycznie deployował do GCP, ustaw te sekrety:

**Settings > Secrets and variables > Actions > New repository secret**

#### 1. `GCP_SA_KEY`
```
Service Account JSON Key (JSON format)
```
- Pobierz z GCP Console: `Service Accounts > Create Key > JSON`
- Upewnij się że format to **JSON** (nie base64)
- Skopiuj całą zawartość pliku `.json`

#### 2. `GCP_PROJECT_ID`
```
Twój GCP Project ID
```
Przykład: `glass-core-467907-e9`

#### 3. `OPENAI_API_KEY` (opcjonalnie)
```
Twój OpenAI API Key
```
- Wymaga jeśli chcesz integracji ChatGPT

#### 4. `MONDAY_API_KEY` (opcjonalnie)
```
Monday.com API Token
```

#### 5. `MONDAY_BOARD_ID` (opcjonalnie)
```
Monday.com Board ID
```

#### 6. `POSTGRES_HOST`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` (opcjonalnie)
```
PostgreSQL connection details
```

#### 7. `SECRET_KEY` (opcjonalnie)
```
Flask SECRET_KEY
```

#### 8. `API_KEY` (opcjonalnie)
```
Custom API Key
```

---

## 📊 Pipeline Status

### Testy (zawsze uruchamiają się)

```yaml
- Python 3.13
- Dependencies z requirements.txt
- Unit tests: pytest tests/ (ignoring integration)
- Coverage: 30%+
```

### Linting

```yaml
- flake8: E9, F63, F7, F82 (błędy krytyczne)
- black: Code formatting check (informacyjne)
```

### Security Scan

```yaml
- Trivy: Vulnerability scanner
- Uploads to GitHub Security tab
```

### Deployment (jeśli sekrety ustawione)

```yaml
- Wymaga: GCP_SA_KEY + GCP_PROJECT_ID
- Warunek: push do main
- Fallback: Deployment skipowany jeśli sekrety nie dostępne
```

---

## 🚨 Troubleshooting

### ❌ "Deployment skipped: GCP secrets not configured"

**To jest OK!** Pipeline będzie działał normalnie:
- ✅ Testy będą się uruchamiać
- ✅ Linting będzie działać
- ✅ Security scan będzie działać
- ℹ️ Deployment do GCP będzie pominięty

Aby włączyć deployment:
1. Przejdź do repozytorium na GitHub
2. Settings > Secrets and variables > Actions
3. Dodaj `GCP_SA_KEY` i `GCP_PROJECT_ID`

### ❌ "Run failed: CI/CD Pipeline"

Jeśli testy failują:

1. **Sprawdź Python version**
   ```bash
   python --version  # Powinien być 3.13+
   ```

2. **Zainstaluj dependencies**
   ```bash
   pip install -r requirements.txt
   pip install pytest pytest-cov flake8 black
   ```

3. **Uruchom testy lokalnie**
   ```bash
   pytest tests/ --cov=src --ignore=tests/integration
   ```

4. **Sprawdź linting**
   ```bash
   flake8 src/
   black --check src/
   ```

### ❌ GCP_SA_KEY Invalid Format

Upewnij się że:
- Format to **JSON** (nie base64)
- Zawartość zaczyna się od `{`
- Brak linii startowych/końcowych

Poprawa:
```bash
# Pobierz nowy key z GCP
# Otwórz w tekście edytorze
# Sprawdź czy to poprawny JSON
# Skopiuj całą zawartość (od { do })
# Wklej do GitHub Secret
```

---

## 📈 Monitoring

Sprawdź status pipeline'u:

1. **GitHub**: https://github.com/MrCanon19/novahouse-chatbot-api/actions
2. **Ostatnie runs**: Po każdym push na main
3. **Badge**: Dodaj do README.md:
   ```markdown
   ![CI/CD Pipeline](https://github.com/MrCanon19/novahouse-chatbot-api/workflows/CI%2FCD%20Pipeline/badge.svg)
   ```

---

## 🔄 Manual Trigger

Aby ręcznie uruchomić pipeline:

```bash
# Na GitHub
Actions > CI/CD Pipeline > Run workflow
```

---

## 📋 Checklist

- [ ] Pipeline uruchamia się po push
- [ ] Testy przechodzą (76+ passed)
- [ ] Linting OK
- [ ] Security scan OK (jeśli Trivy dostępne)
- [ ] Deployment skonfigurowany (opcjonalnie)

---

**Wygenerowano:** 4 grudnia 2025  
**Wersja:** 2.5.3
