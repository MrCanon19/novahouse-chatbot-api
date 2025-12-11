# 🚀 Quick Start - Szybki przewodnik

## 📍 Aktualna lokalizacja projektu

```bash
cd "/Users/michalmarini/Cursor-pliki/Nova House/chatbot-api"
```

**Uwaga:** Stara ścieżka `/Users/michalmarini/Projects/manus/novahouse-chatbot-api` już nie istnieje!

---

## 💾 Commit i Push - 3 sposoby

### Sposób 1: Skrypt (NAJŁATWIEJSZY) ⭐

```bash
cd "/Users/michalmarini/Cursor-pliki/Nova House/chatbot-api"
./scripts/quick_commit.sh "Aktualizacja kodu"
```

Lub bez wiadomości (użyje domyślnej):
```bash
./scripts/quick_commit.sh
```

### Sposób 2: Komendy ręczne (klasyczne)

```bash
# 1. Przejdź do katalogu
cd "/Users/michalmarini/Cursor-pliki/Nova House/chatbot-api"

# 2. Dodaj wszystkie zmiany
git add .

# 3. Commit z wiadomością
git commit -am "Aktualizacja kodu"

# 4. Push do GitHub
git push
```

### Sposób 3: Jedna linia

```bash
cd "/Users/michalmarini/Cursor-pliki/Nova House/chatbot-api" && git add . && git commit -am "Aktualizacja kodu" && git push
```

---

## 🔑 Konfiguracja GitHub Secrets (dla auto-deploy)

### Krok 1: Utwórz Service Account Key

```bash
# Zaloguj się do GCP
gcloud auth login

# Ustaw projekt
gcloud config set project glass-core-467907-e9

# Utwórz klucz (jeśli service account już istnieje)
gcloud iam service-accounts keys create key.json \
  --iam-account=github-actions@glass-core-467907-e9.iam.gserviceaccount.com
```

**Jeśli service account nie istnieje, utwórz go:**

```bash
# Utwórz service account
gcloud iam service-accounts create github-actions \
  --display-name="GitHub Actions Deployer" \
  --project=glass-core-467907-e9

# Nadaj uprawnienia
gcloud projects add-iam-policy-binding glass-core-467907-e9 \
  --member="serviceAccount:github-actions@glass-core-467907-e9.iam.gserviceaccount.com" \
  --role="roles/appengine.deployer"

gcloud projects add-iam-policy-binding glass-core-467907-e9 \
  --member="serviceAccount:github-actions@glass-core-467907-e9.iam.gserviceaccount.com" \
  --role="roles/storage.admin"

# Utwórz klucz
gcloud iam service-accounts keys create key.json \
  --iam-account=github-actions@glass-core-467907-e9.iam.gserviceaccount.com
```

### Krok 2: Skopiuj zawartość klucza

```bash
# macOS - kopiuje do schowka
cat key.json | pbcopy

# Lub wyświetl zawartość
cat key.json
```

### Krok 3: Dodaj do GitHub Secrets

1. Otwórz: https://github.com/MrCanon19/novahouse-chatbot-api/settings/secrets/actions
2. Kliknij **"New repository secret"**
3. Dodaj pierwszy sekret:
   - **Name:** `GCP_SA_KEY`
   - **Value:** Wklej zawartość `key.json` (Cmd+V)
   - Kliknij **"Add secret"**
4. Dodaj drugi sekret:
   - **Name:** `GCP_PROJECT_ID`
   - **Value:** `glass-core-467907-e9`
   - Kliknij **"Add secret"**

### Krok 4: Usuń lokalny klucz (bezpieczeństwo!)

```bash
rm key.json
```

✅ **Gotowe!** Teraz każdy push na `main` = automatyczny deploy.

---

## 🧪 Test automatycznego deploy

```bash
cd "/Users/michalmarini/Cursor-pliki/Nova House/chatbot-api"

# Pusty commit aby trigger GitHub Actions
git commit --allow-empty -m "test: trigger auto-deploy"
git push origin main
```

Sprawdź w GitHub Actions:
- https://github.com/MrCanon19/novahouse-chatbot-api/actions

---

## 📋 Przegląd TODO/FIXME

**Status:** ✅ Wszystko niekrytyczne, aplikacja działa OK

**Znalezione TODO (3):**
1. `src/routes/chatbot.py:487` - A/B testing tracking (opcjonalne)
2. `src/services/dead_letter_queue.py:131` - Escalate to admin (opcjonalne)
3. `src/services/dead_letter_queue.py:169` - Email escalation (opcjonalne)

**Pełny raport:** `docs/TODO_REVIEW.md`

**Wniosek:** Można zostawić - nie blokują działania aplikacji.

---

## 🎯 Najczęstsze komendy

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

### Pobierz najnowsze zmiany
```bash
git pull
```

### Cofnij ostatni commit (zachowuje zmiany)
```bash
git reset --soft HEAD~1
```

---

## ⚠️ Uwagi

1. **Zawsze sprawdź `git status`** przed commitowaniem
2. **Nie commituj plików z sekretami** (są w `.gitignore`)
3. **Używaj opisowych wiadomości commit** - np. "Fix: Naprawa błędu w chatbot.py"
4. **Stara ścieżka nie działa** - użyj nowej: `/Users/michalmarini/Cursor-pliki/Nova House/chatbot-api`

---

## 🔗 Przydatne linki

- **GitHub Repo:** https://github.com/MrCanon19/novahouse-chatbot-api
- **GitHub Actions:** https://github.com/MrCanon19/novahouse-chatbot-api/actions
- **GCP Console:** https://console.cloud.google.com/?project=glass-core-467907-e9
- **App Engine:** https://console.cloud.google.com/appengine?project=glass-core-467907-e9

---

💡 **Tip:** Stwórz alias w `~/.zshrc`:
```bash
alias gopush='cd "/Users/michalmarini/Cursor-pliki/Nova House/chatbot-api" && ./scripts/quick_commit.sh'
```

Wtedy wystarczy: `gopush "Twoja wiadomość"`

