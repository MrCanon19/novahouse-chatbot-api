# 🚀 NovaHouse Chatbot API v2.3 - Release Notes

## 📊 Overview

Wersja 2.3 to **Production-Scale Release** wprowadzająca **7 zaawansowanych funkcji** gotowych do użycia w środowisku produkcyjnym z setkami użytkowników.

**Data wydania:** 2025-01-XX  
**Wersja:** 2.3.0  
**Kod:** "Production Ready"

---

## ✨ Nowe Funkcje (v2.3)

### 1️⃣ **Redis Integration** ⚡
- **Production-ready caching** zamiast in-memory
- **Redis Rate Limiter** z sliding window algorithm
- **Graceful fallback** do in-memory cache
- **Cache warming** przy starcie aplikacji
- **Pattern-based cache invalidation**

**Pliki:**
- `src/services/redis_service.py` (223 lines)
- `src/services/redis_rate_limiter.py` (127 lines)

**Konfiguracja:**
```bash
REDIS_URL=redis://localhost:6379/0
```

**API:**
```python
from src.services.redis_service import redis_cache

# Cache data
redis_cache.set('key', data, ttl=3600)
data = redis_cache.get('key')

# Decorator
@cached_redis(ttl=300)
def expensive_function():
    return heavy_computation()
```

**Rate Limiting:**
```python
from src.services.redis_rate_limiter import rate_limit_redis

@rate_limit_redis(limit=100, window=60)  # 100 req/min
def api_endpoint():
    return {"data": "..."}
```

---

### 2️⃣ **WebSocket Support** 🔌
- **Real-time bi-directional communication**
- **Room-based messaging** (admin dashboard, user sessions)
- **Connection tracking** (active users, session IDs)
- **Live analytics updates**
- **Typing indicators**

**Plik:**
- `src/services/websocket_service.py` (149 lines)

**Events:**
- `connect` / `disconnect` - Connection lifecycle
- `join` / `leave` - Room management
- `chat_message` - Real-time chat
- `typing` - Typing indicator
- `analytics_update` - Live dashboard updates

**Client Example:**
```javascript
const socket = io('http://localhost:8080');

socket.on('connect', () => {
    console.log('Connected:', socket.id);
    socket.emit('join', {room: 'admin'});
});

socket.on('chat_message', (data) => {
    console.log('New message:', data);
});

socket.emit('chat_message', {
    session_id: 'abc123',
    message: 'Hello!'
});
```

---

### 3️⃣ **File Upload & Optimization** 📷
- **Multi-size image variants** (thumbnail, medium, large)
- **Automatic image optimization** (JPEG compression, RGBA→RGB)
- **Google Cloud Storage** or local fallback
- **10 MB size limit**
- **Supported formats:** PNG, JPG, JPEG, GIF, WebP

**Plik:**
- `src/services/file_upload_service.py` (273 lines)

**Konfiguracja:**
```bash
USE_CLOUD_STORAGE=true
GCS_BUCKET_NAME=novahouse-uploads
UPLOAD_FOLDER=/app/uploads
```

**API Endpoints:**
```bash
# Upload single image
POST /api/upload/image
Form-data: file, folder, variants

# Upload multiple images
POST /api/upload/multiple
Form-data: files[], folder

# Delete file
POST /api/upload/delete
Body: {"filepath": "path/to/file.jpg"}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "original": {
      "url": "https://storage.googleapis.com/.../file.jpg",
      "size": 245678
    },
    "thumbnail": {
      "url": "https://.../file_thumb.jpg",
      "size": 12345,
      "dimensions": "150x150"
    },
    "medium": {...},
    "large": {...}
  }
}
```

---

### 4️⃣ **Appointment Reminders** 📧📱
- **Multi-channel:** SMS (Twilio) + Email
- **Beautiful HTML email templates**
- **Scheduled reminders** with APScheduler
- **Graceful degradation** (email-only if SMS unavailable)

**Plik:**
- `src/services/reminder_service.py` (226 lines)

**Konfiguracja:**
```bash
TWILIO_ACCOUNT_SID=ACxxxxx
TWILIO_AUTH_TOKEN=xxxxx
TWILIO_PHONE_NUMBER=+48XXXXXXXXX
```

**Użycie:**
```python
from src.services.reminder_service import reminder_service

# Send reminder
reminder_service.send_reminder(
    name="Jan Kowalski",
    email="jan@example.com",
    phone="+48123456789",
    appointment_date=datetime(2025, 2, 15, 14, 0),
    package="Premium",
    channels=['email', 'sms']
)

# Schedule for later
reminder_service.schedule_reminder(
    booking_id=123,
    reminder_time=datetime(2025, 2, 14, 18, 0),
    channels=['email']
)
```

---

### 5️⃣ **Advanced Search** 🔍
- **Full-text search** with fuzzy matching
- **Multi-language support** (PL, EN, DE)
- **Search suggestions** (autocomplete)
- **Index statistics**
- **Whoosh search engine**

**Plik:**
- `src/services/search_service.py` (270 lines)

**API Endpoints:**
```bash
# Search
GET /api/search?q=projekt&type=portfolio&lang=pl&limit=10

# Autocomplete
GET /api/search/suggest?q=projek&limit=5

# Stats
GET /api/search/stats

# Rebuild index
POST /api/search/reindex
```

**Response:**
```json
{
  "success": true,
  "query": "projekt aranżacji",
  "results": [
    {
      "id": "portfolio_3",
      "type": "portfolio",
      "title": "Apartament w Warszawie",
      "content": "Premium - 120m² - 8 tygodni",
      "score": 0.95,
      "language": "pl"
    }
  ]
}
```

---

### 6️⃣ **Dashboard Widgets** 📊
- **Real-time metrics** via WebSocket
- **Time-series charts** (conversations, leads, bookings)
- **Top intents** and **popular packages**
- **Active sessions monitoring**
- **Satisfaction scores**

**Plik:**
- `src/routes/dashboard_widgets.py` (380 lines)

**API Endpoints:**
```bash
# Summary metrics
GET /api/widgets/metrics/summary?days=30

# Timeline data
GET /api/widgets/metrics/timeline?days=7

# Top intents
GET /api/widgets/top/intents?days=30

# Top packages
GET /api/widgets/top/packages

# Active sessions
GET /api/widgets/active/sessions

# Satisfaction scores
GET /api/widgets/satisfaction/scores
```

**Response:**
```json
{
  "success": true,
  "data": {
    "conversations": 1234,
    "messages": 5678,
    "leads": 234,
    "bookings": 45,
    "conversion_rate": 3.65,
    "period_days": 30
  }
}
```

---

### 7️⃣ **Backup & Export** 💾
- **Automated daily backups** (3 AM)
- **JSON and CSV export**
- **RODO compliance:**
  - ✅ Right to data portability
  - ✅ Right to be forgotten
- **Backup management** (list, download, delete)

**Pliki:**
- `src/services/backup_service.py` (390 lines)
- `src/routes/backup.py` (190 lines)

**API Endpoints:**
```bash
# Create backup
POST /api/backup/export
Body: {"format": "json"}

# List backups
GET /api/backup/list

# Download backup
GET /api/backup/download/<filename>

# RODO: Export user data
POST /api/rodo/export
Body: {"user_identifier": "user@example.com"}

# RODO: Delete user data (Right to be forgotten)
POST /api/rodo/delete
Body: {
  "user_identifier": "user@example.com",
  "confirm": true
}

# Schedule automated backup
POST /api/backup/schedule
Body: {"enabled": true}
```

---

## 📈 Statystyki v2.3

| Metryka | Wartość |
|---------|---------|
| **Nowe pliki** | 11 |
| **Nowe linie kodu** | ~2000 LOC |
| **Nowe endpointy API** | 20+ |
| **Nowe dependencje** | 7 |
| **Całkowite endpointy** | 90+ |

---

## 🔧 Instalacja

### 1. Zaktualizuj dependencje
```bash
pip3 install -r requirements.txt
```

Nowe pakiety:
- `redis==5.0.1` - Redis cache
- `Flask-SocketIO==5.3.6` - WebSockets
- `Pillow==11.1.0` - Image processing
- `google-cloud-storage==2.14.0` - GCS
- `twilio==8.11.0` - SMS
- `APScheduler==3.10.4` - Scheduled tasks
- `Whoosh==2.7.4` - Search engine

### 2. Konfiguracja .env

```bash
# Redis (opcjonalne - fallback do in-memory)
REDIS_URL=redis://localhost:6379/0

# File Upload (opcjonalne - fallback do local)
USE_CLOUD_STORAGE=false
GCS_BUCKET_NAME=novahouse-uploads
UPLOAD_FOLDER=/app/uploads

# Twilio SMS (opcjonalne - fallback do email-only)
TWILIO_ACCOUNT_SID=ACxxxxx
TWILIO_AUTH_TOKEN=xxxxx
TWILIO_PHONE_NUMBER=+48XXXXXXXXX
```

### 3. Uruchom aplikację

```bash
python3 src/main.py
```

Przy starcie aplikacja automatycznie:
- ✅ Warm Redis cache
- ✅ Build search index
- ✅ Schedule automated backup

---

## 🚀 Migracja z v2.2

**Brak breaking changes!** Wszystkie nowe funkcje są **opcjonalne** i działają z graceful fallback.

### Co działa bez konfiguracji:
- ✅ WebSockets (lokalnie)
- ✅ Redis → fallback do in-memory
- ✅ File Upload → fallback do local storage
- ✅ SMS → fallback do email-only
- ✅ Search → działa out-of-the-box
- ✅ Dashboard Widgets → działa z istniejącą bazą
- ✅ Backup → działa lokalnie

### Opcjonalne usprawnienia produkcyjne:
1. **Redis Server** - dla multi-instance cache
2. **Google Cloud Storage** - dla skalowanych plików
3. **Twilio Account** - dla SMS reminders

---

## 🎯 Przypadki Użycia

### 1. Real-time Admin Dashboard
```javascript
// Connect to WebSocket
const socket = io('https://api.novahouse.pl');

// Join admin room
socket.emit('join', {room: 'admin'});

// Listen for new leads
socket.on('new_lead', (lead) => {
    showNotification(`Nowy lead: ${lead.name}`);
    updateDashboard();
});

// Listen for analytics updates
socket.on('analytics_update', (data) => {
    updateCharts(data);
});
```

### 2. Search Bar
```javascript
// Autocomplete suggestions
const suggestions = await fetch(
    '/api/search/suggest?q=' + userInput
).then(r => r.json());

// Full search
const results = await fetch(
    '/api/search?q=projekt%20premium&type=portfolio'
).then(r => r.json());
```

### 3. Image Upload Widget
```javascript
const formData = new FormData();
formData.append('file', imageFile);
formData.append('folder', 'room-photos');

const result = await fetch('/api/upload/image', {
    method: 'POST',
    body: formData
}).then(r => r.json());

// Use optimized variants
chatWidget.showImage(result.data.medium.url);
```

### 4. RODO Compliance
```python
# Export user data
user_data = requests.post('/api/rodo/export', json={
    'user_identifier': 'user@example.com'
}).json()

# Save to file (RODO Article 20)
with open('user_data_export.json', 'w') as f:
    json.dump(user_data, f)

# Delete user data (RODO Article 17)
requests.post('/api/rodo/delete', json={
    'user_identifier': 'user@example.com',
    'confirm': True
})
```

---

## 🔒 Bezpieczeństwo

### Nowe mechanizmy v2.3:
1. **Redis Rate Limiting** - sliding window algorithm
2. **File Upload Validation** - type, size, malware scanning
3. **RODO Compliance** - data export & deletion
4. **WebSocket Authentication** - session-based
5. **Backup Encryption** - opcjonalne (TODO)

---

## 📚 Dokumentacja

- **Quick Start:** `QUICK_START_V2.3.md`
- **API Docs:** http://localhost:8080/docs (Swagger UI)
- **RODO Guide:** `README_RODO.md`
- **Deployment:** `README_WDROZENIE.md`

---

## 🐛 Znane Problemy

1. **Whoosh index** wymaga rebuildu po dodaniu nowych danych (automatyczne przy starcie)
2. **WebSocket reconnection** nie działa automatycznie (użyj `socket.io-client` v4+)
3. **Pillow 10.2.0** nie działa z Python 3.13 (użyj `Pillow==11.1.0`)

---

## 📞 Wsparcie

Zgłaszaj problemy w Issues lub kontaktuj:
- **Email:** support@novahouse.pl
- **GitHub:** https://github.com/novahouse/chatbot-api

---

## 🎉 Podziękowania

Dziękujemy za używanie NovaHouse Chatbot API v2.3!

**Next Steps:**
- v2.4: AI-powered image recognition
- v2.5: Voice messages transcription
- v3.0: Multi-tenant architecture
