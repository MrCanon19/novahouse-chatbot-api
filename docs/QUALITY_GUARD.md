# 🛡️ Przewodnik: Ochrona przed błędami

## Automatyczne narzędzia zainstalowane

### 1. Pre-commit Hooks ✅
Automatycznie sprawdza kod **przed każdym commitem**:
- ✅ Formatowanie (black)
- ✅ Sortowanie importów (isort)
- ✅ Usuwanie nieużywanych zmiennych (autoflake)
- ✅ Sprawdzanie składni (flake8)
- ✅ Usuwanie białych znaków na końcach linii
- ✅ Sprawdzanie konfliktów merge

**Instalacja:**
```bash
make setup-hooks
```

### 2. Make Commands 🔧

Nowe komendy w Makefile:

```bash
make fix-all        # Napraw wszystkie problemy automatycznie
make format         # Formatuj kod (black + isort + autoflake)
make lint           # Sprawdź kod (flake8)
make test           # Uruchom testy
make check-all      # Pełne sprawdzenie przed commitem
```

### 3. VS Code - Error Lens ⚙️

Już skonfigurowane w `.vscode/settings.json`:
- Pokazuje tylko **błędy krytyczne**
- Ukrywa ostrzeżenia o długich liniach HTML
- Wyłączone ostrzeżenia lintingu

## Jak to działa?

### Przed commitem:
```bash
git add .
git commit -m "moja zmiana"
# ⬇️ Pre-commit automatycznie:
# 1. Formatuje kod
# 2. Usuwa nieużywane importy
# 3. Sprawdza błędy
# 4. Jeśli znajdzie problemy - naprawia je!
```

### Ręczne sprawdzenie:
```bash
make fix-all    # Napraw wszystko
make test       # Sprawdź czy działa
```

### Jeśli coś się zepsuje:
```bash
make fix-all    # Automatyczna naprawa
make test       # Sprawdź testy
git add .
git commit -m "fix: automatyczne naprawy"
```

## Co się zmieniło?

### ✅ Teraz masz:
1. **Pre-commit hooks** - sprawdzanie przed każdym commitem
2. **Make fix-all** - jeden przycisk naprawia wszystko
3. **Error Lens** - pokazuje tylko ważne błędy
4. **Dokumentacja** - ten plik!

### 🚫 Nie będziesz już miał:
- Niespodzianek z 1000+ błędami lintingu
- Problemów z formatowaniem
- Nieużywanych importów
- Białych znaków na końcach linii
- Bare except bez obsługi błędów

## Przykłady użycia

### Codziennie:
```bash
# Zmiana kodu
vim src/routes/example.py

# Automatyczne naprawy
make fix-all

# Commit (pre-commit sprawdzi automatycznie)
git add .
git commit -m "feat: nowa funkcjonalność"
```

### Przed wysłaniem PR:
```bash
make fix-all    # Napraw formatowanie
make test       # Uruchom testy
make lint       # Sprawdź kod
git push
```

### Szybkie sprawdzenie:
```bash
make format     # Tylko formatowanie
make test       # Tylko testy
```

## Konfiguracja

### Pre-commit (`.pre-commit-config.yaml`)
- Black - formatowanie (line-length 100)
- isort - sortowanie importów
- flake8 - linting
- autoflake - usuwanie nieużywanych importów
- Podstawowe sprawdzenia (trailing whitespace, end of file, etc.)

### VS Code (`.vscode/settings.json`)
- Error Lens: tylko błędy
- Python linting: wyłączony (używamy pre-commit)
- Auto-format on save: włączony

## Troubleshooting

### Pre-commit nie działa?
```bash
pre-commit uninstall
make setup-hooks
```

### Chcę pominąć pre-commit raz?
```bash
git commit -m "message" --no-verify
```

### Sprawdź wszystkie pliki:
```bash
pre-commit run --all-files
```

---

💡 **Porada:** Uruchom `make help` żeby zobaczyć wszystkie dostępne komendy!
