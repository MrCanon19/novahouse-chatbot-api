# Integracja Monday.com - RUNDA 2

## 🎯 Cel
Przesyłanie leadów z kwalifikacji chatbota bezpośrednio do Monday.com z bogatymi danymi o preferencjach klienta.

---

## ✅ Co Zrobiono

### 1. **Rozszerzony Monday Client** (`src/integrations/monday_client.py`)
- ✅ Dodane pola dla danych kwalifikacji:
  - `package` - Rekomendowany pakiet (Standard/Premium/Luxury)
  - `confidence` - Procent pewności rekomendacji
  - `property_type` - Typ nieruchomości (Mieszkanie, Dom, etc.)
  - `budget` - Budżet klienta
  - `interior_style` - Styl wnętrz (Minimalistyczny, Nowoczesny, etc.)
  - `status` - Status leada (domyślnie "New Lead")

- ✅ Nowa metoda `create_lead_item_with_qualification()`:
  ```python
  monday.create_lead_item_with_qualification(
      lead_data={'name': 'Jan Kowalski', 'email': 'jan@example.com', 'phone': '123456789'},
      qualification_result={'recommended_package': 'premium', 'confidence': 85.5, 'property_type': 'Dom', ...}
  )
  ```

### 2. **Ulepszona Kwalifikacja** (`src/routes/qualification.py`)
- ✅ Nowe pola kwalifikacyjne (8 pytań zamiast 7):
  - Metraż (Range: 0-40, 41-70, 71+)
  - Budżet (Range: 0-100k, 100k-200k, 200k+)
  - Szybka realizacja (Boolean)
  - Materiały (Choice: Podstawowe, Średnia, Premium, Luksusowe)
  - **Typ nieruchomości** (Choice: Mieszkanie, Dom, Apartamentowiec, Komercyjna)
  - **Styl wnętrz** (Choice: Minimalistyczny, Nowoczesny, Klasyczny, Industrial, Skandynawski)
  - Smart home (Boolean)
  - Konsultacja designera (Boolean)

- ✅ Integracja z Monday w `/api/qualification/submit`:
  - Pobiera dane kwalifikacji ze struktury `qualification_data`
  - Przesyła rozszerzone dane do Monday.com
  - Zapisuje `monday_item_id` do modelu Lead

### 3. **Nowe Pytania Kwalifikacyjne** (`src/knowledge/novahouse_info.py`)
- ✅ Dodane pola `data_field` dla trackowania preferencji:
  - `property_type` - Typ nieruchomości
  - `interior_style` - Preferowany styl wnętrz

---

## 📊 Struktura Danych Przesyłanej do Monday

```json
{
  "name": "Jan Kowalski",
  "email": "jan@example.com",
  "phone": "123456789",
  "message": "Kwalifikacja: premium (85.5% pewności)",
  "recommended_package": "premium",
  "confidence_score": 85.5,
  "property_type": "Dom",
  "budget": "150000",
  "interior_style": "Nowoczesny",
  "status": "New Lead"
}
```

---

## 🔧 Zmienne Środowiskowe

Dodaj do `.env` lub zmiennych systemowych:

```bash
# Monday.com
MONDAY_API_KEY=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
MONDAY_BOARD_ID=123456789

# Opcjonalnie - custom fields w Monday
MONDAY_PACKAGE_COLUMN_ID=status_1
MONDAY_CONFIDENCE_COLUMN_ID=numbers_1
MONDAY_PROPERTY_TYPE_COLUMN_ID=text_1
MONDAY_INTERIOR_STYLE_COLUMN_ID=dropdown_1
```

---

## 🧪 Testowanie

### Test 1: Połączenie z Monday
```bash
curl -X POST http://localhost:8080/api/monday/test \
  -H "Content-Type: application/json" \
  -H "X-ADMIN-API-KEY: your_admin_key"
```

### Test 2: Pełna Kwalifikacja z Monday Sync
```bash
curl -X POST http://localhost:8080/api/qualification/submit \
  -H "Content-Type: application/json" \
  -d '{
    "answers": [
      {"question_id": 1, "answer": "50"},
      {"question_id": 2, "answer": "150000"},
      {"question_id": 3, "answer": "nie"},
      {"question_id": 4, "answer": "Premium"},
      {"question_id": 5, "answer": "Dom"},
      {"question_id": 6, "answer": "Nowoczesny"},
      {"question_id": 7, "answer": "tak"},
      {"question_id": 8, "answer": "tak"}
    ],
    "contact_info": {
      "name": "Jan Kowalski",
      "email": "jan@example.com",
      "phone": "123456789"
    },
    "qualification_data": {
      "property_type": "Dom",
      "budget": "150000",
      "interior_style": "Nowoczesny"
    }
  }'
```

**Oczekiwana odpowiedź:**
```json
{
  "recommendation": {
    "recommended_package": "premium",
    "confidence": 82.3,
    "scores": {...}
  },
  "lead_id": 123,
  "answers_count": 8
}
```

### Test 3: Weryfikacja w Monday
1. Zaloguj się do Monday.com
2. Przejdź na board skonfigurowany w `MONDAY_BOARD_ID`
3. Powinien się pojawić nowy item z:
   - Nazwa: "Jan Kowalski"
   - Email: jan@example.com
   - Package: premium
   - Confidence: 82.3%
   - Status: New Lead

---

## 🎨 Custom Fields w Monday

Aby w pełni skorzystać z integracji, skonfiguruj te kolumny w Monday.com:

| Kolumna | Typ | ID (w kodzie) | Przykład |
|---------|-----|---------------|---------|
| Name | Text | item_name | Jan Kowalski |
| Email | Email | email | jan@example.com |
| Phone | Phone | phone | 123456789 |
| Message | Text | text | Kwalifikacja: premium (85.5%) |
| Package | Dropdown/Status | package | premium |
| Confidence | Number | confidence | 85.5 |
| Property Type | Dropdown | property_type | Dom |
| Budget | Text/Currency | budget | 150000 |
| Interior Style | Dropdown | interior_style | Nowoczesny |
| Status | Status | status | New Lead |

---

## 🚀 Flow Danych

```
1. Użytkownik wypełnia kwestionariusz kwalifikacyjny
   ↓
2. Frontend wysyła POST /api/qualification/submit
   ↓
3. Backend oblicza rekomendację (cual pakiet)
   ↓
4. Jeśli user wpisał email + imię:
   - Tworzy Lead w DB
   - Pobiera dane kwalifikacji z `qualification_data`
   ↓
5. Synchronizuje z Monday.com:
   - Wszystkie dane leada + dane kwalifikacji
   ↓
6. Zwraca rekomendację + lead_id + monday_item_id
```

---

## 🐛 Troubleshooting

| Problem | Rozwiązanie |
|---------|------------|
| "Monday.com not configured" | Sprawdź `MONDAY_API_KEY` i `MONDAY_BOARD_ID` w env |
| "Failed to create Monday.com item" | Sprawdź format JSON w `columnValues` |
| Lead utworzony, ale nie w Monday | Sprawdzenie tokenów Monday i board access |
| Brak custom fields w Monday | Dodaj kolumny ręcznie w Monday lub użyj domyślnych |

---

## 📈 Metryki do Monitorowania

- **Conversion Rate**: Lead z kwalifikacji / All messages
- **Package Distribution**: Ile osób → Standard/Premium/Luxury
- **Confidence Scores**: Średnia pewność rekomendacji
- **Monday Sync Rate**: Leady zsyncone / Całość leadów

---

## 🔗 Powiązane Pliki

- `src/integrations/monday_client.py` - Monday API Client
- `src/routes/qualification.py` - Kwalifikacja + Monday Sync
- `src/knowledge/novahouse_info.py` - QUALIFICATION_QUESTIONS
- `src/models/chatbot.py` - Model Lead (z `monday_item_id`)
- `RUNDY_IMPLEMENTATION.md` - Ogólny plan rundy

---

## ✨ Wdrażanie

```bash
# 1. Ustaw zmienne środowiskowe
export MONDAY_API_KEY="your_api_key"
export MONDAY_BOARD_ID="your_board_id"

# 2. Restart serwera
systemctl restart novahouse-chatbot

# 3. Test
curl -X POST http://localhost:8080/api/qualification/submit \
  -H "Content-Type: application/json" \
  -d '{ ... }'

# 4. Monitoruj logi
tail -f /var/log/novahouse-chatbot/app.log | grep "Monday.com"
```

---

**Commit**: `runda2: integracja Monday.com z danymi kwalifikacji`
