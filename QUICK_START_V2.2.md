# 🚀 NovaHouse Chatbot v2.2 - Quick Start Guide

## ✅ Co zostało zainstalowane?

### 📦 Nowe zależności (już zainstalowane!)
- ✅ **PyYAML 6.0.1** - Parser OpenAPI/Swagger
- ✅ **langdetect 1.0.9** - Automatyczna detekcja języka

### 🎉 Nowe funkcje
1. **Email Notifications** - Automatyczne powiadomienia
2. **Admin Dashboard** - Zaawansowane filtrowanie i CSV export
3. **Rate Limiting** - Ochrona przed nadużyciami (100 req/min)
4. **Caching** - Szybsze odpowiedzi FAQ
5. **Swagger Docs** - Interaktywna dokumentacja API
6. **Advanced Analytics** - Sentiment, heatmap, funnel, cohort
7. **A/B Testing** - Eksperymenty z wariantami
8. **Multi-language** - Polski, Angielski, Niemiecki

---

## 🏃 Szybki start (3 minuty)

### Krok 1: Skopiuj .env
```bash
cd /Users/michalmarini/Projects/manus/novahouse-chatbot-api
cp .env.example .env
```

### Krok 2: Edytuj .env (opcjonalnie)
Otwórz `.env` i ustaw (tylko jeśli chcesz używać email):
```bash
# Email (opcjonalnie - dla Gmail)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=twoj-email@gmail.com
SMTP_PASSWORD=haslo-aplikacji-16-znakow
FROM_EMAIL=kontakt@novahouse.pl
ADMIN_EMAIL=kontakt@novahouse.pl
```

**Jak uzyskać hasło aplikacji Gmail:**
1. https://myaccount.google.com/apppasswords
2. Wybierz "Mail" → Generate
3. Skopiuj 16-znakowe hasło

### Krok 3: Uruchom serwer
```bash
python3 src/main.py
```

### Krok 4: Testuj! 🎊
Otwórz w przeglądarce:
- **Widget**: http://localhost:8080
- **Swagger UI**: http://localhost:8080/api/docs
- **Admin Dashboard**: http://localhost:8080/admin
- **Health Check**: http://localhost:8080/health

---

## 📚 Przykłady użycia

### 1️⃣ Email Notifications (automatyczne!)
```bash
# Lead automatically sends 2 emails:
# 1. To admin: "New lead: Jan Kowalski"
# 2. To customer: "Thank you for contacting us"

curl -X POST http://localhost:8080/api/leads \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Jan Kowalski",
    "email": "jan@example.com",
    "phone": "+48123456789",
    "service_type": "renovation"
  }'
```

### 2️⃣ CSV Export
```bash
# Export all leads to CSV
curl -X POST http://localhost:8080/api/leads/export \
  -H "Content-Type: application/json" \
  -d '{}' > leads.csv
```

### 3️⃣ Multi-language Detection
```bash
# Auto-detect language
curl -X POST http://localhost:8080/api/i18n/detect \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello, I need a quote"}'

# Response: {"detected_language": "en"}
```

### 4️⃣ A/B Testing
```bash
# Create experiment
curl -X POST http://localhost:8080/api/ab-testing/experiments \
  -H "X-API-Key: your-key" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Greeting Test",
    "experiment_type": "greeting",
    "variants": [
      {"id": "A", "name": "Control", "content": "Cześć!"},
      {"id": "B", "name": "Test", "content": "Witaj!"}
    ]
  }'

# Start experiment
curl -X POST http://localhost:8080/api/ab-testing/experiments/1/start \
  -H "X-API-Key: your-key"
```

### 5️⃣ Advanced Analytics
```bash
# Activity heatmap (24h x 7 days)
curl http://localhost:8080/api/analytics/advanced/heatmap?days=30 \
  -H "X-API-Key: your-key"

# Conversion funnel
curl http://localhost:8080/api/analytics/advanced/funnel?days=30 \
  -H "X-API-Key: your-key"
```

---

## 🔐 Bezpieczeństwo

### Ustaw API Key (produkcja)
W `.env`:
```bash
API_KEY=twoj-super-tajny-klucz-min-32-znaki
```

Następnie używaj w requestach:
```bash
curl http://localhost:8080/api/leads \
  -H "X-API-Key: twoj-super-tajny-klucz-min-32-znaki"
```

### Rate Limiting
Domyślnie: **100 requestów / 60 sekund**

Headers w odpowiedzi:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1673456789
```

Przekroczenie limitu → **HTTP 429 Too Many Requests**

---

## 📊 Dostępne Endpointy

### Email & Notifications
- ✅ Automatyczne przy: `POST /api/leads`
- ✅ Automatyczne przy: `POST /api/booking/book`

### Admin Dashboard
- `POST /api/leads/filter` - Zaawansowane filtrowanie
- `POST /api/leads/export` - Eksport do CSV
- `POST /api/leads/bulk-update` - Masowe aktualizacje

### Analytics
- `POST /api/analytics/advanced/sentiment` - Analiza sentymentu
- `GET /api/analytics/advanced/heatmap` - Mapa aktywności
- `GET /api/analytics/advanced/funnel` - Funnel konwersji
- `GET /api/analytics/advanced/cohort` - Analiza kohortowa
- `GET /api/analytics/advanced/journey/{id}` - Journey użytkownika

### A/B Testing
- `POST /api/ab-testing/experiments` - Utwórz eksperyment
- `POST /api/ab-testing/experiments/{id}/start` - Start
- `POST /api/ab-testing/experiments/{id}/stop` - Stop
- `GET /api/ab-testing/experiments/{id}/results` - Wyniki
- `POST /api/ab-testing/assign` - Przypisz wariant
- `POST /api/ab-testing/track/conversion` - Trackuj konwersję

### Multi-language (i18n)
- `POST /api/i18n/detect` - Wykryj język
- `GET /api/i18n/translations/{lang}` - Pobierz tłumaczenia
- `GET /api/i18n/languages` - Lista języków
- `GET /api/i18n/faq/{intent}/{lang}` - FAQ w języku

### Documentation
- `GET /api/docs` - **Swagger UI** (interaktywna dokumentacja)
- `GET /api/docs/redoc` - ReDoc (alternatywna docs)
- `GET /api/docs/spec` - Raw OpenAPI JSON

---

## 🧪 Testy

### Uruchom wszystkie testy
```bash
pytest tests/
```

### Tylko nowe testy
```bash
pytest tests/test_knowledge.py -v
```

### Z coverage
```bash
pytest --cov=src tests/
```

---

## 🚨 Troubleshooting

### Problem: "Nie mogę zainstalować psycopg2"
**Rozwiązanie:** To jest OK! Używasz SQLite lokalnie. PostgreSQL tylko w produkcji.

### Problem: "Brak modułu yaml"
**Rozwiązanie:**
```bash
pip3 install PyYAML==6.0.1
```

### Problem: "langdetect not found"
**Rozwiązanie:**
```bash
pip3 install langdetect==1.0.9
```

### Problem: Email nie działa
**Sprawdź:**
1. Czy ustawiłeś SMTP_* w .env?
2. Czy hasło aplikacji Gmail jest poprawne?
3. Czy włączona 2FA w Google?

**Debug:**
```bash
# Sprawdź logi
tail -f logs/app.log
```

### Problem: Rate limit za niski
**Zwiększ w kodzie:**
```python
@rate_limit(200, 60)  # 200 req/min
def endpoint():
    ...
```

---

## 📈 Monitoring

### Sprawdź metryki
```bash
curl http://localhost:8080/api/analytics/stats
```

### Cache stats
```bash
curl http://localhost:8080/api/analytics/cache-stats
```

### Rate limit status
Sprawdź headers w każdej odpowiedzi:
```
X-RateLimit-Remaining: 95
```

---

## 🚀 Deploy do produkcji

### Google Cloud Platform
```bash
# 1. Ustaw zmienne w app.yaml
gcloud app deploy

# 2. Sprawdź logi
gcloud app logs tail -s default

# 3. Test
curl https://twoja-aplikacja.appspot.com/health
```

### Uwaga dla produkcji:
1. ✅ Ustaw `FLASK_ENV=production`
2. ✅ Ustaw silny `API_KEY`
3. ✅ Skonfiguruj SMTP (SendGrid/Mailgun)
4. ⚠️ Zamień in-memory cache na **Redis**
5. ⚠️ Zamień in-memory rate limiter na **Redis**

---

## 💡 Pro Tips

### 1. Swagger UI to Twój najlepszy przyjaciel
Otwórz http://localhost:8080/api/docs i testuj wszystkie endpointy!

### 2. A/B Testing dla wszystkiego
Test warianty:
- Greeting messages
- CTA buttons
- Email templates
- Chatbot prompts

### 3. Monitoruj conversion funnel
```bash
curl http://localhost:8080/api/analytics/advanced/funnel?days=7
```
Znajdź, gdzie użytkownicy odpadają!

### 4. Multi-language = więcej leadów
Widget automatycznie wykrywa język użytkownika!

### 5. CSV Export = Excel ready
Importuj do Excel/Google Sheets jednym kliknięciem.

---

## 📞 Pomoc

- **Dokumentacja API:** http://localhost:8080/api/docs
- **Release Notes:** `RELEASE_NOTES_V2.2.md`
- **Email:** kontakt@novahouse.pl

---

**Wersja:** 2.2.0 "Enterprise Ready"  
**Data:** 15 stycznia 2025  
**Status:** ✅ Production Ready

🎉 **Gotowe do użycia! Wszystko działa out-of-the-box!**
