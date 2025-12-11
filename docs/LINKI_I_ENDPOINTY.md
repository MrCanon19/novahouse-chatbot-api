# 🔗 Działające Linki i Endpointy - Nova House Chatbot API

**Produkcja:** `https://glass-core-467907-e9.ey.r.appspot.com`

---

## 📋 Spis Treści

1. [Chatbot - Interfejs Główny](#1-chatbot--interfejs-główny-)
2. [Dashboard - Panel Leadów](#2-dashboard--panel-leadów-)
3. [Panel Administratora](#3-panel-administratora-)
4. [API Documentation (Swagger)](#4-api-documentation-swagger-200-)
5. [Health Check](#5-health-check--działa-i-pokazuje-tylko-status)
6. [Widget Demo](#6-widget-demo-)
7. [Kwalifikacja Klienta](#7-kwalifikacja-klienta-200-)
8. [Polityka Prywatności (RODO)](#8-polityka-prywatności-rodo-)

---

## 1. **Chatbot** 🧪

**URL:** [`https://glass-core-467907-e9.ey.r.appspot.com/static/chatbot.html`](https://glass-core-467907-e9.ey.r.appspot.com/static/chatbot.html)

### Po co:
Główny interfejs chatbota dla klientów końcowych. To jest podstawowy punkt wejścia dla potencjalnych klientów, którzy chcą uzyskać informacje o pakietach wykończeniowych Nova House.

### Użycie:
- Klienci mogą zadawać pytania o pakiety wykończeniowe
- Pytania o ceny i koszty
- Informacje o procesie budowy
- FAQ i odpowiedzi na typowe pytania

### Funkcje:
- ✅ Rozmowa z AI (GPT-4/GPT-3.5)
- ✅ Zbieranie leadów (automatyczne zapisywanie kontaktów)
- ✅ Kwalifikacja klienta (scoring i dopasowanie pakietów)
- ✅ FAQ (odpowiedzi na częste pytania)
- ✅ WebSocket support (live updates)
- ✅ Historia konwersacji

### Techniczne:
- **Typ:** Static HTML + JavaScript
- **Backend:** Flask API (`/api/chatbot/*`)
- **WebSocket:** Real-time messaging (opcjonalne)

---

## 2. **Dashboard** ✅

**URL:** [`https://glass-core-467907-e9.ey.r.appspot.com/static/dashboard.html`](https://glass-core-467907-e9.ey.r.appspot.com/static/dashboard.html)

### Po co:
Panel administracyjny do zarządzania leadami. Umożliwia zespołowi sprzedaży i administracji przeglądanie, filtrowanie i zarządzanie wszystkimi leadami zebranymi przez chatbota.

### Użycie:
- Podgląd wszystkich leadów w jednym miejscu
- Filtrowanie po dacie, statusie, źródle
- Eksport leadów do CSV
- Podgląd szczegółów konwersacji

### Funkcje:
- ✅ Lista leadów z filtrowaniem
- ✅ Statystyki konwersji
- ✅ Wykresy i analityka
- ✅ Historia rozmów (pełne logi)
- ✅ Live updates przez WebSocket
- ✅ Eksport do CSV
- ✅ Status leadów (nowy, w trakcie, zamknięty)

### Techniczne:
- **Typ:** Static HTML + JavaScript
- **Backend:** Flask API (`/api/leads/*`, `/api/analytics/*`)
- **Autoryzacja:** API Key (X-API-KEY header)

---

## 3. **Panel Administratora** ✅

**URL:** [`https://glass-core-467907-e9.ey.r.appspot.com/admin`](https://glass-core-467907-e9.ey.r.appspot.com/admin)

### Po co:
Zaawansowany panel administratora z widgetami analitycznymi. Kompleksowe narzędzie do zarządzania całym systemem, monitoring i diagnostyka.

### Użycie:
- Zarządzanie systemem na wyższym poziomie niż podstawowy dashboard
- Monitoring wydajności i zdrowia aplikacji
- Diagnostyka problemów
- Zarządzanie backupami i migracjami

### Funkcje:
- ✅ **Widgety analityczne:**
  - A/B testing tracking
  - Conversion tracking
  - Performance metrics
- ✅ **Zarządzanie backupami:**
  - Tworzenie backupów
  - Przywracanie z backupów
  - Historia backupów
- ✅ **Monitoring systemów:**
  - Telegram notifications status
  - RODO audit logs
  - System health checks
- ✅ **Głębsza analiza danych:**
  - User behavior analytics
  - Conversation quality metrics
  - Lead scoring analysis
- ✅ **Diagnostyka wydajności:**
  - Database performance
  - API response times
  - Error tracking

### Techniczne:
- **Typ:** Flask Template (HTML)
- **Backend:** Flask API (`/api/admin/*`, `/api/dashboard-widgets/*`)
- **Autoryzacja:** API Key (X-API-KEY header)

---

## 4. **API Documentation (Swagger)** (200 ✅) - jak używać

**URL:** [`https://glass-core-467907-e9.ey.r.appspot.com/docs`](https://glass-core-467907-e9.ey.r.appspot.com/docs)

### Po co:
Interaktywna dokumentacja API w formacie Swagger UI. Umożliwia developerom i integratorom poznanie wszystkich dostępnych endpointów API, ich parametrów, odpowiedzi i możliwość testowania bezpośrednio w przeglądarce.

### Użycie:
- Developerzy mogą poznać wszystkie endpointy API
- Testowanie API bez potrzeby pisania kodu
- Sprawdzanie wymaganych parametrów i formatów
- Przykłady requestów i responses

### Funkcje:
- ✅ Swagger UI (interaktywny interfejs)
- ✅ Przykłady requestów/responses
- ✅ Testowanie API w przeglądarce
- ✅ Dokumentacja wszystkich endpointów:
  - `/api/chatbot/*` - Chatbot endpoints
  - `/api/leads/*` - Lead management
  - `/api/analytics/*` - Analytics
  - `/api/admin/*` - Admin operations
  - `/api/backup/*` - Backup management
  - `/api/migration/*` - Database migrations
  - I wiele innych...

### Techniczne:
- **Typ:** Flask Blueprint (Swagger UI)
- **Backend:** Flask-Swagger-UI
- **Status:** 200 OK ✅

---

## 5. **Health Check** ✅ - działa i pokazuje tylko status

**URL:** [`https://glass-core-467907-e9.ey.r.appspot.com/api/chatbot/health`](https://glass-core-467907-e9.ey.r.appspot.com/api/chatbot/health)

### Po co:
Endpoint diagnostyczny do monitorowania zdrowia aplikacji. Używany przez systemy monitoringu (np. Uptime Robot, Google Cloud Monitoring) do sprawdzania, czy aplikacja działa poprawnie.

### Użycie:
- Monitoring zdrowia aplikacji
- Sprawdzenie czy serwis działa
- Automatyczne alerty przy awariach
- Integracja z systemami monitoringu

### Funkcje:
- ✅ Status serwisów (database, Redis, etc.)
- ✅ Wersja aplikacji
- ✅ Uptime informacje
- ✅ Dostępność bazy danych
- ✅ Response time metrics

### Przykładowa odpowiedź:
```json
{
  "status": "healthy",
  "version": "2.3",
  "database": "connected",
  "uptime": "5d 12h 30m"
}
```

### Techniczne:
- **Typ:** REST API endpoint
- **Method:** GET
- **Autoryzacja:** Brak (publiczny endpoint)
- **Status:** 200 OK ✅

---

## 6. **Widget Demo** ✅

**URL:** [`https://glass-core-467907-e9.ey.r.appspot.com/static/widget-demo.html`](https://glass-core-467907-e9.ey.r.appspot.com/static/widget-demo.html)

### Po co:
Demonstracja widgetu chatbota do osadzenia na stronie internetowej. Pokazuje jak widget wygląda i działa w różnych konfiguracjach, co ułatwia decyzję o implementacji.

### Użycie:
- Pokazanie jak widget wygląda na stronie www
- Testowanie różnych pozycji widgetu (bottom-right, bottom-left, etc.)
- Podgląd responsywności na różnych urządzeniach
- Kopiowanie kodu HTML do embedowania

### Funkcje:
- ✅ Kod HTML do embedowania
- ✅ Preview widget w różnych pozycjach:
  - Bottom-right (domyślna)
  - Bottom-left
  - Top-right
  - Top-left
- ✅ Responsywność (mobile, tablet, desktop)
- ✅ Customizacja kolorów i stylów

### Techniczne:
- **Typ:** Static HTML + JavaScript
- **Widget:** Embeddable chatbot widget
- **Integration:** Simple `<script>` tag

---

## 7. **Kwalifikacja Klienta** 200 ✅

**URL:** [`https://glass-core-467907-e9.ey.r.appspot.com/qualification`](https://glass-core-467907-e9.ey.r.appspot.com/qualification)

### Po co:
Interaktywny formularz kwalifikacyjny dla potencjalnych klientów. Zbiera szczegółowe informacje o projekcie klienta, aby automatycznie dopasować najlepszy pakiet wykończeniowy i ocenić potencjał leada.

### Użycie:
- Zbieranie szczegółowych informacji o projekcie klienta
- Automatyczne dopasowanie pakietów wykończeniowych
- Scoring leadów (ocena wartości leada)
- Integracja z CRM (Monday.com)

### Funkcje:
- ✅ **Formularz z progress barem:**
  - 7 pytań kwalifikacyjnych
  - Wizualny wskaźnik postępu
  - Walidacja danych
- ✅ **Pytania o:**
  - Metraż mieszkania/domu
  - Budżet projektu
  - Lokalizację
  - Preferencje wykończenia
  - Termin realizacji
  - Poziom wykończenia (standard, premium, lux)
  - Dodatkowe wymagania
- ✅ **Automatyczne rekomendacje pakietów:**
  - Dopasowanie na podstawie odpowiedzi
  - Porównanie pakietów
  - Estymacja kosztów
- ✅ **System scoringu i dopasowania:**
  - Lead score (0-100)
  - Priorytetyzacja leadów
  - Automatyczne przypisanie do sales
- ✅ **Potencjalna integracja z CRM:**
  - Monday.com integration
  - Automatyczne tworzenie leadów
  - Synchronizacja danych

### Techniczne:
- **Typ:** Flask Route (HTML Template)
- **Backend:** Flask API (`/api/qualification/*`)
- **Status:** 200 OK ✅

---

## 8. **Polityka Prywatności (RODO)** ✅

**URL:** [`https://glass-core-467907-e9.ey.r.appspot.com/static/polityka-prywatnosci.html`](https://glass-core-467907-e9.ey.r.appspot.com/static/polityka-prywatnosci.html)

### Po co:
Zgodność z RODO/GDPR. Wymagany dokument prawny informujący użytkowników o przetwarzaniu ich danych osobowych, prawach użytkowników i zasadach prywatności.

### Użycie:
- Informacja dla użytkowników o przetwarzaniu danych
- Wymóg prawny (RODO/GDPR compliance)
- Link w stopce strony lub w formularzach
- Podstawa prawna dla zbierania danych

### Funkcje:
- ✅ **Zgody:**
  - Zgoda na przetwarzanie danych osobowych
  - Zgoda na marketing
  - Zgoda na cookies
- ✅ **Prawa użytkowników:**
  - Prawo do dostępu do danych
  - Prawo do usunięcia danych
  - Prawo do przenoszenia danych
  - Prawo do sprzeciwu
- ✅ **Polityka cookies:**
  - Jakie cookies są używane
  - Cel użycia cookies
  - Jak zarządzać cookies
- ✅ **Eksport danych:**
  - Możliwość pobrania swoich danych
  - Format JSON/CSV
  - Endpoint: `/api/rodo/export`

### Techniczne:
- **Typ:** Static HTML
- **Backend:** Flask API (`/api/rodo/*`)
- **Compliance:** RODO/GDPR ✅

---

## 📊 Podsumowanie

| # | Endpoint | Status | Typ | Autoryzacja |
|---|----------|--------|-----|-------------|
| 1 | `/static/chatbot.html` | ✅ | Static | Brak |
| 2 | `/static/dashboard.html` | ✅ | Static | API Key |
| 3 | `/admin` | ✅ | Template | API Key |
| 4 | `/docs` | ✅ 200 | Swagger | Brak |
| 5 | `/api/chatbot/health` | ✅ | API | Brak |
| 6 | `/static/widget-demo.html` | ✅ | Static | Brak |
| 7 | `/qualification` | ✅ 200 | Template | Brak |
| 8 | `/static/polityka-prywatnosci.html` | ✅ | Static | Brak |

---

## 🔐 Autoryzacja

### API Key Authentication
Większość endpointów API wymaga nagłówka:
```
X-API-KEY: your_api_key_here
```

### Publiczne Endpointy (bez autoryzacji):
- `/static/*` - Wszystkie pliki statyczne
- `/api/chatbot/health` - Health check
- `/docs` - Swagger documentation
- `/qualification` - Formularz kwalifikacyjny

### Chronione Endpointy (wymagają API Key):
- `/api/leads/*` - Zarządzanie leadami
- `/api/analytics/*` - Analityka
- `/api/admin/*` - Operacje administracyjne
- `/api/backup/*` - Backup management
- `/api/migration/*` - Migracje bazy danych

---

## 🚀 Szybki Start

1. **Dla klientów:** Użyj [`/static/chatbot.html`](https://glass-core-467907-e9.ey.r.appspot.com/static/chatbot.html)
2. **Dla adminów:** Użyj [`/static/dashboard.html`](https://glass-core-467907-e9.ey.r.appspot.com/static/dashboard.html)
3. **Dla developerów:** Sprawdź [`/docs`](https://glass-core-467907-e9.ey.r.appspot.com/docs)
4. **Dla monitoringu:** Sprawdź [`/api/chatbot/health`](https://glass-core-467907-e9.ey.r.appspot.com/api/chatbot/health)

---

## ✅ Weryfikacja Linków

**Data weryfikacji:** 2025-12-11 (ostatnia aktualizacja)

| # | Endpoint | Status HTTP | Status |
|---|----------|-------------|--------|
| 1 | `/static/chatbot.html` | 200 | ✅ Działa |
| 2 | `/static/dashboard.html` | 200 | ✅ Działa |
| 3 | `/admin` | 302 | ✅ Działa (redirect) |
| 4 | `/docs` | 200 | ✅ Działa |
| 5 | `/api/chatbot/health` | 200 | ✅ Działa |
| 6 | `/static/widget-demo.html` | 200 | ✅ Działa |
| 7 | `/qualification` | 200 | ✅ Działa |
| 8 | `/static/polityka-prywatnosci.html` | 200 | ✅ Działa |

### ✅ Wszystko Naprawione!

**Wykonane naprawy:**
- ✅ Dodano brakujące pliki HTML do `src/static/`
- ✅ Naprawiono route `/admin` (redirect do `/admin/dashboard`)
- ✅ Dodano `flask-limiter` do requirements
- ✅ Dodano `pybreaker` do requirements
- ✅ Naprawiono opcjonalny import `websocket_service`

**Status:** 🟢 **WSZYSTKIE LINKI DZIAŁAJĄ!**

---

**Ostatnia aktualizacja:** 2025-12-11  
**Ostatnia weryfikacja linków:** 2025-12-11  
**Wersja API:** 2.3  
**Status Produkcji:** 🟢 **WSZYSTKO DZIAŁA!**

**Wszystkie 8 linków działają poprawnie:**
- ✅ Health Check: 200
- ✅ Chatbot: 200
- ✅ Dashboard: 200
- ✅ Admin: 302 (redirect)
- ✅ Docs (Swagger): 200
- ✅ Widget Demo: 200
- ✅ Qualification: 200
- ✅ Polityka Prywatności: 200

**Wykonane naprawy:**
- ✅ Dodano brakujące pliki HTML
- ✅ Naprawiono route `/admin`
- ✅ Dodano brakujące zależności (flask-limiter, pybreaker)
- ✅ Naprawiono opcjonalny import websocket_service

