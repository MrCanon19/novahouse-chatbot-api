# Status projektu NovaHouse Chatbot API

**Data aktualizacji:** 30 listopada 2025  
**Wersja:** 2.4.0 "Production Ready"  
**Status:** 🟢 Wszystko działa poprawnie

---

## Główne funkcje

### 🤖 Chatbot (dla klientów)
- Rozmowa z AI o pakietach wykończeniowych
- Odpowiedzi na 45+ pytań FAQ
- Automatyczna kwalifikacja klientów
- Zbieranie leadów
- Real-time chat przez WebSocket
- Wsparcie wielojęzyczne (PL/EN/DE)
- [Chatbot link](https://glass-core-467907-e9.ey.r.appspot.com/static/chatbot.html)

### 📊 Dashboard (dla admina)
- Podgląd leadów, filtrowanie, eksport CSV
- Statystyki, wykresy konwersji
- Masowe operacje
- Live updates przez WebSocket
- Historia rozmów
- [Dashboard link](https://glass-core-467907-e9.ey.r.appspot.com/static/dashboard.html)

### 🎛️ Admin Dashboard (zaawansowany)
- Widgety analityczne, A/B testy, backupy
- Monitoring systemów
- [Admin link](https://glass-core-467907-e9.ey.r.appspot.com/admin)

### 📚 API Documentation (Swagger)
- Kompletna dokumentacja API
- Interaktywny Swagger UI
- Przykłady requestów/responses
- [Swagger link](https://glass-core-467907-e9.ey.r.appspot.com/docs)

### ⚕️ Health Check
- Status serwisów, wersja, diagnostyka
- [Health link](https://glass-core-467907-e9.ey.r.appspot.com/api/chatbot/health)

### 🔌 Widget Demo
- Demo widgetu chatbota, kod do embedowania
- [Widget demo link](https://glass-core-467907-e9.ey.r.appspot.com/static/widget-demo.html)

### 📋 Kwalifikacja Klienta
- Formularz kwalifikacyjny, rekomendacje, integracja z CRM
- [Kwalifikacja link](https://glass-core-467907-e9.ey.r.appspot.com/qualification)

### 🔒 Polityka Prywatności (RODO)
- Informacje o przetwarzaniu danych, zgody, prawa
- [RODO link](https://glass-core-467907-e9.ey.r.appspot.com/static/polityka-prywatnosci.html)

---

## Dodatkowe endpointy API
- Portfolio: `/api/knowledge/portfolio`
- Proces: `/api/knowledge/process`
- Opinie: `/api/knowledge/reviews`
- Partnerzy: `/api/knowledge/partners`
- Pakiety: `/api/knowledge/packages`
- Kontakt: `/api/knowledge/contact`
- Statystyki: `/api/analytics/stats`
- A/B Testing: `/api/ab-testing/stats`
- Dashboard Widgets: `/api/dashboard/widgets`
- Leads: `/api/leads` (GET/POST/PUT/DELETE)
- Eksport CSV: `/api/leads/export`

---

## Baza wiedzy chatbota
- 45+ pytań FAQ
- 5 pakietów wykończeniowych
- 3 katalogi produktów
- Domy pasywne, zabudowy stolarskie, usługi dodatkowe

**Dane firmowe:**
- NovaHouse Sp. z o.o.
- KRS: 0000612864
- NIP: 5833201699
- REGON: 364323586
- Doświadczenie: od 2011 roku
- Projekty: 350+
- Zadowolenie: 96%
- Partnerzy: 120+
- Rabat: 15%
- Gwarancja: 3 lata

**Biura:** Gdańsk, Warszawa, Wrocław
**Kontakt:** +48 585 004 663, +48 509 929 437, +48 607 518 544, kontakt@novahouse.pl

---

## Wydajność (po optymalizacji 30.11.2025)
- 200 OK – wszystkie endpointy
- Odpowiedzi: 0.15–0.6s
- Cold start: 14–15s
- Instance class: F4, min instances: 2, CPU: 2 cores, RAM: 1GB
- HTTP caching: 24h, CORS caching: 1h, timeout: 60s
- Naprawiono: KeyError 'duration' → 'execution_time'

---

## Integracje
- Monday.com (CRM)
- Booksy (Rezerwacje)
- Email (SMTP)
- Twilio (SMS)
- Google Cloud Storage
- Redis (Cache)

---

## Integracja na stronie www
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

## Stack technologiczny
- Backend: Python 3.13, Flask 3.1, SQLAlchemy 2.0
- Frontend: HTML/CSS/JavaScript
- Real-time: Socket.IO, WebSockets
- Cache: Redis
- Search: Whoosh
- Storage: Google Cloud Storage
- Notifications: Email (SMTP), SMS (Twilio)
- Hosting: Google Cloud App Engine
- Database: PostgreSQL (Cloud SQL)
- Version Control: GitHub (MrCanon19/novahouse-chatbot-api)

---

## Wsparcie techniczne
- GitHub: https://github.com/MrCanon19/novahouse-chatbot-api
- Ostatni commit: Poprawa stylu markdownlint, 30.11.2025
- Automatyczna synchronizacja: iCloud → GitHub (co godzinę)
- Backup: `~/Projects/manus/novahouse-chatbot-api/backups/icloud-backup/`

---

## Checklist działania
- [x] Chatbot odpowiada poprawnie
- [x] Dashboard ładuje leady
- [x] API zwraca 200 OK
- [x] Health check pozytywny
- [x] WebSocket połączenia działają
- [x] Baza wiedzy aktualna
- [x] Wszystkie pakiety widoczne
- [x] Integracje aktywne
- [x] Wydajność <1s
- [x] RODO compliance

---

**Wygenerowano:** 30 listopada 2025, 19:30
**Status:** 🟢 Wszystko działa poprawnie
