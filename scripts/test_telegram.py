#!/usr/bin/env python3
"""
Test powiadomień Telegram dla backupów NovaHouse
"""
import os
import sys
from datetime import datetime

# Dodaj ścieżkę do src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.utils.telegram_alert import send_telegram_alert


def test_telegram_backup_notification():
    """Test powiadomienia o backupie"""
    print("🧪 Testowanie powiadomień Telegram...")
    print("=" * 60)
    
    # Sprawdź konfigurację
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID", "7319412445")
    
    if not telegram_token:
        print("❌ BŁĄD: TELEGRAM_BOT_TOKEN nie jest ustawiony!")
        print("\nAby ustawić token:")
        print("  export TELEGRAM_BOT_TOKEN='twój_token'")
        print("\nLub dodaj do .env:")
        print("  TELEGRAM_BOT_TOKEN=twój_token")
        return False
    
    print(f"✅ TELEGRAM_BOT_TOKEN: {'*' * 20}...{telegram_token[-4:]}")
    print(f"✅ Telegram Chat ID: {telegram_chat_id}")
    print()
    
    # Test 1: Prosta wiadomość testowa
    print("📤 Test 1: Prosta wiadomość testowa...")
    try:
        send_telegram_alert("🧪 Test powiadomień Telegram - NovaHouse Chatbot\n\nTo jest testowa wiadomość.")
        print("✅ Test 1: Sukces!")
    except Exception as e:
        print(f"❌ Test 1: Błąd - {e}")
        return False
    
    print()
    
    # Test 2: Powiadomienie o sukcesie backupu
    print("📤 Test 2: Powiadomienie o sukcesie backupu...")
    try:
        message = (
            "✅ Backup NovaHouse\n\n"
            f"Backup utworzony pomyślnie!\n"
            f"📁 Lokalizacja: /tmp/backups/backup_20250115_030000.json.gpg\n"
            f"📊 Rozmiar: 2.45 MB\n"
            f"🔐 Typ: zaszyfrowany\n"
            f"🗑️ Usunięto starych backupów: 3\n"
            f"⏰ Czas: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        send_telegram_alert(message)
        print("✅ Test 2: Sukces!")
    except Exception as e:
        print(f"❌ Test 2: Błąd - {e}")
        return False
    
    print()
    
    # Test 3: Powiadomienie o błędzie backupu
    print("📤 Test 3: Powiadomienie o błędzie backupu...")
    try:
        message = (
            "❌ Backup NovaHouse\n\n"
            f"Błąd podczas tworzenia backupu!\n\n"
            f"Błąd: Testowy błąd - nie można utworzyć pliku backupu\n"
            f"⏰ Czas: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        send_telegram_alert(message)
        print("✅ Test 3: Sukces!")
    except Exception as e:
        print(f"❌ Test 3: Błąd - {e}")
        return False
    
    print()
    print("=" * 60)
    print("✅ WSZYSTKIE TESTY ZAKOŃCZONE POMYŚLNIE!")
    print(f"\nSprawdź grupę Telegram ({telegram_chat_id}) - powinny być 3 wiadomości.")
    return True


if __name__ == "__main__":
    success = test_telegram_backup_notification()
    sys.exit(0 if success else 1)

