# 🔧 Instrukcja migracji: Dodanie kolumny email do chat_conversations

## Status
✅ **Aplikacja działa bez kolumny email** - używa fallbacku do `context_data`  
⚠️ **Migracja wymagana** - aby używać bezpośrednio kolumny email dla lepszej wydajności

---

## 🚀 Opcja 1: Przez API Endpoint (REKOMENDOWANE)

### Krok 1: Sprawdź dostępność aplikacji
```bash
curl https://glass-core-467907-e9.ey.r.appspot.com/api/health
```

### Krok 2: Uruchom migrację przez API
```bash
curl -X POST \
  https://glass-core-467907-e9.ey.r.appspot.com/api/migration/create-dead-letter-queue \
  -H "X-API-KEY: V=iqRX16Zlp2TE+Hpz9pnT42it-L75SB" \
  -H "Content-Type: application/json"
```

**Odpowiedź sukcesu:**
```json
{
  "success": true,
  "message": "✅ Dead-letter queue and indexes created",
  "tables": ["dead_letter_queue"],
  "indexes": [
    "idx_dlq_status_created",
    "idx_dlq_created",
    "idx_chat_conversations_email"
  ]
}
```

---

## 🛠️ Opcja 2: Bezpośrednio na GAE (gdy API niedostępne)

### Krok 1: Połącz się z instancją GAE
```bash
gcloud app instances ssh INSTANCE_ID --service default --version VERSION_ID
```

### Krok 2: Uruchom migrację w kontenerze
```bash
# W kontenerze GAE
cd /workspace
python3 migrations/add_email_column_standalone.py
```

**Lub użyj skryptu pomocniczego:**
```bash
python3 migrations/run_email_migration.py
```

---

## 📋 Opcja 3: Przez Cloud SQL Proxy (lokalnie)

### Krok 1: Zainstaluj Cloud SQL Proxy
```bash
# macOS
brew install cloud-sql-proxy

# Lub pobierz binarkę:
# https://cloud.google.com/sql/docs/postgres/sql-proxy
```

### Krok 2: Uruchom proxy
```bash
cloud-sql-proxy glass-core-467907-e9:europe-west1:novahouse-chatbot-db
```

### Krok 3: Uruchom migrację (w nowym terminalu)
```bash
export DATABASE_URL="postgresql://chatbot_user:NovaH0use2025!DB@127.0.0.1:5432/chatbot"
python3 migrations/add_email_column_standalone.py
```

---

## ✅ Weryfikacja migracji

### Sprawdź czy kolumna istnieje:
```sql
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'chat_conversations' 
AND column_name = 'email';
```

### Sprawdź indeks:
```sql
SELECT indexname, indexdef 
FROM pg_indexes 
WHERE tablename = 'chat_conversations' 
AND indexname LIKE '%email%';
```

### Sprawdź zmigrowane dane:
```sql
SELECT COUNT(*) as total,
       COUNT(email) as with_email_column,
       COUNT(*) - COUNT(email) as without_email
FROM chat_conversations;
```

---

## 🔍 Co robi migracja?

1. **Dodaje kolumnę `email VARCHAR(255)`** do tabeli `chat_conversations`
2. **Tworzy indeks** `idx_chat_conversations_email` dla szybkich wyszukiwań
3. **Migruje istniejące dane** z `context_data::json->>'email'` do kolumny `email`
4. **Jest bezpieczna** - sprawdza czy kolumna już istnieje przed dodaniem

---

## ⚠️ Uwagi

- **Migracja jest idempotentna** - można uruchomić wielokrotnie bez szkody
- **Aplikacja działa bez kolumny** - używa fallbacku do `context_data`
- **Po migracji** aplikacja będzie używać bezpośrednio kolumny `email` dla lepszej wydajności
- **Nie wymaga downtime** - można uruchomić podczas działania aplikacji

---

## 📞 Wsparcie

Jeśli migracja nie powiedzie się:
1. Sprawdź logi aplikacji w GCP Console
2. Sprawdź czy endpoint `/api/migration/create-dead-letter-queue` jest dostępny
3. Sprawdź czy API_KEY jest poprawny w `app.yaml`

