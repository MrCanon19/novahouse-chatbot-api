# 🔒 BEZPIECZEŃSTWO SEKRETÓW - OCHRONA KLUCZY API

**Data:** 12 grudnia 2025  
**Status:** ✅ **ZABEZPIECZONE**

---

## ✅ CO ZOSTAŁO NAPRAWIONE

1. **Usunięto pliki z kluczami API z Git**
   - `app.yaml.deploy.*` - pliki tymczasowe deploy
   - Dodano do `.gitignore`

2. **Zabezpieczono logowanie**
   - Nigdy nie logujemy pełnego klucza API
   - Tylko pierwsze 4 znaki dla debugowania
   - Wszystkie `print()` zastąpione przez `logging`

3. **Dodano narzędzia bezpieczeństwa**
   - `scripts/check_secrets_security.py` - skaner sekretów
   - `scripts/pre_commit_security_check.sh` - pre-commit hook
   - `.gitattributes` - dodatkowa ochrona

4. **Zaktualizowano `.gitignore`**
   - `app.yaml.deploy*` - pliki tymczasowe deploy
   - Wszystkie pliki z sekretami są ignorowane

---

## 🔒 ZASADY BEZPIECZEŃSTWA

### 1. NIGDY nie commituj kluczy API do Git

**Zabronione:**
```python
# ❌ NIGDY TAK!
OPENAI_API_KEY = "sk-proj-..."
```

**Dozwolone:**
```python
# ✅ TAK!
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

---

### 2. NIGDY nie loguj pełnego klucza API

**Zabronione:**
```python
# ❌ NIGDY TAK!
logging.info(f"API key: {api_key}")
print(f"Key: {api_key}")
```

**Dozwolone:**
```python
# ✅ TAK!
key_preview = api_key[:4] + "..." if api_key else "None"
logging.info(f"API key starts with: {key_preview}")
```

---

### 3. Używaj zmiennych środowiskowych

**Lokalnie:**
```bash
export OPENAI_API_KEY='sk-...'
```

**W produkcji:**
- GCP Secret Manager (zalecane)
- `app.yaml.secret` (tylko lokalnie, NIE commitować!)

---

## 🛡️ NARZĘDZIA BEZPIECZEŃSTWA

### 1. Skaner sekretów

```bash
python scripts/check_secrets_security.py
```

Sprawdza cały kod pod kątem potencjalnych sekretów.

---

### 2. Pre-commit hook

```bash
# Zainstaluj hook
ln -s ../../scripts/pre_commit_security_check.sh .git/hooks/pre-commit
```

Automatycznie blokuje commit jeśli wykryje sekrety.

---

### 3. Sprawdzanie przed wdrożeniem

```bash
./scripts/check_deployment_ready.sh
```

Sprawdza gotowość i bezpieczeństwo przed wdrożeniem.

---

## 📋 CHECKLISTA BEZPIECZEŃSTWA

Przed każdym commitem:

- [ ] Sprawdź czy nie commitujesz plików z sekretami
- [ ] Uruchom `check_secrets_security.py`
- [ ] Sprawdź czy `.gitignore` zawiera wszystkie pliki z sekretami
- [ ] Upewnij się, że klucze API są tylko w zmiennych środowiskowych

Przed wdrożeniem:

- [ ] Sprawdź czy `app.yaml.secret` jest w `.gitignore`
- [ ] Upewnij się, że klucze są w GCP Secret Manager (produkcja)
- [ ] Sprawdź logi - nie powinny zawierać pełnych kluczy

---

## 🚨 CO ZROBIĆ, GDY KLUCZ ZOSTAŁ UJAWNIONY

1. **Natychmiast wygeneruj nowy klucz** w https://platform.openai.com/api-keys
2. **Usuń stary klucz** z systemu
3. **Zaktualizuj klucz** we wszystkich miejscach:
   - GCP Secret Manager
   - `app.yaml.secret` (lokalnie)
   - Zmienne środowiskowe
4. **Sprawdź logi** - czy stary klucz nie został zalogowany
5. **Przeszukaj Git** - czy stary klucz nie jest w historii:
   ```bash
   git log -p | grep "sk-proj-..."
   ```

---

## 📁 PLIKI Z SEKRETAMI (NIE COMMITOWAĆ!)

- `app.yaml.secret` ✅ w `.gitignore`
- `app.yaml.deploy*` ✅ w `.gitignore`
- `.env` ✅ w `.gitignore`
- `*.secret.yaml` ✅ w `.gitignore`
- `config/app.yaml` ✅ w `.gitignore`

---

## ✅ WERYFIKACJA

Sprawdź czy wszystko jest bezpieczne:

```bash
# 1. Sprawdź czy pliki z sekretami są ignorowane
git check-ignore app.yaml.secret app.yaml.deploy

# 2. Skanuj kod pod kątem sekretów
python scripts/check_secrets_security.py

# 3. Sprawdź logi - nie powinny zawierać pełnych kluczy
grep -r "sk-proj-" logs/ 2>/dev/null || echo "✅ Brak kluczy w logach"
```

---

**Data utworzenia:** 12 grudnia 2025  
**Status:** ✅ Wszystkie sekrety są bezpiecznie chronione

