# 📚 Instrukcja Git - Quick Reference

## 🚀 Szybki Commit i Push

### Opcja 1: Użyj skryptu (NAJŁATWIEJSZE)

```bash
cd "/Users/michalmarini/Cursor-pliki/Nova House/chatbot-api"
./scripts/quick_commit.sh "Twoja wiadomość commit"
```

Lub bez wiadomości (użyje domyślnej):
```bash
./scripts/quick_commit.sh
```

### Opcja 2: Komendy ręczne

```bash
# 1. Przejdź do katalogu projektu
cd "/Users/michalmarini/Cursor-pliki/Nova House/chatbot-api"

# 2. Sprawdź status (opcjonalnie)
git status

# 3. Dodaj wszystkie zmiany
git add .

# 4. Commit z wiadomością
git commit -am "Aktualizacja kodu"

# 5. Push do GitHub
git push
```

## 📋 Co robią te komendy?

### `git add .`
- Dodaje **wszystkie** zmienione pliki do staging area
- Przygotowuje je do commitowania
- ⚠️ Uwaga: dodaje też pliki z `.gitignore` jeśli są zmienione

### `git commit -am "wiadomość"`
- `-a` = automatycznie dodaje zmienione pliki (ale nie nowe!)
- `-m` = wiadomość commit
- Tworzy snapshot zmian w historii Git

### `git push`
- Wysyła commity do zdalnego repo (GitHub)
- Aktualizuje branch `main` na GitHub

## 🔍 Przydatne komendy

### Sprawdź status
```bash
git status
```

### Zobacz co się zmieniło
```bash
git diff
```

### Zobacz historię
```bash
git log --oneline -10
```

### Sprawdź remote (GitHub)
```bash
git remote -v
```

### Pobierz najnowsze zmiany (bez merge)
```bash
git fetch
```

### Pobierz i zmerguj zmiany
```bash
git pull
```

## ⚠️ Uwagi

1. **Zawsze sprawdź `git status`** przed commitowaniem
2. **Nie commituj plików z sekretami** (są w `.gitignore`)
3. **Używaj opisowych wiadomości commit** - np. "Fix: Naprawa błędu w chatbot.py"
4. **Jeśli coś poszło nie tak**: `git reset --soft HEAD~1` (cofa commit, zachowuje zmiany)

## 🎯 Najlepsze praktyki

### Dobre wiadomości commit:
- ✅ `"Fix: Naprawa błędu w rate limiter"`
- ✅ `"Feature: Dodanie nowego endpointu /api/health"`
- ✅ `"Refactor: Optymalizacja importów w main.py"`
- ✅ `"Docs: Aktualizacja README"`

### Złe wiadomości commit:
- ❌ `"zmiany"`
- ❌ `"fix"`
- ❌ `"update"`
- ❌ `"asdf"`

## 🔗 Aktualna lokalizacja projektu

```
/Users/michalmarini/Cursor-pliki/Nova House/chatbot-api
```

**GitHub repo:** `https://github.com/MrCanon19/novahouse-chatbot-api.git`

---

💡 **Tip:** Stwórz alias w `~/.zshrc`:
```bash
alias gopush='cd "/Users/michalmarini/Cursor-pliki/Nova House/chatbot-api" && ./scripts/quick_commit.sh'
```

Wtedy wystarczy: `gopush "Twoja wiadomość"`

