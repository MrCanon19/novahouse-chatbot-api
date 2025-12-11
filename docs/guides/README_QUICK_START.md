# 🚀 NOVAHOUSE CHATBOT - SZYBKI START

## ⚡ W 5 Minutach od Zera do Działającego Systemu

Ten przewodnik przeprowadzi Cię przez **kompletną konfigurację** - od pustego folderu do w pełni działającego chatbota z rezerwacjami.

---

## 📋 KROK 1: Przygotuj Klucze API (10 minut)

### 🔹 Monday.com (CRM)

**Co to jest:** System zarządzania leadami - wszystkie zapytania z chatbota trafiają tu automatycznie.

**Jak uzyskać:**

1. Zaloguj się na [Monday.com](https://monday.com)
2. Kliknij **awatar** (prawy górny róg) → **Admin**
3. **API** → **Developers** → **Personal API Token**
4. Kliknij **Generate** → skopiuj klucz
5. Otwórz swoją tablicę → URL ma format: `monday.com/boards/2145240699`
   - To `2145240699` to **Board ID**

**Zapisz:**
```
MONDAY_API_KEY=twoj_wygenerowany_klucz
MONDAY_BOARD_ID=2145240699
```

---

### 🔹 Booksy (Rezerwacje)

**Co to jest:** System rezerwacji konsultacji - klienci mogą umówić się z Tobą lub Twoimi agentami.

**Jak uzyskać:**

1. Zaloguj się: [Booksy Business](https://booksy.com/en-us/business)
2. **Settings** → **Integrations** → **API**
3. Kliknij **Generate API Key** → skopiuj
4. **Settings** → **Business Info** → znajdź **Business ID**
5. **Settings** → **Team** → Dodaj agentów (jeśli jeszcze nie masz):
   - Marcin Kubiak (szef)
   - Agent 1, Agent 2, Agent 3

**Zapisz:**
```
BOOKSY_API_KEY=twoj_klucz_booksy
BOOKSY_BUSINESS_ID=twoje_business_id
```

---

### 🔹 Google Gemini AI (Opcjonalnie)

**Co to jest:** Sztuczna inteligencja do odpowiedzi chatbota. **Bez tego też działa** (używa FAQ).

**Jak uzyskać:**

1. Przejdź: [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Kliknij **Create API Key**
3. Wybierz projekt (lub utwórz nowy)
4. Skopiuj klucz

**Zapisz:**
```
GEMINI_API_KEY=twoj_klucz_gemini
```

⚠️ **Możesz pominąć** - chatbot działa z FAQ (10 pytań).

---

## 📋 KROK 2: Konfiguracja (2 minuty)

### 1. Skopiuj plik konfiguracyjny

```bash
cd /Users/michalmarini/Projects/manus/chatbot-api
cp .env.example .env
```

### 2. Otwórz plik `.env` i wypełnij:

```bash
nano .env
# LUB
code .env  # jeśli używasz VS Code
```

### 3. Wklej swoje klucze:

```bash
# Monday.com
MONDAY_API_KEY=eyJhbGciOiJIUzI1NiJ9...  # Twój klucz
MONDAY_BOARD_ID=2145240699

# Booksy
BOOKSY_API_KEY=Bearer sk_live_...  # Twój klucz
BOOKSY_BUSINESS_ID=123456

# Gemini (opcjonalnie)
GEMINI_API_KEY=AIzaSy...  # Twój klucz lub zostaw puste

# Admin (opcjonalnie - zabezpiecza panel admina)
ADMIN_API_KEY=twoje-haslo-admin

# Flask
SECRET_KEY=generuj-losowy-string-32-znaki
```

### 4. Zapisz (Ctrl+O, Enter, Ctrl+X w nano)

---

## 📋 KROK 3: Uruchomienie (1 minuta)

### Lokalne (development):

```bash
# Aktywuj środowisko (jeśli masz)
source venv/bin/activate

# Uruchom
python src/main.py
```

**Otwórz przeglądarkę:**
- Dashboard: http://localhost:8080
- Panel Admin: http://localhost:8080/admin
- Kwalifikacja: http://localhost:8080/qualification
- Chatbot: http://localhost:8080/static/chatbot.html

---

### Produkcja (Google Cloud):

```bash
# Deploy
gcloud app deploy --quiet

# Zobacz logi
gcloud app logs tail -s default
```

**Twoja aplikacja:**
- https://glass-core-467907-e9.ey.r.appspot.com

---

## 📋 KROK 4: Test Integracji (2 minuty)

### 🧪 Test Monday.com

```bash
curl -X POST http://localhost:8080/api/chatbot/monday-test \
  -H "Content-Type: application/json" \
  -H "X-ADMIN-API-KEY: twoje-haslo-admin"
```

**Oczekiwany wynik:**
```json
{
  "message": "Monday.com connection successful",
  "api_key_set": true,
  "board_id_set": true
}
```

---

### 🧪 Test Booksy

```bash
curl -X POST http://localhost:8080/api/booking/test \
  -H "Content-Type: application/json" \
  -H "X-ADMIN-API-KEY: twoje-haslo-admin"
```

**Oczekiwany wynik:**
```json
{
  "message": "Booksy connection successful",
  "api_key_set": true,
  "business_id_set": true,
  "services_count": 2,
  "staff_count": 4
}
```

---

### 🧪 Test Agentów Booksy

```bash
curl http://localhost:8080/api/booking/staff
```

**Oczekiwany wynik:**
```json
{
  "staff": [
    {
      "id": "staff_123",
      "name": "Marcin Kubiak",
      "title": "CEO & Senior Designer",
      "specialization": "Premium & Luxury"
    },
    {
      "id": "staff_456",
      "name": "Anna Kowalska",
      "title": "Interior Architect"
    },
    {
      "id": "staff_789",
      "name": "Paweł Nowak",
      "title": "Junior Designer"
    }
  ],
  "count": 3
}
```

✅ **Jeśli widzisz swoich agentów - DZIAŁA!**

---

## 📋 KROK 5: Użytkowanie (Gotowe!)

### Dla Klientów:

1. **Chatbot** → Otwórz stronę główną
2. **Kwalifikacja** → Wypełnij 8 pytań → Otrzymaj rekomendację
3. **Rezerwacja** → Wybierz agenta → Wybierz termin → Potwierdź

**Flow:**
```
Klient → Chatbot → Kwalifikacja → Lead w Monday → Rezerwacja w Booksy
```

---

### Dla Marcina i Zespołu:

1. **Monday.com Dashboard** → Wszystkie leady z automatycznymi danymi
2. **Booksy Dashboard** → Wszystkie rezerwacje, kalendarz zespołu
3. **Admin Panel** → http://localhost:8080/admin → Statystyki, leady

---

## 🎯 Co się Dzieje Automatycznie?

### ✅ Po wypełnieniu kwalifikacji przez klienta:

1. **System obliczy** rekomendowany pakiet (Standard/Premium/Luxury)
2. **Utworzy lead** w bazie danych
3. **Zsyncuje do Monday.com** z danymi:
   - Imię, email, telefon
   - Rekomendowany pakiet
   - % pewności rekomendacji
   - Typ nieruchomości, styl wnętrz, budżet
   - Status: "New Lead"

### ✅ Po wyborze terminu rezerwacji:

1. **Klient wybiera agenta** (Marcin lub ktoś z zespołu)
2. **System pobiera dostępne terminy** tego agenta
3. **Tworzy rezerwację w Booksy**
4. **Aktualizuje status leada** w Monday → "consultation_booked"
5. **(Przyszłość) Wysyła email** potwierdzający

---

## 🔧 Troubleshooting

### Problem: "Monday.com not configured"

**Rozwiązanie:**
```bash
# Sprawdź czy klucze są w .env
cat .env | grep MONDAY

# Powinno pokazać:
MONDAY_API_KEY=twoj_klucz
MONDAY_BOARD_ID=2145240699

# Restart aplikacji
python src/main.py
```

---

### Problem: "Booksy connection failed"

**Rozwiązanie:**
```bash
# Sprawdź klucze
cat .env | grep BOOKSY

# Test połączenia
curl http://localhost:8080/api/booking/test \
  -H "X-ADMIN-API-KEY: twoj_admin_key"
```

---

### Problem: "No staff members found"

**Rozwiązanie:**
1. Zaloguj się do Booksy Business
2. Settings → Team
3. Dodaj agentów (Marcin + zespół)
4. Ustaw każdemu:
   - Imię i nazwisko
   - Tytuł (np. "Senior Designer")
   - Dostępność (godziny pracy)
   - Zdjęcie (opcjonalnie)

---

## 📞 Kontakt

**Developer:** Michał Marini
- GitHub: MrCanon19
- Email: marini19944@gmail.com
- Tel: 508 397 440

**Klient:** Marcin Kubiak
- Email: m.kubiak@novahouse.pl
- Tel: 502 274 453

---

## 📚 Dodatkowa Dokumentacja

- **Pełna dokumentacja:** `RUNDY_1_2_3_FINAL_SUMMARY.md`
- **Monday.com:** `MONDAY_INTEGRATION.md`
- **Booksy:** `BOOKSY_INTEGRATION.md`
- **Dashboard:** `DASHBOARD_AUDIT.md`
- **API Endpoints:** Zobacz commit `f58ff77`

---

## ✅ Checklist Gotowości

Przed uruchomieniem produkcyjnym upewnij się:

- [ ] Wszystkie klucze API wpisane w `.env`
- [ ] Monday.com board gotowy (kolumny: status, email, phone, package)
- [ ] Booksy business skonfigurowany (agenci dodani)
- [ ] Test Monday.com przechodzi ✅
- [ ] Test Booksy przechodzi ✅
- [ ] Lista agentów się pobiera ✅
- [ ] Deploy na GCP wykonany
- [ ] Dashboard otwiera się poprawnie
- [ ] Kwalifikacja działa (8 pytań)
- [ ] Rezerwacja tworzy się w Booksy

---

🎉 **GOTOWE! System działa w pełni automatycznie!**

Wystarczy, że klienci wejdą na stronę - reszta dzieje się sama:
1. Chat → 2. Kwalifikacja → 3. Lead w Monday → 4. Rezerwacja z agentem → 5. DONE! ✅
