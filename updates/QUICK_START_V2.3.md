# ⚡ Quick Start - NovaHouse Chatbot API v2.3

## 🚀 5-Minute Setup

### 1. Instalacja Dependencji
```bash
cd novahouse-chatbot-api
pip3 install -r requirements.txt
```

### 2. Konfiguracja (opcjonalna)

Utwórz `.env` (wszystkie zmienne opcjonalne z fallback):

```bash
# Database
DATABASE_URL=postgresql://user:pass@localhost/novahouse

# Redis (fallback: in-memory cache)
REDIS_URL=redis://localhost:6379/0

# Email (dla powiadomień)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=bot@novahouse.pl
SMTP_PASSWORD=your_app_password

# Twilio SMS (fallback: email-only)
TWILIO_ACCOUNT_SID=ACxxxxx
TWILIO_AUTH_TOKEN=xxxxx
TWILIO_PHONE_NUMBER=+48XXXXXXXXX

# Google Cloud Storage (fallback: local storage)
USE_CLOUD_STORAGE=false
GCS_BUCKET_NAME=novahouse-uploads
UPLOAD_FOLDER=/tmp/uploads
```

### 3. Uruchom
```bash
python3 src/main.py
```

✅ Aplikacja dostępna na: http://localhost:8080

---

## 📋 Testowanie Nowych Funkcji v2.3

### 1️⃣ WebSocket (Real-time Chat)

**HTML Client:**
```html
<script src="https://cdn.socket.io/4.5.4/socket.io.min.js"></script>
<script>
const socket = io('http://localhost:8080');

socket.on('connect', () => {
    console.log('✅ Connected:', socket.id);

    // Join admin room
    socket.emit('join', {room: 'admin'});
});

// Listen for new leads
socket.on('new_lead', (data) => {
    console.log('🎯 New Lead:', data);
});

// Send chat message
socket.emit('chat_message', {
    session_id: 'test123',
    message: 'Hello from WebSocket!'
});
</script>
```

**Test w terminalu:**
```bash
# Install socket.io-client (Node.js)
npm install -g socket.io-client

# Test connection
node -e "
const io = require('socket.io-client');
const socket = io('http://localhost:8080');
socket.on('connect', () => {
    console.log('Connected:', socket.id);
    socket.emit('ping');
});
"
```

---

### 2️⃣ Advanced Search

```bash
# Full-text search
curl "http://localhost:8080/api/search?q=projekt&type=portfolio&limit=5"

# Autocomplete
curl "http://localhost:8080/api/search/suggest?q=projek"

# Search stats
curl "http://localhost:8080/api/search/stats"

# Rebuild index
curl -X POST "http://localhost:8080/api/search/reindex"
```

**Response:**
```json
{
  "success": true,
  "results": [
    {
      "id": "portfolio_3",
      "title": "Apartament w Warszawie",
      "score": 0.95,
      "type": "portfolio"
    }
  ]
}
```

---

### 3️⃣ File Upload

**Single Image:**
```bash
curl -X POST http://localhost:8080/api/upload/image \
  -F "file=@room_photo.jpg" \
  -F "folder=room-photos" \
  -F "variants=true"
```

**Response:**
```json
{
  "success": true,
  "data": {
    "original": {
      "url": "/uploads/room-photos/room_photo_20250115_abc123.jpg",
      "size": 245678
    },
    "thumbnail": {
      "url": "/uploads/room-photos/room_photo_20250115_abc123_thumb.jpg",
      "size": 8912,
      "dimensions": "150x150"
    },
    "medium": {
      "url": "/uploads/room-photos/room_photo_20250115_abc123_medium.jpg",
      "size": 45678,
      "dimensions": "800x800"
    },
    "large": {
      "url": "/uploads/room-photos/room_photo_20250115_abc123_large.jpg",
      "size": 123456,
      "dimensions": "1920x1920"
    }
  }
}
```

**Multiple Images:**
```bash
curl -X POST http://localhost:8080/api/upload/multiple \
  -F "files[]=@photo1.jpg" \
  -F "files[]=@photo2.jpg" \
  -F "folder=gallery"
```

---

### 4️⃣ Dashboard Widgets

```bash
# Summary metrics (last 30 days)
curl "http://localhost:8080/api/widgets/metrics/summary?days=30"

# Timeline data for charts
curl "http://localhost:8080/api/widgets/metrics/timeline?days=7"

# Top intents
curl "http://localhost:8080/api/widgets/top/intents?days=30"

# Active sessions
curl "http://localhost:8080/api/widgets/active/sessions"

# Satisfaction scores
curl "http://localhost:8080/api/widgets/satisfaction/scores"
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
    "conversion_rate": 3.65
  }
}
```

---

### 5️⃣ Appointment Reminders

**Python:**
```python
from src.services.reminder_service import reminder_service
from datetime import datetime, timedelta

# Send reminder now
reminder_service.send_reminder(
    name="Jan Kowalski",
    email="jan@example.com",
    phone="+48123456789",
    appointment_date=datetime.now() + timedelta(days=1),
    package="Premium",
    channels=['email', 'sms']
)

# Schedule for later
reminder_service.schedule_reminder(
    booking_id=123,
    reminder_time=datetime.now() + timedelta(hours=2),
    channels=['email']
)
```

---

### 6️⃣ Backup & Export

```bash
# Create full backup (JSON)
curl -X POST http://localhost:8080/api/backup/export \
  -H "Content-Type: application/json" \
  -d '{"format": "json"}'

# List backups
curl "http://localhost:8080/api/backup/list"

# RODO: Export user data
curl -X POST http://localhost:8080/api/rodo/export \
  -H "Content-Type: application/json" \
  -d '{"user_identifier": "user@example.com"}'

# RODO: Delete user data
curl -X POST http://localhost:8080/api/rodo/delete \
  -H "Content-Type: application/json" \
  -d '{
    "user_identifier": "user@example.com",
    "confirm": true
  }'
```

---

### 7️⃣ Redis Caching

**Python:**
```python
from src.services.redis_service import redis_cache, cached_redis

# Manual caching
redis_cache.set('user_123', user_data, ttl=3600)
user_data = redis_cache.get('user_123')

# Decorator
@cached_redis(ttl=300)  # Cache for 5 minutes
def get_expensive_data():
    return slow_database_query()

# Cache invalidation
redis_cache.delete('user_123')
redis_cache.flush_pattern('user_*')

# Stats
stats = redis_cache.get_stats()
print(stats)  # {'total_keys': 45, 'memory_used': '2.5MB'}
```

---

## 🎯 Przykładowe Scenariusze

### Scenario 1: Real-time Admin Dashboard

```javascript
// Connect WebSocket
const socket = io('http://localhost:8080');

// Join admin room
socket.emit('join', {room: 'admin'});

// Update dashboard on new lead
socket.on('new_lead', async (lead) => {
    // Show notification
    showToast(`Nowy lead: ${lead.name}`);

    // Refresh metrics
    const metrics = await fetch('/api/widgets/metrics/summary').then(r => r.json());
    updateDashboard(metrics.data);
});

// Update charts in real-time
socket.on('analytics_update', (data) => {
    updateChart('conversionsChart', data.timeline);
});
```

### Scenario 2: Image Gallery with Upload

```javascript
// Upload room photos
const uploadForm = document.getElementById('uploadForm');
uploadForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData();
    const files = document.getElementById('fileInput').files;

    for (let file of files) {
        formData.append('files[]', file);
    }
    formData.append('folder', 'room-gallery');

    const result = await fetch('/api/upload/multiple', {
        method: 'POST',
        body: formData
    }).then(r => r.json());

    // Display thumbnails
    result.results.forEach(upload => {
        if (upload.success) {
            addImageToGallery(upload.data.thumbnail.url);
        }
    });
});
```

### Scenario 3: Search Bar with Autocomplete

```javascript
const searchInput = document.getElementById('searchInput');
let debounceTimer;

// Autocomplete
searchInput.addEventListener('input', (e) => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(async () => {
        const query = e.target.value;
        if (query.length < 2) return;

        const suggestions = await fetch(
            `/api/search/suggest?q=${encodeURIComponent(query)}`
        ).then(r => r.json());

        showSuggestions(suggestions.suggestions);
    }, 300);
});

// Full search
searchInput.addEventListener('keypress', async (e) => {
    if (e.key === 'Enter') {
        const results = await fetch(
            `/api/search?q=${encodeURIComponent(e.target.value)}&limit=10`
        ).then(r => r.json());

        displaySearchResults(results.results);
    }
});
```

---

## 🔧 Troubleshooting

### Redis nie działa?
✅ **Fallback automatyczny** - aplikacja używa in-memory cache

```bash
# Opcjonalnie zainstaluj Redis
brew install redis  # macOS
sudo apt install redis  # Linux

# Uruchom
redis-server
```

### WebSocket nie łączy?
Sprawdź CORS i użyj Socket.IO v4+:
```bash
npm install socket.io-client@4.5.4
```

### Twilio SMS nie działa?
✅ **Fallback automatyczny** - wysyła tylko email

### Pillow błąd instalacji?
Użyj nowszej wersji:
```bash
pip3 install Pillow==11.1.0
```

### Search index pusty?
Rebuild:
```bash
curl -X POST http://localhost:8080/api/search/reindex
```

---

## 📚 Następne Kroki

1. **Swagger Docs:** http://localhost:8080/docs
2. **Admin Dashboard:** http://localhost:8080/admin
3. **Full Guide:** `RELEASE_NOTES_V2.3.md`
4. **RODO Guide:** `README_RODO.md`

---

## 🎉 Gotowe!

Wszystkie 7 nowych funkcji v2.3 działają! 🚀

Pytania? Issues: https://github.com/novahouse/chatbot-api/issues
