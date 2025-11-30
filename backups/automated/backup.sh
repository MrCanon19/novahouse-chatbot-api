#!/bin/bash
# NovaHouse Chatbot - Automatic Backup Script
set -e
DATE=$(date +"%Y-%m-%d_%H-%M-%S")
DB_URL=${DB_URL:-"postgres://user:pass@localhost:5432/dbname"}
BACKUP_DIR="$(dirname "$0")"
BACKUP_PATH="$BACKUP_DIR/db_backup_$DATE.sql"
ENCRYPTED_PATH="$BACKUP_DIR/db_backup_$DATE.sql.gpg"
GPG_RECIPIENT="Michał Marini <marini19944@gmail.com>" # Twój nowy klucz GPG
# Instrukcja odszyfrowania backupu:
# gpg --output db_backup_decrypted.sql --decrypt db_backup_YYYY-MM-DD_HH-MM-SS.sql.gpg
GIT_REPO="/Users/michalmarini/Projects/manus/novahouse-chatbot-api/backups/automated/"

# Dump bazy
pg_dump $DB_URL > $BACKUP_PATH

# Szyfrowanie backupu
if gpg --output "$ENCRYPTED_PATH" --encrypt --recipient "$GPG_RECIPIENT" "$BACKUP_PATH"; then
  rm "$BACKUP_PATH"
  echo "✅ Backup zaszyfrowany: $ENCRYPTED_PATH"
else
  echo "❌ Szyfrowanie backupu nie powiodło się!"
  python3 -c "from src.utils.telegram_alert import send_telegram_alert; send_telegram_alert('Błąd szyfrowania backupu bazy danych!')"
  exit 1
fi

# Wysyłka na Git
cd "$GIT_REPO"
git add "$(basename "$ENCRYPTED_PATH")"
git commit -m "Automatyczny backup bazy: $DATE"
git push origin main

if [ $? -eq 0 ]; then
  python3 -c "from src.utils.telegram_alert import send_telegram_alert; send_telegram_alert('Backup bazy danych (szyfrowany) wysłany na Git: $ENCRYPTED_PATH')"
else
  python3 -c "from src.utils.telegram_alert import send_telegram_alert; send_telegram_alert('Błąd wysyłki backupu na Git!')"
fi
