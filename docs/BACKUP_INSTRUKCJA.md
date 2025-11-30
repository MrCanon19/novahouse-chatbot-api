# Automatyczne backupy bazy danych i logów

System backupów wykorzystuje narzędzia wbudowane w GCP (Cloud SQL, Cloud Storage) oraz lokalny backup na SFTP/iCloud.

## Backup bazy danych (Cloud SQL)
- Codzienny automatyczny snapshot bazy przez GCP (ustaw w panelu Cloud SQL → Backups).
- Dodatkowo: skrypt do lokalnego dumpa bazy (np. `pg_dump` lub `mysqldump`) i wysyłka na SFTP/iCloud.

## Backup logów (Cloud Storage)
- Logi aplikacji są automatycznie przesyłane do Cloud Storage.
- Możesz ustawić bucket z wersjonowaniem i automatycznym usuwaniem starych logów.

## Przykładowy skrypt dumpa bazy (PostgreSQL)

```bash
#!/bin/bash
set -e
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
pg_dump $DB_URL > /backups/automated/db_backup_$DATE.sql
# Wysyłka na SFTP/iCloud
# sftp user@host:/remote/path <<< $'put /backups/automated/db_backup_$DATE.sql'
```

## Bezpieczeństwo
- Backupy są szyfrowane i dostępne tylko dla administratorów.
- Automatyczne powiadomienia o nieudanym backupie (można dodać alert Telegram).

## Odzyskiwanie
- Backupy można przywrócić przez panel GCP lub ręcznie z pliku dumpa.

Szczegóły konfiguracji znajdziesz w dokumentacji GCP/AWS/iCloud.
