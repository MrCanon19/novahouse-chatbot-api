from src.utils.telegram_alert import send_telegram_alert


def main():
    try:
        send_telegram_alert("Codzienny test alertu Telegram: OK")
    except Exception as e:
        # Jeśli alert nie przejdzie, wyślij powiadomienie na maila lub loguj
        with open("/tmp/telegram_alert_error.log", "a") as f:
            f.write(f"Telegram alert failed: {e}\n")
        # Możesz tu dodać integrację z innym systemem powiadomień


if __name__ == "__main__":
    main()
