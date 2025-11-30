# NovaHouse Chatbot – Backup Automation

## Automated Backup
- Backup script runs every 2 weeks (cron)
- Database dump is encrypted with GPG
- Encrypted backup is pushed to Git
- Telegram alerts for success/failure

## Security
- GPG encryption (RSA 3072, passphrase protected)
- Only .gpg files are versioned
- Backup key info: see `backups/automated/gpg_key_info.txt`

## Cron setup
See `backups/automated/cron_backup_example.txt` for ready-to-use cron entry.

## Manual backup
- Trigger via admin dashboard (button)

## Restore backup
- Decrypt with:
  ```sh
  gpg --output db_backup_decrypted.sql --decrypt db_backup_YYYY-MM-DD_HH-MM-SS.sql.gpg
  ```
- Restore to PostgreSQL:
  ```sh
  psql -U user -d dbname -f db_backup_decrypted.sql
  ```

## Automation & Monitoring
- Daily Telegram alert test (script + cron)
- Regular decryption and restoration test of backups
- Backup and alert status visible in the admin panel

## Checklist
- [x] Backup encrypted and versioned
- [x] Decryption and restoration test
- [x] Automatic Telegram alert tests
- [x] Error notifications
