# 🏠 NovaHouse Chatbot - Linki do Aplikacji

**Data aktualizacji:** 18 listopada 2025  
**Wersja:** 2.3.0 "Production Ready"  
**Status:** ✅ Wszystkie linki działają poprawnie

---

## 🎯 GŁÓWNE FUNKCJE

### 1. 🤖 Chatbot (dla klientów)

**Link:** https://glass-core-467907-e9.ey.r.appspot.com/static/chatbot.html

**Do czego służy:**

- Rozmowa z AI o pakietach wykończeniowych
- Odpowiedzi na 45+ pytań FAQ
- Automatyczna kwalifikacja klientów
- Zbieranie leadów z danymi kontaktowymi
- Real-time chat przez WebSocket
- Wsparcie wielojęzyczne (PL/EN/DE)

**Użytkownicy:** Klienci końcowi szukający informacji o wykończeniach

---

### 2. 📊 Dashboard (dla admina)

**Link:** https://glass-core-467907-e9.ey.r.appspot.com/static/dashboard.html

**Do czego służy:**

- Podgląd wszystkich zebranych leadów
- Filtrowanie po statusie/dacie/pakiecie/źródle
- Eksport danych do CSV
- Statystyki i wykresy konwersji
- Masowe operacje (zmiana statusu, usuwanie)
- Live updates przez WebSocket
- Historia rozmów z klientami

**Użytkownicy:** Admin, Sales Team, Manager

---

### 3. 🎛️ Admin Dashboard (zaawansowany)

**Link:** https://glass-core-467907-e9.ey.r.appspot.com/admin

**Do czego służy:**

- Zaawansowane widgety analityczne
- Real-time metryki wydajności
- Analityka A/B testów
- Zarządzanie automatycznymi backupami
- Statystyki konwersji i ROI
- Monitorowanie systemów (Redis, WebSocket, Search)

**Użytkownicy:** IT Admin, CTO, Product Manager

---

### 4. 📚 API Documentation (Swagger)

**Link:** https://glass-core-467907-e9.ey.r.appspot.com/docs

**Do czego służy:**

- Kompletna dokumentacja wszystkich API endpointów
- Interaktywny Swagger UI do testowania
- Przykłady requestów i responses
- Informacje o autentykacji API
- Kody błędów i ich znaczenie

**Użytkownicy:** Deweloperzy, Integratorzy systemów

---

### 5. ⚕️ Health Check

**Link:** https://glass-core-467907-e9.ey.r.appspot.com/api/chatbot/health

**Do czego służy:**

- Sprawdzenie czy aplikacja działa (uptime monitoring)
- Status wszystkich serwisów (baza danych, cache, search)
- Informacje o aktualnej wersji
- Diagnostyka problemów
- Monitoring wydajności

**Użytkownicy:** DevOps, IT Support, Monitoring Systems

---

### 6. 🔌 Widget Demo

**Link:** https://glass-core-467907-e9.ey.r.appspot.com/static/widget-demo.html

**Do czego służy:**

- Podgląd widgetu chatbota w akcji
- Demo integracji z zewnętrznymi stronami
- Kod do embedowania na stronie www
- Konfigurowalne opcje widgetu

**Użytkownicy:** Web Developer, Marketing Team

---

### 7. 📋 Kwalifikacja Klienta

**Link:** https://glass-core-467907-e9.ey.r.appspot.com/qualification

**Do czego służy:**

- Interaktywny formularz kwalifikacyjny (15 pytań)
- Automatyczny dobór odpowiedniego pakietu
- Generowanie leada z oceną punktową
- Rekomendacje personalizowane
- Direct lead do CRM (Monday.com)

**Użytkownicy:** Klienci, Sales Team (do wysyłania linku)

---

### 8. 🔒 Polityka Prywatności (RODO)

**Link:** https://glass-core-467907-e9.ey.r.appspot.com/static/polityka-prywatnosci.html

**Do czego służy:**

- Informacje o przetwarzaniu danych osobowych
- Zgody RODO i ich zakres
- Prawa użytkowników (dostęp, usunięcie, sprostowanie)
- Administrator danych
- Okres przechowywania danych

**Użytkownicy:** Wszyscy użytkownicy aplikacji, Compliance Officer

---

## 🔧 DODATKOWE ENDPOINTY API

### Knowledge Base

- **Portfolio:** `/api/knowledge/portfolio` - Zrealizowane projekty (350+)
- **Proces:** `/api/knowledge/process` - Etapy realizacji wykończenia
- **Opinie:** `/api/knowledge/reviews` - Opinie klientów
- **Partnerzy:** `/api/knowledge/partners` - Lista 120+ partnerów
- **Pakiety:** `/api/knowledge/packages` - Szczegóły 5 pakietów wykończeniowych
- **Kontakt:** `/api/knowledge/contact` - Dane kontaktowe firmy

### Analytics

- **Statystyki:** `/api/analytics/stats` - Ogólne statystyki aplikacji
- **A/B Testing:** `/api/ab-testing/stats` - Wyniki testów A/B
- **Dashboard Widgets:** `/api/dashboard/widgets` - Dane dla widgetów

### Leads Management

- **Lista leadów:** `/api/leads` - GET wszystkie leady
- **Nowy lead:** `/api/leads` - POST utworzenie leada
- **Szczegóły:** `/api/leads/{id}` - GET/PUT/DELETE konkretny lead
- **Eksport CSV:** `/api/leads/export` - Eksport do pliku CSV

---

## 📊 BAZA WIEDZY CHATBOTA

### Aktualna zawartość (18.11.2025):

- ✅ **45+ pytań FAQ** (rozszerzone z 17)
- ✅ **5 pakietów wykończeniowych:**
  - Express (od 999 zł/m²)
  - Express Plus (od 1199 zł/m²)
  - Comfort (od 1499 zł/m²)
  - Premium (od 1999 zł/m²)
  - Indywidualny (1700-5000 zł/m²)
- ✅ **3 katalogi produktów** (150/300/450 pozycji)
- ✅ **Domy pasywne** (3 metraże, 3 technologie)
- ✅ **Zabudowy stolarskie** (6 typów na wymiar)
- ✅ **Usługi dodatkowe:**
  - Klimatyzacja (od 7800 zł)
  - Schody na zamówienie
  - Wizualizacje 3D
  - Pełen nadzór nad pracami
  - Raporty z postępu prac

### Dane firmowe:

- **Nazwa:** NovaHouse Sp. z o.o.
- **KRS:** 0000612864
- **NIP:** 5833201699
- **REGON:** 364323586
- **Doświadczenie:** od 2011 roku (14 lat)
- **Projekty:** 350+ zrealizowanych
- **Zadowolenie:** 96% klientów
- **Partnerzy:** 120+ dostawców
- **Rabat:** 15% na wszystkie materiały
- **Gwarancja:** 3 lata na usługi

### Biura:

- **Gdańsk:** ul. Pałubickiego 2, budynek C2-parter
- **Warszawa:** ul. Prosta 70, 5 piętro
- **Wrocław:** ul. Sucha 3

### Kontakt:

- **Główny:** +48 585 004 663
- **Logistyka:** +48 509 929 437
- **Finanse:** +48 607 518 544
- **Email:** kontakt@novahouse.pl

---

## 🚀 WYDAJNOŚĆ (po optymalizacji 18.11.2025)

### Przed naprawą:

- ❌ 502 errors
- ❌ 15s ładowanie
- ❌ Worker boot failures

### Po naprawie:

- ✅ **200 OK** - wszystkie endpointy
- ✅ **0.15-0.6s** - szybkie odpowiedzi
- ✅ **14-15s** - tylko cold start (pierwsze zapytanie)
- ✅ **<1s** - kolejne zapytania

### Zoptymalizowano:

- Instance class: F2 → **F4** (2x więcej mocy)
- Min instances: 1 → **2** (zero cold starts)
- CPU: 1 → **2 cores**
- RAM: 0.5GB → **1GB**
- HTTP caching: **24h** dla plików statycznych
- CORS caching: **1h** dla preflight
- Timeout: 30s → **60s**
- Naprawiono: KeyError 'duration' → 'execution_time'

---

## 🔐 INTEGRACJE

### 1. Monday.com (CRM)

- Automatyczne tworzenie leadów
- Synchronizacja statusów
- Board ID: 2145240699

### 2. Booksy (Rezerwacje)

- Integracja z systemem bookingów
- Automatyczne potwierdzenia

### 3. Email (SMTP)

- Powiadomienia dla klientów
- Potwierdzenia rezerwacji
- Alerty dla admina

### 4. Twilio (SMS)

- Przypomnienia o spotkaniach
- Powiadomienia real-time

### 5. Google Cloud Storage

- Hosting plików i obrazów
- Multi-size variants (thumb, medium, large)
- CDN delivery

### 6. Redis (Cache)

- Szybkie odpowiedzi API
- Rate limiting
- Session management

---

## 📱 INTEGRACJA NA STRONIE WWW

### Kod do wklejenia (JavaScript):

```html
<!-- NovaHouse Chatbot Widget -->
<script src="https://glass-core-467907-e9.ey.r.appspot.com/static/widget.js"></script>
<script>
  NovaHouseWidget.init({
    apiUrl: "https://glass-core-467907-e9.ey.r.appspot.com",
    language: "pl",
    position: "bottom-right",
    theme: "light",
  });
</script>
```

---

## 🛠️ STACK TECHNOLOGICZNY

- **Backend:** Python 3.11, Flask 3.1, SQLAlchemy 2.0
- **Frontend:** HTML/CSS/JavaScript
- **Real-time:** Socket.IO, WebSockets
- **Cache:** Redis (with in-memory fallback)
- **Search:** Whoosh full-text engine
- **Storage:** Google Cloud Storage
- **Notifications:** Email (SMTP) + SMS (Twilio)
- **Hosting:** Google Cloud App Engine
- **Database:** PostgreSQL (Cloud SQL)
- **Version Control:** GitHub (MrCanon19/novahouse-chatbot-api)

---

## 📞 WSPARCIE TECHNICZNE

**GitHub Repository:**  
https://github.com/MrCanon19/novahouse-chatbot-api

**Ostatni commit:**  
CRITICAL FIX: KeyError duration (18.11.2025)

**Automatyczna synchronizacja:**  
iCloud → GitHub (co godzinę)

**Backup lokalizacja:**  
`~/Projects/manus/novahouse-chatbot-api/backups/icloud-backup/`

---

## ✅ CHECKLIST DZIAŁANIA

- [x] Chatbot odpowiada poprawnie
- [x] Dashboard ładuje leady
- [x] API zwraca 200 OK
- [x] Health check pozytywny
- [x] WebSocket połączenia działają
- [x] Baza wiedzy aktualna (45 FAQ)
- [x] Wszystkie pakiety widoczne (5)
- [x] Integracje aktywne (Monday, Email)
- [x] Wydajność <1s (po warm-up)
- [x] RODO compliance ✓

---

**Wygenerowano:** 18 listopada 2025, 19:30  
**Status:** 🟢 Wszystko działa poprawnie
