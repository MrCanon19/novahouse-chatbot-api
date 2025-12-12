#!/usr/bin/env python3
"""
Prosty test Telegram - można podać token jako argument
Użycie: python3 scripts/test_telegram_simple.py [TELEGRAM_BOT_TOKEN]
"""
import os
import sys

import requests


def test_telegram(token: str = None):
    """Test powiadomienia Telegram"""
    telegram_token = token or os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID", "7319412445")
    
    if not telegram_token:
        print("❌ BŁĄD: TELEGRAM_BOT_TOKEN nie jest ustawiony!")
        print("\nMożesz podać token jako argument:")
        print("  python3 scripts/test_telegram_simple.py TWÓJ_TOKEN")
        print("\nLub ustaw zmienną środowiskową:")
        print("  export TELEGRAM_BOT_TOKEN='twój_token'")
        return False
    
    print(f"📤 Wysyłanie testowej wiadomości do grupy Telegram...")
    print(f"   Chat ID: {telegram_chat_id}")
    print(f"   Token: {'*' * 20}...{telegram_token[-4:]}")
    print()
    
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    payload = {
        "chat_id": telegram_chat_id,
        "text": "🧪 Test powiadomień Telegram - NovaHouse Chatbot\n\n✅ Jeśli widzisz tę wiadomość, oznacza to że powiadomienia działają poprawnie!"
    }
    
    try:
        response = requests.post(url, data=payload, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        if result.get("ok"):
            print("✅ SUKCES! Wiadomość została wysłana!")
            print(f"   Message ID: {result.get('result', {}).get('message_id')}")
            print("\n📱 Sprawdź grupę Telegram - powinieneś zobaczyć wiadomość testową.")
            return True
        else:
            print(f"❌ Błąd: {result.get('description', 'Unknown error')}")
            return False
            
    except requests.exceptions.HTTPError as e:
        print(f"❌ Błąd HTTP: {e}")
        if e.response.status_code == 401:
            print("   Token jest nieprawidłowy lub został odwołany!")
            try:
                error_detail = e.response.json()
                print(f"   Szczegóły: {error_detail.get('description', 'Unknown')}")
            except:
                pass
        elif e.response.status_code == 400:
            print("   Chat ID jest nieprawidłowy lub bot nie ma dostępu do grupy!")
            try:
                error_detail = e.response.json()
                print(f"   Szczegóły: {error_detail.get('description', 'Unknown')}")
            except:
                pass
        return False
    except Exception as e:
        print(f"❌ Błąd: {e}")
        return False


if __name__ == "__main__":
    # Sprawdź czy token został podany jako argument
    token = sys.argv[1] if len(sys.argv) > 1 else None
    
    success = test_telegram(token)
    sys.exit(0 if success else 1)

