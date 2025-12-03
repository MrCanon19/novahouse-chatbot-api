#!/usr/bin/env python3
"""
Secret Rotation Monitoring Script
Sprawdza wiek sekretów GitHub i alarmuje jeśli wymagają rotacji

Uruchamiane przez cron co tydzień:
0 9 * * 1 cd /path/to/project && python scripts/check_secret_expiration.py
"""

import os
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def check_github_secrets_age():
    """
    Sprawdza wiek sekretów GitHub poprzez próbę ich użycia
    Zwraca listę sekretów wymagających rotacji
    """
    secrets_to_check = [
        "OPENAI_API_KEY",
        "MONDAY_API_KEY",
        "POSTGRES_PASSWORD",
        "SECRET_KEY",
        "API_KEY",
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_CHAT_ID",
        "SENTRY_DSN",
        "ZENCAL_API_KEY",
        "GOOGLE_MAPS_API_KEY",
    ]

    warnings = []
    errors = []

    # Sprawdź czy sekrety są skonfigurowane
    missing_secrets = []
    for secret_name in secrets_to_check:
        value = os.getenv(secret_name)
        if not value:
            missing_secrets.append(secret_name)

    if missing_secrets:
        warnings.append(f"⚠️  Brakujące sekrety: {', '.join(missing_secrets)}")

    # Testuj połączenia z API (opcjonalnie)
    try:
        # Test OpenAI API
        openai_key = os.getenv("OPENAI_API_KEY")
        if openai_key:
            try:
                from openai import OpenAI

                client = OpenAI(api_key=openai_key)
                # Prosty test - lista modeli
                client.models.list()
                print("✅ OpenAI API Key: Valid")
            except Exception as e:
                errors.append(f"❌ OpenAI API Key: Invalid or expired - {str(e)[:100]}")
    except ImportError:
        warnings.append("⚠️  openai package not installed - skipping API test")

    try:
        # Test Monday.com API
        monday_key = os.getenv("MONDAY_API_KEY")
        if monday_key:
            import requests

            headers = {"Authorization": monday_key, "API-Version": "2024-01"}
            response = requests.post(
                "https://api.monday.com/v2",
                headers=headers,
                json={"query": "{ me { id } }"},
                timeout=5,
            )
            if response.status_code == 200:
                print("✅ Monday.com API Key: Valid")
            else:
                errors.append(
                    f"❌ Monday.com API Key: Invalid or expired - HTTP {response.status_code}"
                )
    except Exception as e:
        warnings.append(f"⚠️  Monday.com API test failed: {str(e)[:100]}")

    try:
        # Test PostgreSQL connection
        postgres_host = os.getenv("POSTGRES_HOST")
        postgres_password = os.getenv("POSTGRES_PASSWORD")
        if postgres_host and postgres_password:
            import psycopg2

            try:
                conn = psycopg2.connect(
                    host=postgres_host,
                    database=os.getenv("POSTGRES_DB", "chatbot"),
                    user=os.getenv("POSTGRES_USER", "postgres"),
                    password=postgres_password,
                    connect_timeout=5,
                )
                conn.close()
                print("✅ PostgreSQL Password: Valid")
            except Exception as e:
                errors.append(f"❌ PostgreSQL Password: Invalid - {str(e)[:100]}")
    except ImportError:
        warnings.append("⚠️  psycopg2 not installed - skipping PostgreSQL test")

    return warnings, errors


def send_telegram_alert(message: str):
    """Wyślij alert na Telegram"""
    try:
        import requests

        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        chat_id = os.getenv("TELEGRAM_CHAT_ID")

        if not bot_token or not chat_id:
            print("⚠️  TELEGRAM_BOT_TOKEN lub TELEGRAM_CHAT_ID not configured")
            return False

        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}

        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            print("✅ Telegram alert sent successfully")
            return True
        else:
            print(f"❌ Telegram alert failed: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Telegram alert error: {e}")
        return False


def main():
    """Main function"""
    print("=" * 60)
    print("🔐 Secret Rotation Monitoring")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    warnings, errors = check_github_secrets_age()

    # Podsumowanie
    print("\n" + "=" * 60)
    if errors:
        print(f"❌ CRITICAL: {len(errors)} secret(s) invalid or expired!")
        for error in errors:
            print(error)

        # Wyślij alert na Telegram
        alert_message = f"🚨 *Secret Rotation Alert*\n\n{len(errors)} secret(s) require immediate attention:\n\n"
        alert_message += "\n".join(errors)
        send_telegram_alert(alert_message)

        sys.exit(1)  # Exit with error code

    elif warnings:
        print(f"⚠️  {len(warnings)} warning(s):")
        for warning in warnings:
            print(warning)
        sys.exit(0)  # Exit ok with warnings

    else:
        print("✅ All secrets valid!")
        sys.exit(0)


if __name__ == "__main__":
    main()
