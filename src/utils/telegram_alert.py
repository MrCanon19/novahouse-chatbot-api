import os

import requests


def send_telegram_alert(message: str):
    telegram_token = os.getenv("TELEGRAM_BOT_TOKEN")
    telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID", "7319412445")  # Default: NovaHouse monitoring group
    if not telegram_token:
        print("ALERT: TELEGRAM_BOT_TOKEN not configured! Podaj token bota w sekrecie środowiska.")
        return
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    payload = {"chat_id": telegram_chat_id, "text": message}
    try:
        response = requests.post(url, data=payload, timeout=5)
        response.raise_for_status()
        print("[Telegram] Alert sent.")
    except Exception as e:
        print(f"[Telegram] Alert failed: {e}")
