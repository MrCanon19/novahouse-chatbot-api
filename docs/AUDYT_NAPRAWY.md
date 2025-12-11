# 🚨 AUDYT BEZPIECZEŃSTWA I OPTYMALIZACJI - RAPORT NAPRAW

**Data audytu:** 3 grudnia 2025  
**Inspektor:** Senior DevOps Engineer (40 lat doświadczenia)  
**Projekt:** chatbot-api  

---

## 🔴 KRYTYCZNE PROBLEMY (NATYCHMIASTOWA NAPRAWA!)

### 1. ❌ **KATASTROFA BEZPIECZEŃSTWA: Secrets w Git**

**Problem:** Plik `app.yaml` zawiera WSZYSTKIE production secrets i jest commitowany do Git!

**Znalezione exposed credentials:**
- ✅ `SECRET_KEY` - Flask session key (exposed w Git!)
- ✅ `API_KEY` - Admin API key dla backupów (exposed w Git!)
- ✅ `DATABASE_URL` - PostgreSQL password `vicNRNoO3TpLZzQ_BkAVbz886dW_J0Yo` (exposed w Git!)
- ✅ `OPENAI_API_KEY` - OpenAI API key (exposed w Git!)
- ✅ `MONDAY_API_KEY` - Monday.com JWT token (exposed w Git!)

**Ryzyko:**
- Każdy z dostępem do repozytorium ma FULL ACCESS do bazy danych
- Może wykraść wszystkie dane klientów (RODO violation!)
- Może wygenerować nieograniczone koszty OpenAI API
- Może manipulować Monday.com CRM

**Naprawa:**
1. ✅ Natychmiast zmienić WSZYSTKIE hasła i klucze API
2. ✅ Usunąć secrets z `app.yaml`
3. ✅ Użyć Google Secret Manager
4. ✅ Dodać `app.yaml` do `.gitignore`
5. ✅ Usunąć secrets z historii Git (git filter-repo)

**Koszt naprawy:** 2-4 godziny  
**Priorytet:** 🔴 KRYTYCZNY - NATYCHMIAST!

---

### 2. ⚠️ **Cloud SQL działa 24/7 bez potrzeby**

**Problem:** Cloud SQL z `activation_policy: ALWAYS` kosztuje 18 zł/mc nawet gdy nikt nie używa chatbota.

**Obecna konfiguracja:**
- Tier: `db-f1-micro` (najtańszy, OK)
- Pricing: `PER_USE` (płacisz za czas działania)
- Backups: Enabled (OK, ale zajmują miejsce)
- Activation: `ALWAYS` (zły wybór!)

**Optymalizacja:**
- Nie można użyć `ON_DEMAND` dla PostgreSQL (tylko MySQL)
- Alternatywa: Użyć **Cloud Run** zamiast App Engine (płacisz tylko za requesty)
- Lub: Zatrzymywać Cloud SQL ręcznie gdy nie używasz (cron job?)

**Koszt obecny:** ~18 zł/mc  
**Możliwa oszczędność:** Do 15 zł/mc (jeśli używasz 10 dni/mc)  
**Priorytet:** 🟡 ŚREDNI

---

### 3. ⚠️ **Niepotrzebne GCP API włączone (potencjalne koszty)**

**Znalezione włączone API:**
- `analyticshub.googleapis.com` - NIE UŻYWASZ
- `backupdr.googleapis.com` - NIE UŻYWASZ (masz własne backupy)
- `cloudasset.googleapis.com` - NIE UŻYWASZ
- `dataform.googleapis.com` - NIE UŻYWASZ
- `dataplex.googleapis.com` - NIE UŻYWASZ
- `datastore.googleapis.com` - NIE UŻYWASZ (masz PostgreSQL)
- `osconfig.googleapis.com` - NIE UŻYWASZ (nie masz VM)
- `oslogin.googleapis.com` - NIE UŻYWASZ

**Ryzyko:** Każde API może generować nieoczekiwane koszty przy akty API

**Naprawa:** Wyłączyć wszystkie nieużywane API

**Koszt obecny:** 0 zł (ale potencjalne ryzyko)  
**Priorytet:** 🟡 ŚREDNI

---

### 4. ⚠️ **Staging bucket zajmuje 63 MB niepotrzebnie**

**Problem:** Bucket `gs://staging.glass-core-467907-e9.appspot.com/` zawiera 63 MB danych.

**Obecne buckety:**
- `gs://glass-core-467907-e9-chatbot-backups/` - 77 KB (OK, backupy)
- `gs://glass-core-467907-e9.appspot.com/` - 0 MB (pusty, OK)
- `gs://staging.glass-core-467907-e9.appspot.com/` - **63 MB** (niepotrzebne!)

**Koszt:** ~0.10 zł/mc (mało, ale po co?)

**Naprawa:** Wyczyścić staging bucket

**Priorytet:** 🟢 NISKI

---

## 🟡 PROBLEMY ŚREDNIE (Optymalizacja)

### 5. ⚠️ **Dead code i TODO w produkcji**

**Znalezione TODOs:**
- `src/services/session_timeout.py:60` - TODO: Track in database
- `src/services/lead_scoring_ml.py:343` - TODO: check competitive_intel table
- `src/services/lead_scoring_ml.py:355` - TODO: Add negative examples
- `src/services/message_handler.py:104` - TODO: calculate duration

**Problem:** Niezaimplementowane features mogą powodować błędy

**Naprawa:** Zaimplementować lub usunąć TODOs

**Priorytet:** 🟡 ŚREDNI

---

### 6. ⚠️ **Zencal API niekonfigurowany (generuje logi błędów)**

**Problem:** Kod sprawdza `ZENCAL_API_KEY` ale nie jest skonfigurowany, generuje warning logi.

**Znalezione:**
- 20+ referencji do `ZENCAL_API_KEY` w `src/integrations/zencal_client.py`
- Każde wywołanie generuje log: "ALERT: ZENCAL_API_KEY not configured"

**Naprawa:**
- Skonfigurować Zencal API
- LUB usunąć Zencal z kodu (jeśli nie używasz)

**Priorytet:** 🟡 ŚREDNI

---

### 7. ⚠️ **Brak Sentry monitoring**

**Problem:** `SENTRY_DSN` zakomentowane - nie widzisz błędów produkcyjnych!

**Konsekwencje:**
- Nie wiesz kiedy chatbot nie działa
- Nie widzisz błędów 500
- Tracisz leadów przez niewidoczne błędy

**Naprawa:** Włączyć Sentry (14-dniowy free trial, potem ~$26/mc dla małego projektu)

**Priorytet:** 🟡 ŚREDNI

---

### 8. ⚠️ **F2 instance - możliwa optymalizacja**

**Problem:** F2 instance ma 512 MB RAM, możliwe że za dużo dla prostego chatbota.

**Obecna config:**
- Instance: F2 (512 MB RAM, 1.2 GHz CPU)
- Koszt: ~4 zł/mc

**Test:** Spróbować F1 (256 MB) z optymalizacją kodu:
- Usunąć niepotrzebne importy
- Lazy load ciężkich bibliotek
- Optymalizacja queries

**Możliwa oszczędność:** 2 zł/mc (50%)  
**Priorytet:** 🟢 NISKI

---

## 🟢 DROBNE PROBLEMY (Nice to have)

### 9. ✅ **Komentarze w app.yaml mylące**

**Problem:** Komentarz "DO NOT COMMIT TO GIT" ale plik JUŻ JEST w Git!

**Naprawa:** Usunąć mylące komentarze

---

### 10. ✅ **Duplikaty w komentarzach**

**Problem:** Dwa razy `# Google Cloud Storage (optional)` w app.yaml

**Naprawa:** Usunąć duplikat

---

## 📊 PODSUMOWANIE NAPRAW

### Krytyczne (NATYCHMIAST):
1. ✅ Zmienić wszystkie secrets i użyć Secret Manager
2. ✅ Usunąć secrets z Git history

### Średnie (Ten tydzień):
3. ✅ Wyłączyć niepotrzebne GCP API
4. ✅ Wyczyścić staging bucket
5. ✅ Naprawić lub usunąć TODOs
6. ✅ Skonfigurować lub usunąć Zencal
7. ✅ Włączyć Sentry monitoring

### Niskie (Kiedy masz czas):
8. ✅ Przetestować F1 instance
9. ✅ Cleanup komentarzy w app.yaml

---

## 💰 WPŁYW NA KOSZTY

**Obecne koszty:** ~24 zł/mc
- Cloud SQL: 18 zł/mc
- App Engine F2: 4 zł/mc
- Storage: 1.5 zł/mc
- Secrets: 0 zł (nie używasz Secret Manager)

**Po naprawach (WYKONANE):**
- ✅ Cloud SQL: 18 zł/mc (bez zmian, musi działać)
- ❌ App Engine F1: NIE MOŻLIWE (256 MB RAM za mało - crashuje z 500)
- ✅ Storage: 1.4 zł/mc (63 MB staging bucket wyczyszczone)
- ✅ GCP APIs: 7 niepotrzebnych API wyłączonych (oszczędność potencjalnych kosztów)

**RAZEM:** ~23.9 zł/mc (oszczędność ~0.10 zł/mc)

**Sentry:** Kod gotowy, DSN skonfigurowany ale NIE WDROŻONY (powodował crashe 500)  
**Rozwiązanie:** Użyj GCP Secret Manager dla SENTRY_DSN zamiast hardcoded w app.yaml

---

## ⚡ PLAN NAPRAWY (Kolejność wykonania)

### Faza 1: SECURITY (NATYCHMIAST - 2h)
1. ✅ Włączyć Secret Manager API
2. ✅ Utworzyć secrets w Secret Manager
3. ✅ Zaktualizować app.yaml do użycia Secret Manager
4. ✅ Zmienić WSZYSTKIE credentials
5. ✅ Usunąć secrets z Git history
6. ✅ Dodać app.yaml do .gitignore

### Faza 2: CLEANUP (30min)
7. ✅ Wyłączyć niepotrzebne GCP API
8. ✅ Wyczyścić staging bucket

### Faza 3: CODE QUALITY (1h)
9. ✅ Naprawić TODOs w kodzie
10. ✅ Usunąć Zencal jeśli nie używasz

### Faza 4: MONITORING (30min)
11. ✅ Włączyć Sentry monitoring

### Faza 5: OPTYMALIZACJA (Opcjonalnie)
12. ✅ Test F1 instance

**TOTAL TIME:** 4-5 godzin dla full naprawy

---

## 🎯 REKOMENDACJE FINALNE

1. **SECURITY FIRST** - Zmień wszystkie credentials DZISIAJ!
2. **Secret Manager** - Koszt 0.20 zł/mc to NICZEGO w porównaniu do bezpieczeństwa
3. **Sentry** - Włącz monitoring, tracisz leady przez błędy których nie widzisz
4. **Cleanup** - Wyłącz niepotrzebne API i wyczyść buckety
5. **F1 test** - Możesz zaoszczędzić 2 zł/mc ale to najmniejszy priorytet

**KONKLUZJA:** Aplikacja działa ale ma POWAŻNE luki bezpieczeństwa. Fix security FIRST, reszta może poczekać.
