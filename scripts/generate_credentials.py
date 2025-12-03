#!/usr/bin/env python3
"""
Generate new secure credentials for app.yaml
Run this script and copy the output to your app.yaml file
"""

import secrets
import string


def generate_secret_key():
    """Generate Flask SECRET_KEY (64 hex chars)"""
    return secrets.token_hex(32)


def generate_api_key():
    """Generate Admin API_KEY (32 chars alphanumeric + special)"""
    alphabet = string.ascii_letters + string.digits + "-_=+"
    return "".join(secrets.choice(alphabet) for _ in range(32))


def generate_password():
    """Generate PostgreSQL password (32 chars safe for URLs)"""
    # Only alphanumeric + underscore (safe for connection strings)
    alphabet = string.ascii_letters + string.digits + "_"
    return "".join(secrets.choice(alphabet) for _ in range(32))


if __name__ == "__main__":
    print("=" * 70)
    print("🔐 NEW CREDENTIALS GENERATOR")
    print("=" * 70)
    print()
    print("⚠️  CRITICAL: These are NEW credentials!")
    print("⚠️  You MUST update these in:")
    print("   1. app.yaml (local only, NOT in git)")
    print("   2. GCP Cloud SQL (change PostgreSQL password)")
    print("   3. GitHub Secrets (if using CI/CD)")
    print()
    print("=" * 70)
    print()

    print("# Flask Session Key")
    print(f'SECRET_KEY: "{generate_secret_key()}"')
    print()

    print("# Admin API Key")
    print(f'API_KEY: "{generate_api_key()}"')
    print()

    print("# PostgreSQL Password (for DATABASE_URL)")
    db_password = generate_password()
    print(f"PostgreSQL Password: {db_password}")
    print()
    print("UPDATE DATABASE_URL:")
    print(
        f"postgresql://chatbot_user:{db_password}@/chatbot?host=/cloudsql/glass-core-467907-e9:europe-west1:novahouse-chatbot-db"
    )
    print()

    print("=" * 70)
    print("MANUAL ROTATION REQUIRED:")
    print("=" * 70)
    print()
    print("1. OpenAI API Key:")
    print("   → https://platform.openai.com/api-keys")
    print("   → Click 'Create new secret key'")
    print("   → Copy to app.yaml: OPENAI_API_KEY")
    print()
    print("2. Monday.com API Token:")
    print("   → https://monday.com/developers")
    print("   → Generate new token")
    print("   → Copy to app.yaml: MONDAY_API_KEY")
    print()
    print("3. GCP Cloud SQL Password:")
    print("   → gcloud sql users set-password chatbot_user \\")
    print(f"     --instance=novahouse-chatbot-db \\")
    print(f"     --password='{db_password}'")
    print()
    print("=" * 70)
    print("✅ Done! Copy these to app.yaml (NOT in git!)")
    print("=" * 70)
