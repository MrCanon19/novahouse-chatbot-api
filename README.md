# 🏠 NovaHouse Chatbot API

**Version:** 2.3.0 "Production Ready" 🚀  
AI Chatbot dla NovaHouse - pomoc klientom w wyborze pakietów wykończeniowych.

## 🚀 Live Demo

- **Chatbot:** https://glass-core-467907-e9.ey.r.appspot.com/static/chatbot.html
- **Dashboard:** https://glass-core-467907-e9.ey.r.appspot.com/static/dashboard.html
- **API Docs:** https://glass-core-467907-e9.ey.r.appspot.com/docs
- **Health Check:** https://glass-core-467907-e9.ey.r.appspot.com/api/chatbot/health

## 🛠️ Tech Stack

- **Backend:** Python 3.13, Flask 3.1, SQLAlchemy 2.0
- **Frontend:** HTML/CSS/JavaScript
- **Real-time:** Socket.IO, WebSockets
- **Cache:** Redis (with in-memory fallback)
- **Search:** Whoosh full-text engine
- **Storage:** Google Cloud Storage (with local fallback)
- **Notifications:** Email (SMTP) + SMS (Twilio)
- **Hosting:** Google Cloud App Engine
- **Database:** PostgreSQL / SQLite

## ✨ Features

### Core (v1.0 - v2.2)
- ✅ 17+ FAQ inteligentnych odpowiedzi
- ✅ Email notifications (lead confirmations, booking confirmations)
- ✅ Advanced Analytics & A/B Testing
- ✅ Multi-language support (PL/EN/DE)
- ✅ Admin Dashboard with filters
- ✅ Lead filtering & CSV export
- ✅ Bulk operations (mass status updates)
- ✅ 9 Knowledge API endpoints (portfolio, process, reviews, partners)
- ✅ Session management
- ✅ Responsive design
- ✅ Health monitoring
- ✅ Swagger API Documentation

### New in v2.3 🎉
- ✅ **Redis Integration** - Production-ready caching & rate limiting
- ✅ **WebSocket Support** - Real-time chat & live dashboard updates
- ✅ **File Upload & Optimization** - Multi-size image variants + GCS
- ✅ **Appointment Reminders** - SMS (Twilio) + Email multi-channel
- ✅ **Advanced Search** - Full-text search with fuzzy matching
- ✅ **Dashboard Widgets** - Real-time metrics & interactive charts
- ✅ **Backup & Export** - Automated backups + RODO compliance

## 🚀 Quick Start

### Instalacja lokalna

\`\`\`bash
# Clone repo
git clone https://github.com/MrCanon19/novahouse-chatbot-api.git
cd novahouse-chatbot-api

# Setup venv
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run locally
python3 src/main.py
\`\`\`

Otwórz: http://localhost:8080

### Deploy na GCP

\`\`\`bash
gcloud app deploy app.yaml --quiet
\`\`\`

Zobacz szczegóły w [INSTRUKCJA_WDROZENIA_GCP.md](INSTRUKCJA_WDROZENIA_GCP.md)

## 📁 Struktura Projektu

\`\`\`
novahouse-chatbot-api/
├── main.py                  # Entry point dla App Engine
├── src/
│   ├── main.py              # Główna aplikacja Flask
│   ├── routes/
│   │   ├── chatbot.py       # Endpointy chat
│   │   ├── health.py        # Health check
│   │   └── user.py          # User management
│   ├── models/
│   │   ├── chatbot.py       # Database models
│   │   └── user.py          # User model
│   └── static/
│       ├── chatbot.html     # Interfejs chatbota
│       ├── dashboard.html   # Panel analytics
│       └── index.html       # Landing page
├── app.yaml                 # Konfiguracja GCP
├── requirements.txt         # Python dependencies
└── README.md               # Ten plik
\`\`\`

## 📊 API Endpoints

| Method | Endpoint | Opis |
|--------|----------|------|
| GET | \`/api/chatbot/health\` | Health check |
| POST | \`/api/chatbot/chat\` | Wyślij wiadomość |
| POST | \`/api/chatbot/lead\` | Stwórz lead |
| GET | \`/api/chatbot/conversation/<session_id>\` | Historia konwersacji |
| GET | \`/api/chatbot/intents\` | Lista intencji |
| GET | \`/api/chatbot/entities\` | Lista entities |

## 🔧 Konfiguracja

Kluczowe pliki:
- \`app.yaml\` - Konfiguracja Google App Engine
- \`requirements.txt\` - Python dependencies
- \`.gcloudignore\` - Pliki wykluczane z deployu

## 💰 Koszty

**$0/miesiąc** - Darmowy tier na Google Cloud Platform (App Engine F1 instance)

## 📈 Status

- **Status:** ✅ Live in Production
- **Uptime:** 24/7
- **Version:** 1.0
- **Last Updated:** October 2025

## 📝 Changelog

Zobacz [CHANGELOG.md](CHANGELOG.md) dla historii zmian.

## 🤝 Kontakt

Created by **Michał Marini** for **NovaHouse Sp. z o.o.**

---

**© 2025 NovaHouse. All rights reserved.**
