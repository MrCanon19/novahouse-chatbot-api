# Integracja Booksy - RUNDA 3

## 🎯 Cel
Integracja z systemem rezerwacji Booksy umożliwia klientom rezerwowanie konsultacji z ekspertami NovaHouse bezpośrednio z chatbota.

---

## ✅ Co Zrobiono

### 1. **Booksy Client** (`src/integrations/booksy_client.py`)
- ✅ Klasa `BooksynClient` z metodami:
  - `test_connection()` - Sprawdzenie połączenia z API Booksy
  - `get_services()` - Pobranie dostępnych usług
  - `get_staff()` - Pobranie listy pracowników
  - `get_available_slots()` - Pobranie dostępnych termów
  - `create_booking()` - Utworzenie rezerwacji
  - `cancel_booking()` - Anulowanie rezerwacji

### 2. **Booking Routes** (`src/routes/booking.py`)
- ✅ Nowe endpointy:
  - `GET /api/booking/services` - Lista dostępnych usług
  - `GET /api/booking/staff` - Lista pracowników
  - `GET /api/booking/available-slots` - Dostępne terminy
  - `POST /api/booking/create` - Utworzenie rezerwacji
  - `DELETE /api/booking/cancel/<booking_id>` - Anulowanie rezerwacji
  - `POST /api/booking/test` - Test połączenia (wymaga admin key)

### 3. **Main App Update** (`src/main.py`)
- ✅ Zarejestrowano booking blueprint z prefiksem `/api/booking`

---

## 🔧 Zmienne Środowiskowe

Dodaj do `.env`:

```bash
# Booksy
BOOKSY_API_KEY=your_api_key_here
BOOKSY_BUSINESS_ID=your_business_id_here
```

Gdzie:
- `BOOKSY_API_KEY` - Token API z panelu Booksy
- `BOOKSY_BUSINESS_ID` - ID firmy w systemie Booksy

---

## 📊 Struktura Rezerwacji

```json
{
  "client_name": "Jan Kowalski",
  "client_email": "jan@example.com",
  "client_phone": "123456789",
  "service_id": "service_123",
  "start_time": "2025-11-20T14:00:00",
  "staff_id": "staff_456",
  "notes": "Zainteresowany pakietem Premium"
}
```

---

## 🧪 Testowanie

### Test 1: Połączenie z Booksy
```bash
curl -X POST http://localhost:8080/api/booking/test \
  -H "Content-Type: application/json" \
  -H "X-ADMIN-API-KEY: your_admin_key"
```

**Oczekiwana odpowiedź:**
```json
{
  "message": "Booksy connection successful",
  "api_key_set": true,
  "business_id_set": true,
  "services_count": 3,
  "staff_count": 5
}
```

### Test 2: Pobranie dostępnych usług
```bash
curl http://localhost:8080/api/booking/services
```

**Oczekiwana odpowiedź:**
```json
{
  "services": [
    {
      "id": "service_123",
      "name": "Konsultacja (30 min)",
      "duration": 1800,
      "price": 99.00
    },
    {
      "id": "service_456",
      "name": "Pełny projekt (2h)",
      "duration": 7200,
      "price": 299.00
    }
  ],
  "count": 2
}
```

### Test 3: Pobranie dostępnych terminów
```bash
curl "http://localhost:8080/api/booking/available-slots?service_id=service_123&date_from=2025-11-15&date_to=2025-11-30"
```

**Oczekiwana odpowiedź:**
```json
{
  "service_id": "service_123",
  "slots": [
    {
      "start_time": "2025-11-20T10:00:00",
      "end_time": "2025-11-20T10:30:00",
      "staff_id": "staff_456"
    },
    {
      "start_time": "2025-11-20T14:00:00",
      "end_time": "2025-11-20T14:30:00",
      "staff_id": "staff_123"
    }
  ],
  "count": 2
}
```

### Test 4: Utworzenie rezerwacji
```bash
curl -X POST http://localhost:8080/api/booking/create \
  -H "Content-Type: application/json" \
  -d '{
    "client_name": "Jan Kowalski",
    "client_email": "jan@example.com",
    "client_phone": "123456789",
    "service_id": "service_123",
    "start_time": "2025-11-20T14:00:00",
    "staff_id": "staff_456",
    "notes": "Zainteresowany pakietem Premium"
  }'
```

**Oczekiwana odpowiedź:**
```json
{
  "message": "Booking created successfully",
  "booking_id": "booking_789",
  "booking_time": "2025-11-20T14:00:00",
  "client_email": "jan@example.com"
}
```

### Test 5: Anulowanie rezerwacji
```bash
curl -X DELETE http://localhost:8080/api/booking/cancel/booking_789 \
  -H "X-ADMIN-API-KEY: your_admin_key"
```

---

## 🚀 Flow Rezerwacji

```
1. User wstępuje z chatbotem o pakiety
   ↓
2. Chatbot proponuje rezerwację konsultacji
   ↓
3. Frontend pobiera dostępne usługi i terminy
   GET /api/booking/services
   GET /api/booking/available-slots
   ↓
4. User wybiera termin
   ↓
5. Frontend wysyła rezerwację
   POST /api/booking/create
   ↓
6. Backend synchronizuje z Booksy
   ↓
7. Lead status zmienia się na "consultation_booked"
   ↓
8. Potwierdzenie wysyłane na email klienta
```

---

## 🎨 Widget Rezerwacji - Frontend

Przykład integacji w HTML:

```html
<!-- Booking Widget -->
<div id="booking-widget" style="margin-top: 20px; padding: 15px; border: 1px solid #ddd; border-radius: 8px;">
    <h3>📅 Zarezerwuj konsultację</h3>
    
    <label>Wybierz usługę:</label>
    <select id="service-select"></select>
    
    <label>Wybierz termin:</label>
    <select id="slots-select"></select>
    
    <button onclick="confirmBooking()">Zarezerwuj</button>
</div>

<script>
async function loadServices() {
    const response = await fetch('/api/booking/services');
    const data = await response.json();
    
    const select = document.getElementById('service-select');
    data.services.forEach(service => {
        const option = document.createElement('option');
        option.value = service.id;
        option.textContent = `${service.name} - ${service.price} zł`;
        select.appendChild(option);
    });
}

async function loadSlots(serviceId) {
    const response = await fetch(`/api/booking/available-slots?service_id=${serviceId}`);
    const data = await response.json();
    
    const select = document.getElementById('slots-select');
    select.innerHTML = '';
    data.slots.forEach(slot => {
        const option = document.createElement('option');
        option.value = slot.start_time;
        option.textContent = new Date(slot.start_time).toLocaleString('pl-PL');
        select.appendChild(option);
    });
}

async function confirmBooking() {
    const slot = document.getElementById('slots-select').value;
    const service = document.getElementById('service-select').value;
    
    const response = await fetch('/api/booking/create', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            client_name: 'Current User',
            client_email: 'user@example.com',
            client_phone: '123456789',
            service_id: service,
            start_time: slot
        })
    });
    
    const result = await response.json();
    alert(`✅ Rezerwacja potwierdzona! ID: ${result.booking_id}`);
}

document.addEventListener('DOMContentLoaded', () => {
    loadServices();
    document.getElementById('service-select').addEventListener('change', (e) => {
        loadSlots(e.target.value);
    });
});
</script>
```

---

## 🔗 Integracja z Chatbotem

W `src/routes/chatbot.py` dodaj logikę oferowania rezerwacji:

```python
def get_default_response(message: str) -> str:
    """Get a default response when Gemini is not available"""
    
    message_lower = message.lower()
    
    if any(word in message_lower for word in ['rezerwacja', 'termin', 'umówić', 'spotkanie']):
        return """
🗓️ **Chętnie umówimy Cię na konsultację!**

Dostępne usługi:
- Konsultacja (30 min) - Poznajmy Twoje potrzeby
- Pełny projekt (2h) - Szczegółowy projekt wnętrz

Kliknij przycisk poniżej, aby wybrać termin. ⬇️
"""
    
    # ... rest of default responses
```

---

## 🐛 Troubleshooting

| Problem | Rozwiązanie |
|---------|------------|
| "Booksy not configured" | Sprawdź `BOOKSY_API_KEY` i `BOOKSY_BUSINESS_ID` w env |
| "Failed to create booking" | Sprawdź czy service_id istnieje i termin jest dostępny |
| "No available slots" | Ustaw prawidłowe daty w zapytaniu available-slots |
| CORS error | Sprawdź czy CORS jest włączone w main.py |

---

## 📈 Monitoring

Monitoruj następujące metryki:
- **Booking rate** - Ile osób rezerwuje vs. kolik konwersuje
- **Slot utilization** - Które terminy są najpopularniejsze
- **Cancellation rate** - Ile rezerwacji jest anulowanych
- **Lead to booking conversion** - % leadów które rezerwują

---

## 🔐 Security

- Endpoint `/api/booking/cancel` wymaga `X-ADMIN-API-KEY`
- Booking creation zapisuje się do Lead w bazie - audit trail
- API key przechowywane w zmiennych środowiskowych
- All requests zalogowane

---

## 📋 API Reference

| Endpoint | Metoda | Opis | Wymaga Auth |
|----------|--------|------|-------------|
| `/api/booking/services` | GET | Lista usług | Nie |
| `/api/booking/staff` | GET | Lista pracowników | Nie |
| `/api/booking/available-slots` | GET | Dostępne terminy | Nie |
| `/api/booking/create` | POST | Utworzenie rezerwacji | Nie |
| `/api/booking/cancel/<id>` | DELETE | Anulowanie rezerwacji | Tak |
| `/api/booking/test` | POST | Test połączenia | Tak |

---

**Commit**: `runda3: integracja Booksy - rezerwacje konsultacji`
