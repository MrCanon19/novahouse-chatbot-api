# 🏠 NovaHouse Chatbot - Linki do Aplikacji

**Wersja:** 2.3.0 | **Data:** 18.11.2025 | **Status:** 🟢 Wszystko działa

---

## 🌐 GŁÓWNE LINKI

### 🤖 Chatbot dla Klientów

**https://glass-core-467907-e9.ey.r.appspot.com/static/chatbot.html**  
AI chat o pakietach wykończeniowych, 45+ FAQ, automatyczna kwalifikacja, zbieranie leadów

### 📊 Dashboard Admina

**https://glass-core-467907-e9.ey.r.appspot.com/static/dashboard.html**  
Zarządzanie leadami, filtrowanie, eksport CSV, statystyki konwersji, live updates

### 🎛️ Admin Dashboard (Zaawansowany)

**https://glass-core-467907-e9.ey.r.appspot.com/admin**  
Widgety analityczne, real-time metryki, A/B testing, backupy, ROI

### 📚 Dokumentacja API (Swagger)

**https://glass-core-467907-e9.ey.r.appspot.com/docs**  
Interaktywna dokumentacja wszystkich API endpoints, przykłady, testowanie

### ⚕️ Health Check

**https://glass-core-467907-e9.ey.r.appspot.com/api/chatbot/health**  
Status aplikacji, uptime monitoring, diagnostyka, stan wszystkich serwisów

### 🔌 Widget Demo

**https://glass-core-467907-e9.ey.r.appspot.com/static/widget-demo.html**  
Podgląd chatbot widget, kod do embedowania, demo integracji

### 📋 Formularz Kwalifikacji

**https://glass-core-467907-e9.ey.r.appspot.com/qualification**  
15 pytań kwalifikacyjnych, automatyczny dobór pakietu, direct lead do CRM

### 🔒 Polityka Prywatności (RODO)

**https://glass-core-467907-e9.ey.r.appspot.com/static/polityka-prywatnosci.html**  
Zgody RODO, prawa użytkowników, przetwarzanie danych osobowych

---

## 🔧 API ENDPOINTS

**Knowledge Base:**

- `/api/knowledge/portfolio` - 350+ projektów
- `/api/knowledge/packages` - 5 pakietów wykończeniowych
- `/api/knowledge/process` - Etapy realizacji
- `/api/knowledge/reviews` - Opinie klientów
- `/api/knowledge/partners` - 120+ partnerów
- `/api/knowledge/contact` - Dane kontaktowe

**Analytics:**

- `/api/analytics/stats` - Statystyki aplikacji
- `/api/ab-testing/stats` - Wyniki testów A/B
- `/api/dashboard/widgets` - Dane dla widgetów

**Leads:**

- `/api/leads` - Lista/tworzenie leadów
- `/api/leads/{id}` - Szczegóły/edycja/usuwanie
- `/api/leads/export` - Eksport CSV

---

## 📊 BAZA WIEDZY

✅ **45+ pytań FAQ** (rozszerzone z 17)  
✅ **5 pakietów:** Express (999 zł/m²), Express Plus (1199 zł/m²), Comfort (1499 zł/m²), Premium (1999 zł/m²), Indywidualny (1700-5000 zł/m²)  
✅ **3 katalogi produktów:** Basic 150, Standard 300, Premium 450  
✅ **Domy pasywne:** 3 metraże × 3 technologie  
✅ **Zabudowy stolarskie:** 6 typów na wymiar  
✅ **Usługi dodatkowe:** Klimatyzacja (7800 zł), schody, wizualizacje 3D, nadzór, raporty

---

## 🏢 DANE FIRMY

**NovaHouse Sp. z o.o.**  
KRS: 0000612864 | NIP: 5833201699 | REGON: 364323586  
**Od 2011 roku** | 350+ projektów | 96% zadowolenia | 120+ partnerów

**Biura:**

- Gdańsk: ul. Pałubickiego 2, C2-parter
- Warszawa: ul. Prosta 70, 5 piętro
- Wrocław: ul. Sucha 3

**Kontakt:**  
+48 585 004 663 | +48 509 929 437 | +48 607 518 544  
kontakt@novahouse.pl

---

## 🚀 WYDAJNOŚĆ (18.11.2025)

**Przed optymalizacją:** ❌ 502 errors, 15s load  
**Po optymalizacji:** ✅ 200 OK, 0.15-0.6s response, <1s po warm-up

**Zoptymalizowano:**  
F2→F4 instances | 1→2 min instances | 1→2 CPU | 0.5→1GB RAM  
HTTP cache 24h | CORS cache 1h | Timeout 30→60s

---

## 🔐 INTEGRACJE

✅ Monday.com (CRM, Board: 2145240699)  
✅ Booksy (Rezerwacje)  
✅ Email (SMTP) + Twilio (SMS)  
✅ Google Cloud Storage (CDN)  
✅ Redis (Cache, Rate limiting)

---

## 🛠️ TECH STACK

Python 3.11 | Flask 3.1 | SQLAlchemy 2.0 | Socket.IO | PostgreSQL | Redis | Whoosh | Google Cloud App Engine

**GitHub:** https://github.com/MrCanon19/novahouse-chatbot-api

---

## 📱 KOD WIDGET

```html
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

**Status:** 🟢 Production Ready | **Ostatnia aktualizacja:** 18.11.2025
