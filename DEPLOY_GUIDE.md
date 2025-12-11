# 🚀 Przewodnik Deploy - Kiedy używać jakiej metody

## 📋 Twoje komendy

### 1. Commit i Push ✅

```bash
cd "/Users/michalmarini/Cursor-pliki/Nova House/chatbot-api"
./scripts/quick_commit_no_hooks.sh "Aktualizacja kodu"
```

**To jest poprawne!** ✅

---

## 🚀 Deploy - Masz 2 opcje

### OPCJA A: Automatyczny Deploy (ZALECANE) ⭐

**Jak działa:**
1. Robisz commit i push (jak wyżej)
2. GitHub Actions automatycznie deployuje na GCP App Engine
3. **Nie musisz nic robić ręcznie!**

**Kiedy używać:**
- ✅ **Zawsze** - to jest domyślna metoda
- ✅ Normalne zmiany w kodzie
- ✅ Chcesz mieć historię deploy w GitHub Actions

**Sprawdź status:**
- https://github.com/MrCanon19/novahouse-chatbot-api/actions

**Wymagania:**
- GitHub Secrets skonfigurowane (`GCP_SA_KEY`, `GCP_PROJECT_ID`)
- Jeśli nie masz → użyj ręcznego deploy (patrz niżej)

---

### OPCJA B: Ręczny Deploy (tylko gdy potrzebujesz)

```bash
cd "/Users/michalmarini/Cursor-pliki/Nova House/chatbot-api"
gcloud app deploy app.yaml --quiet --project=glass-core-467907-e9
```

**Kiedy używać:**
- ⚠️ GitHub Secrets nie są skonfigurowane
- ⚠️ Potrzebujesz szybkiego deploy bez commitowania
- ⚠️ Testujesz lokalnie przed push
- ⚠️ Hotfix - pilna naprawa bez czekania na CI/CD

**Uwaga:** Ręczny deploy **nie** aktualizuje historii w GitHub Actions.

---

## 📊 Porównanie metod

| Metoda | Szybkość | Historia | Automatyzacja | Rekomendacja |
|--------|----------|----------|---------------|--------------|
| **Automatyczny (CI/CD)** | ⚡ Średnia | ✅ Pełna | ✅ Tak | ⭐ **ZALECANE** |
| **Ręczny (gcloud)** | ⚡⚡ Szybka | ❌ Brak | ❌ Nie | ⚠️ Tylko gdy potrzeba |

---

## 🎯 Standardowy workflow (ZALECANY)

```bash
# 1. Commit i push
cd "/Users/michalmarini/Cursor-pliki/Nova House/chatbot-api"
./scripts/quick_commit_no_hooks.sh "Aktualizacja kodu"

# 2. Sprawdź GitHub Actions (automatyczny deploy)
# https://github.com/MrCanon19/novahouse-chatbot-api/actions

# 3. Gotowe! ✅
```

**To wszystko!** Deploy się wykona automatycznie.

---

## 🔧 Konfiguracja automatycznego deploy

Jeśli automatyczny deploy nie działa, skonfiguruj GitHub Secrets:

### Krok 1: Utwórz Service Account Key

```bash
gcloud iam service-accounts keys create key.json \
  --iam-account=github-actions@glass-core-467907-e9.iam.gserviceaccount.com
```

### Krok 2: Skopiuj zawartość

```bash
cat key.json | pbcopy
```

### Krok 3: Dodaj do GitHub Secrets

1. Otwórz: https://github.com/MrCanon19/novahouse-chatbot-api/settings/secrets/actions
2. Kliknij **"New repository secret"**
3. Dodaj:
   - **Name:** `GCP_SA_KEY`, **Value:** (wklej JSON)
   - **Name:** `GCP_PROJECT_ID`, **Value:** `glass-core-467907-e9`

### Krok 4: Usuń lokalny klucz

```bash
rm key.json
```

✅ **Gotowe!** Teraz każdy push = automatyczny deploy.

---

## 📋 Podsumowanie

### ✅ Twoje komendy są poprawne:

**Commit:**
```bash
cd "/Users/michalmarini/Cursor-pliki/Nova House/chatbot-api"
./scripts/quick_commit_no_hooks.sh "Aktualizacja kodu"
```

**Deploy:**
- **Automatyczny:** Po push (domyślnie) ⭐
- **Ręczny:** `gcloud app deploy app.yaml --quiet --project=glass-core-467907-e9` (tylko gdy potrzeba)

---

## 💡 Rekomendacja

**Używaj automatycznego deploy:**
1. Commit i push (jak zawsze)
2. GitHub Actions automatycznie deployuje
3. Sprawdź status w GitHub Actions

**Ręczny deploy tylko gdy:**
- GitHub Secrets nie są skonfigurowane
- Pilny hotfix bez commitowania
- Testowanie lokalnie

---

## 🔗 Przydatne linki

- **GitHub Actions:** https://github.com/MrCanon19/novahouse-chatbot-api/actions
- **GCP Console:** https://console.cloud.google.com/appengine?project=glass-core-467907-e9
- **App URL:** https://glass-core-467907-e9.ey.r.appspot.com

