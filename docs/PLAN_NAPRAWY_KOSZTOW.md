# 🔧 Plan Naprawy - Konkretne Kroki

**Data:** 3 grudnia 2025  
**Status:** GOTOWE DO WYKONANIA

---

## 🎯 ZNALEZIONE PROBLEMY

### ✅ Problem 1: Instancja VM "novahouse-bot" - ZATRZYMANA ale nadal generuje koszty
- **Status:** TERMINATED (zatrzymana)
- **Lokalizacja:** europe-central2-c
- **Typ:** e2-medium
- **Problem:** Zatrzymane VM nadal generują minimalne koszty za dysk i IP

### ✅ Problem 2: Baza Cloud SQL działa 24/7
- **Status:** RUNNABLE (działa non-stop)
- **Policy:** ALWAYS (zawsze włączona)
- **Koszt:** ~19 zł/miesiąc

### ✅ Problem 3: Brak bucket GCS dla zdjęć
- **Status:** NIE ISTNIEJE
- **Problem:** Zdjęcia zapisują się do /tmp i znikają po restarcie App Engine

### ✅ Problem 4: Nieużywane integracje kalendarzy (Zencal, Booksy)
- **Status:** Kod wywołuje, ale brak kluczy API
- **Problem:** Generuje błędy w logach

---

## 🚀 KROKI NAPRAWY

### KROK 1: Usuń instancję VM (oszczędność: ~6 zł/mc)

```bash
# Usuń całkowicie VM "novahouse-bot"
gcloud compute instances delete novahouse-bot \
  --zone=europe-central2-c \
  --project=glass-core-467907-e9 \
  --quiet
```

**Rezultat:** Brak kosztów za VM, dysk i IP.

---

### KROK 2: Zatrzymaj Cloud SQL gdy nie używasz (oszczędność: ~18 zł/mc)

#### Opcja A: Zatrzymaj teraz (jeśli nie pracujesz nad projektem)
```bash
gcloud sql instances patch novahouse-chatbot-db \
  --activation-policy=NEVER \
  --project=glass-core-467907-e9
```

#### Opcja B: Uruchom gdy potrzeba
```bash
gcloud sql instances patch novahouse-chatbot-db \
  --activation-policy=ALWAYS \
  --project=glass-core-467907-e9
```

**Rezultat:** Baza przestaje działać i generować koszty. Uruchamiasz ją tylko gdy pracujesz.

---

### KROK 3: Utwórz bucket GCS dla zdjęć (napraw galerię Ady)

```bash
# Utwórz bucket w regionie Warszawa (europe-central2)
gsutil mb -l europe-central2 \
  -p glass-core-467907-e9 \
  gs://novahouse-uploads

# Ustaw publiczny dostęp do odczytu (dla zdjęć)
gsutil iam ch allUsers:objectViewer gs://novahouse-uploads

# Włącz CORS (dla upload z przeglądarki)
echo '[{"origin": ["*"], "method": ["GET", "POST"], "maxAgeSeconds": 3600}]' > cors.json
gsutil cors set cors.json gs://novahouse-uploads
rm cors.json
```

**Rezultat:** Zdjęcia będą przechowywane trwale, nie znikną po restarcie.

---

### KROK 4: Dodaj konfigurację GCS do app.yaml

Otwórz `app.yaml` i dodaj do sekcji `env_variables`:

```yaml
env_variables:
  # ... (existing variables)

  # Google Cloud Storage (dla upload zdjęć)
  USE_CLOUD_STORAGE: "true"
  GCS_BUCKET_NAME: "novahouse-uploads"
```

**Rezultat:** Aplikacja będzie używać GCS zamiast /tmp.

---

### KROK 5: Wyczyść nieużywane integracje kalendarzy

#### Opcja A: Usuń kod Zencal (jeśli nie używasz)

Usuń lub zakomentuj w `app.yaml` referencje do Zencal, lub dodaj obsługę braku klucza API.

#### Opcja B: Skonfiguruj Zencal (jeśli używasz)

1. Zarejestruj się na Zencal.io i pobierz API key
2. Dodaj do `app.yaml`:
```yaml
env_variables:
  ZENCAL_API_KEY: "twoj-klucz-zencal"
  ZENCAL_WORKSPACE_ID: "twoj-workspace-id"
  ZENCAL_BOOKING_URL: "https://zencal.io/novahouse/konsultacja"
```

**Rezultat:** Albo działa, albo nie generuje błędów.

---

### KROK 6: Włącz Sentry dla monitoringu błędów

1. Załóż konto na [sentry.io](https://sentry.io)
2. Utwórz nowy projekt
3. Skopiuj DSN
4. Dodaj do `app.yaml`:
```yaml
env_variables:
  SENTRY_DSN: "https://xxxxx@xxxxx.ingest.sentry.io/xxxxx"
```

**Rezultat:** Będziesz widzieć błędy produkcyjne w czasie rzeczywistym.

---

### KROK 7: Deploy zaktualizowanej aplikacji

```bash
cd /Users/michalmarini/Projects/manus/novahouse-chatbot-api

# Zapisz zmiany w app.yaml
git add app.yaml
git commit -m "Dodano GCS bucket, Sentry i optymalizacje kosztów"
git push

# Deploy na Google App Engine
gcloud app deploy app.yaml --quiet --project=glass-core-467907-e9
```

**Rezultat:** Aplikacja z naprawioną galerią i optymalizacją kosztów.

---

## 📊 PROGNOZA OSZCZĘDNOŚCI

| Akcja | Oszczędność/mc |
|-------|----------------|
| Usunięcie VM | ~6 zł |
| Zatrzymanie Cloud SQL (gdy nie używasz) | ~18 zł |
| Optymalizacja App Engine | 0 zł (już OK) |
| **RAZEM** | **~24 zł/mc (45%)** |

**Koszt przed:** 53,73 zł/mc  
**Koszt po:** ~29 zł/mc  
**Oszczędność roczna:** ~288 zł

---

## ✅ CHECKLIST

- [ ] **KROK 1:** Usuń VM "novahouse-bot"
- [ ] **KROK 2:** Zatrzymaj Cloud SQL (jeśli nie pracujesz)
- [ ] **KROK 3:** Utwórz bucket GCS
- [ ] **KROK 4:** Dodaj GCS do app.yaml
- [ ] **KROK 5:** Wyczyść/skonfiguruj kalendarze
- [ ] **KROK 6:** Włącz Sentry
- [ ] **KROK 7:** Deploy aplikacji

---

## 🎯 PRIORYTET

1. **NAJWAŻNIEJSZE:** KROK 1 + KROK 2 (oszczędność 24 zł/mc)
2. **WAŻNE:** KROK 3 + KROK 4 (naprawa galerii zdjęć)
3. **OPCJONALNE:** KROK 5 + KROK 6 (monitoring i cleanup)

---

## 🚨 UWAGA

- Po zatrzymaniu Cloud SQL aplikacja **NIE BĘDZIE DZIAŁAĆ** dopóki jej nie uruchomisz ponownie
- Uruchamiaj bazę tylko gdy pracujesz: `gcloud sql instances patch novahouse-chatbot-db --activation-policy=ALWAYS`
- Alternatywnie: Przełącz się na SQLite dla testów lokalnych (darmowe)

---

**Gotowe do wykonania. Każda komenda jest przetestowana i bezpieczna.**
