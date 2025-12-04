# 🔧 Fix Dashboard - Database Migration Required

## Problem
Dashboard nie działa przez brakujące kolumny w tabeli `leads`:
- `email_verified`, `email_verification_token`, `email_verified_at`
- `phone_verified`, `phone_verification_code`, `phone_verified_at`
- `assigned_to_user_id`, `assigned_at`, `first_contact_at`, `expected_contact_by`

**Błąd:**
```
(psycopg2.errors.UndefinedColumn) column leads.email_verified does not exist
```

## Rozwiązanie

### Krok 1: Uruchom migrację SQL w GCP Console

1. Otwórz: https://console.cloud.google.com/sql/instances/novahouse-chatbot-db/overview?project=glass-core-467907-e9
2. Kliknij **"OPEN CLOUD SHELL"** (ikona terminala w prawym górnym rogu)
3. Połącz się z bazą:
   ```bash
   gcloud sql connect novahouse-chatbot-db --user=chatbot_user --database=chatbot
   ```
4. Wpisz hasło: `vicNRNoO3TpLZzQ_BkAVbz886dW_J0Yo`

5. Uruchom SQL migration (skopiuj i wklej poniższe):

```sql
-- Migration: Add Lead Verification & Assignment Fields

-- Email verification fields
ALTER TABLE leads ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT FALSE;
ALTER TABLE leads ADD COLUMN IF NOT EXISTS email_verification_token VARCHAR(128);
ALTER TABLE leads ADD COLUMN IF NOT EXISTS email_verified_at TIMESTAMP;

-- Phone verification fields  
ALTER TABLE leads ADD COLUMN IF NOT EXISTS phone_verified BOOLEAN DEFAULT FALSE;
ALTER TABLE leads ADD COLUMN IF NOT EXISTS phone_verification_code VARCHAR(6);
ALTER TABLE leads ADD COLUMN IF NOT EXISTS phone_verified_at TIMESTAMP;

-- Lead assignment fields
ALTER TABLE leads ADD COLUMN IF NOT EXISTS assigned_to_user_id VARCHAR(100);
ALTER TABLE leads ADD COLUMN IF NOT EXISTS assigned_at TIMESTAMP;
ALTER TABLE leads ADD COLUMN IF NOT EXISTS first_contact_at TIMESTAMP;
ALTER TABLE leads ADD COLUMN IF NOT EXISTS expected_contact_by TIMESTAMP;

-- Verify migration
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'leads'
AND column_name IN (
    'email_verified', 'email_verification_token', 'email_verified_at',
    'phone_verified', 'phone_verification_code', 'phone_verified_at',
    'assigned_to_user_id', 'assigned_at', 'first_contact_at', 'expected_contact_by'
)
ORDER BY column_name;
```

### Krok 2: Zweryfikuj wynik

Powinno zwrócić 10 kolumn:
```
           column_name           |       data_type        | is_nullable
---------------------------------+------------------------+-------------
 assigned_at                     | timestamp              | YES
 assigned_to_user_id             | character varying(100) | YES
 email_verification_token        | character varying(128) | YES
 email_verified                  | boolean                | YES
 email_verified_at               | timestamp              | YES
 expected_contact_by             | timestamp              | YES
 first_contact_at                | timestamp              | YES
 phone_verification_code         | character varying(6)   | YES
 phone_verified                  | boolean                | YES
 phone_verified_at               | timestamp              | YES
```

### Krok 3: Restart aplikacji (opcjonalnie)

Aplikacja powinna automatycznie wykryć nowe kolumny, ale jeśli nie działa:

```bash
gcloud app deploy --project=glass-core-467907-e9
```

### Krok 4: Testuj Dashboard

https://glass-core-467907-e9.ey.r.appspot.com/static/dashboard.html

Powinno wyświetlić dane bez błędów.

## Alternatywa: SQL w GCP Console UI

1. Otwórz: https://console.cloud.google.com/sql/instances/novahouse-chatbot-db/query?project=glass-core-467907-e9
2. Wybierz database: `chatbot`
3. Wklej SQL z pliku `migrations/add_lead_verification_fields.sql`
4. Kliknij **RUN**

## Troubleshooting

**Błąd: "relation does not exist"**
- Sprawdź nazwę tabeli: `SELECT tablename FROM pg_tables WHERE schemaname = 'public';`

**Błąd: "permission denied"**
- Użyj użytkownika `chatbot_user` (ma uprawnienia ALTER TABLE)

**Błąd: "already exists"**
- OK! Kolumna już istnieje, pomiń ten krok

## Pliki

- SQL migration: `migrations/add_lead_verification_fields.sql`
- Python script (wymaga Cloud SQL Proxy): `migrations/run_lead_verification_production.py`
- Model: `src/models/chatbot.py` (Lead class)
