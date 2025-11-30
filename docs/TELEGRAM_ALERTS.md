# NovaHouse Chatbot – Telegram Alerts

## What is monitored?
- Backup success/failure
- Deployment errors
- Critical system errors

## How it works
- Telegram bot sends alerts to admin group
- Integrated in backup and deploy scripts
- Uses `src/utils/telegram_alert.py`

## Setup
1. Create Telegram bot via BotFather
2. Get bot token and chat ID
3. Set environment variables:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`
4. Test with:
   ```sh
   python3 -c "from src.utils.telegram_alert import send_telegram_alert; send_telegram_alert('Test alert!')"
   ```

## Example alert
```
Backup bazy danych (szyfrowany) wysłany na Git: backups/automated/db_backup_YYYY-MM-DD_HH-MM-SS.sql.gpg
```
