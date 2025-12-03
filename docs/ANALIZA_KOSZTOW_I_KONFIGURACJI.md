# 📊 Analiza Kosztów i Konfiguracji Projektu

**Data analizy:** 3 grudnia 2025  
**Projekt:** novahouse-chatbot-api  
**Google Cloud Project ID:** glass-core-467907-e9

---

## 🔍 ODPOWIEDZI NA PYTANIA

### 1. Czy korzystasz z Gemini i jakiego API?

**NIE** - projekt **NIE KORZYSTA** z Gemini API w produkcji.

**Dowody:**
- W `app.yaml` (plik konfiguracyjny produkcji) **BRAK** zmiennej `GEMINI_API_KEY`
- Kod korzysta **wyłącznie z OpenAI GPT-4o-mini** (`src/services/message_handler.py` linia 230-340)
- Gemini jest wymieniony tylko w dokumentacji jako "opcjonalny" (`GEMINI_API_KEY=` w `.env.example`)
- **Koszt Gemini API w listopadzie: 0,48 zł** - prawdopodobnie z testów lub przypadkowych wywołań

**Wniosek:** Gemini API nie jest używany aktywnie, koszt 0,48 zł to śladowe użycie (prawdopodobnie testy).

---

### 2. Skąd takie koszty i kiedy?

**Rozliczenie listopad 2025: 53,73 zł**

| Usługa | Koszt | Przyczyna |
|--------|-------|-----------|
| **App Engine** | 27,28 zł | Główny koszt - hosting aplikacji Flask |
| **Cloud SQL (PostgreSQL)** | 18,84 zł | Baza danych - działa **24/7** nawet gdy nie używasz |
| **Compute Engine** | 5,83 zł | Instancje VM (prawdopodobnie dla testów) |
| **Artifact Registry** | 1,30 zł | Przechowywanie obrazów Docker |
| **Gemini API** | 0,48 zł | Śladowe użycie (testy?) |

**Grudzień 2025 (od 1-3 grudnia): 1,51 zł**

| Usługa | Koszt | Przyczyna |
|--------|-------|-----------|
| **Cloud SQL (instancja)** | 0,96 zł | Baza działa non-stop |
| **Balanced PD Capacity** | 0,31 zł | Dysk dla bazy danych (Warszawa) |
| **Cloud SQL (storage)** | 0,21 zł | Przechowywanie danych |
| **Storage PD Snapshot** | 0,03 zł | Snapshoty backupów |

---

### 3. Główne przyczyny kosztów:

#### ✅ **Cloud SQL (PostgreSQL) - Największy winowajca**
- **Problem:** Baza danych działa **24/7** nawet gdy nie pracujesz nad projektem
- **Koszty:** ~19 zł/miesiąc (36% całego rachunku)
- **Rozwiązanie:**
  - Zatrzymaj bazę gdy nie używasz: `gcloud sql instances patch novahouse-chatbot-db --activation-policy=NEVER`
  - Uruchom gdy potrzeba: `gcloud sql instances patch novahouse-chatbot-db --activation-policy=ALWAYS`
  - **LUB** przełącz się na SQLite dla testów lokalnych (darmowe)

#### ✅ **App Engine - Hosting aplikacji**
- **Problem:** Aplikacja działa non-stop z minimum 0 instancji (cold start OK), ale może się autostart
- **Koszty:** ~27 zł/miesiąc (50% rachunku)
- **Konfiguracja w `app.yaml`:**
  ```yaml
  automatic_scaling:
    min_instances: 0  # OK - nie płacisz za bezczynność
    max_instances: 10
    min_idle_instances: 0  # OK - cold start dozwolony
  ```
- **Rozwiązanie:** To jest OK, App Engine płacisz za użycie. Koszt 27 zł = normalny ruch.

#### ✅ **Compute Engine - Instancje VM**
- **Problem:** Masz uruchomioną instancję VM (5,83 zł)
- **Rozwiązanie:** Sprawdź czy nie zapomniałeś o uruchomionych testowych maszynach:
  ```bash
  gcloud compute instances list
  gcloud compute instances delete NAZWA_INSTANCJI
  ```

---

### 4. Przegląd logiki i problemów

#### 🔍 **Problem z galerią zdjęć (od Ady)**

**ZNALEZIONO PROBLEM:**
- Aplikacja ma moduł upload zdjęć (`src/routes/file_upload.py`, `src/services/file_upload_service.py`)
- **BRAK** konfiguracji Google Cloud Storage w `app.yaml`!
- Zdjęcia prawdopodobnie zapisują się lokalnie do `/tmp/uploads`, który **jest czyszczony po restarcie** App Engine
- **To dlatego zdjęcia znikają!**

**Rozwiązanie:**
1. Włącz Google Cloud Storage w `app.yaml`:
   ```yaml
   env_variables:
     USE_CLOUD_STORAGE: "true"
     GCS_BUCKET_NAME: "novahouse-uploads"
   ```
2. Utwórz bucket GCS:
   ```bash
   gsutil mb -l europe-west1 gs://novahouse-uploads
   gsutil iam ch allUsers:objectViewer gs://novahouse-uploads
   ```
3. Upload będzie działać trwale.

---

### 5. Sprawdzenie kluczy API

**KLUCZE API W UŻYCIU (app.yaml):**

| Klucz API | Status | Koszt | Użycie |
|-----------|--------|-------|--------|
| **OPENAI_API_KEY** | ✅ Aktywny | Płatne | GPT-4o-mini dla chatbota |
| **MONDAY_API_KEY** | ✅ Aktywny | Darmowe | Integracja CRM |
| **MONDAY_BOARD_ID** | ✅ Aktywny | - | ID tablicy Monday.com |
| **SECRET_KEY** | ✅ Aktywny | - | Bezpieczeństwo Flask |
| **API_KEY** | ✅ Aktywny | - | Admin dashboard/backup |
| **DATABASE_URL** | ✅ Aktywny | **18,84 zł/mc** | PostgreSQL |
| **SENTRY_DSN** | ❌ Zakomentowany | - | Monitoring błędów (nieaktywny) |

**KLUCZE API BRAKUJĄCE (ale kod ich używa):**

| Klucz API | Status | Potrzebne? |
|-----------|--------|------------|
| **ZENCAL_API_KEY** | ❌ BRAK | TAK - dla rezerwacji |
| **ZENCAL_WORKSPACE_ID** | ❌ BRAK | TAK - dla rezerwacji |
| **GEMINI_API_KEY** | ❌ BRAK | NIE - opcjonalne |
| **REDIS_URL** | ❌ BRAK | NIE - fallback na in-memory |
| **TWILIO (SMS)** | ❌ BRAK | NIE - opcjonalne |
| **GCS_BUCKET_NAME** | ❌ BRAK | TAK - dla upload zdjęć! |

---

### 6. Czemu masz tyle kalendarzy do wyboru?

**ZNALEZIONO PRZYCZYNĘ:**

Aplikacja ma integracje z **TRZEMA** systemami kalendarzy:

1. **Zencal** (`src/integrations/zencal_client.py`)
   - Status: ❌ NIE SKONFIGUROWANY (brak API key)
   - Funkcja: Rezerwacje online
   - Problem: Kod wywołuje Zencal, ale klucz API nie jest ustawiony → błędy

2. **Booksy** (wspomniane w swagger.yaml)
   - Status: ❌ NIE SKONFIGUROWANY (brak w app.yaml)
   - Funkcja: Booksy calendar integration
   - Problem: Kod może próbować wyświetlić opcje Booksy

3. **Google Calendar** (dokumentacja)
   - Status: ❌ NIE ZAIMPLEMENTOWANY (Phase 5 - Skipped)
   - Funkcja: Synchronizacja kalendarza
   - Problem: W dokumentacji, ale nie w kodzie

**Rozwiązanie:**
- **USUŃ** nieużywane integracje kalendarzy z kodu
- **LUB** skonfiguruj **tylko Zencal** (jeśli używasz):
  ```bash
  # W Google Cloud Console > Secret Manager
  gcloud secrets create ZENCAL_API_KEY --data-file=-
  # Wklej klucz Zencal
  ```
- Dodaj do `app.yaml`:
  ```yaml
  env_variables:
    ZENCAL_API_KEY: "twoj-klucz-zencal"
    ZENCAL_WORKSPACE_ID: "twoj-workspace-id"
  ```

---

## 🛠️ REKOMENDACJE NAPRAWY

### 1. **ZATRZYMAJ Cloud SQL gdy nie używasz (oszczędzisz 18 zł/mc):**
```bash
gcloud sql instances patch novahouse-chatbot-db --activation-policy=NEVER
```

### 2. **USUŃ nieużywane instancje VM:**
```bash
gcloud compute instances list
gcloud compute instances delete NAZWA_INSTANCJI
```

### 3. **NAPRAW upload zdjęć (problem Ady):**
```bash
# Utwórz bucket GCS
gsutil mb -l europe-west1 gs://novahouse-uploads
gsutil iam ch allUsers:objectViewer gs://novahouse-uploads
```
Dodaj do `app.yaml`:
```yaml
env_variables:
  USE_CLOUD_STORAGE: "true"
  GCS_BUCKET_NAME: "novahouse-uploads"
```

### 4. **WYCZYŚĆ nieużywane integracje kalendarzy:**
- Usuń kod Zencal jeśli nie używasz
- Usuń kod Booksy jeśli nie używasz
- Wybierz **JEDEN** system kalendarzy i skonfiguruj go

### 5. **WŁĄCZ Sentry dla monitoringu błędów:**
```yaml
env_variables:
  SENTRY_DSN: "https://xxxxx@xxxxx.ingest.sentry.io/xxxxx"
```

---

## 💰 PROGNOZA KOSZTÓW

**Po optymalizacji (zatrzymanie Cloud SQL gdy nie używasz):**
- App Engine: ~27 zł/mc (normalny ruch)
- Cloud SQL: **0 zł** (gdy zatrzymany)
- Compute Engine: **0 zł** (po usunięciu VM)
- Reszta: ~2 zł/mc (storage, registry)

**Szacunkowy koszt po optymalizacji: ~29 zł/mc** (zamiast 53 zł)  
**Oszczędność: ~24 zł/mc (45%)**

---

## ✅ PODSUMOWANIE

1. **NIE używasz Gemini API** - koszt 0,48 zł to testy/przypadkowe wywołania
2. **Główny koszt:** Cloud SQL (19 zł) + App Engine (27 zł) = 86% rachunku
3. **Problem z galerią:** Brak Cloud Storage - zdjęcia znikają po restarcie
4. **Problem z kalendarzami:** 3 nieużywane/nieskonfigurowane systemy kalendarzy
5. **Brakujące klucze API:** Zencal, GCS bucket (dla zdjęć)

**Akcja:**
- Zatrzymaj Cloud SQL gdy nie używasz → oszczędzisz 18 zł/mc
- Skonfiguruj Cloud Storage → napraw galerię zdjęć
- Usuń nieużywane kalendarze → wyczyść kod
- Usuń instancje VM → oszczędzisz 6 zł/mc
