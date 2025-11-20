#!/usr/bin/env python3
"""
Główny plik aplikacji dla Google App Engine
"""


import os
import sys

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

# Dodanie ścieżki do modułów
sys.path.insert(0, os.path.dirname(__file__))

# Inicjalizacja Sentry (monitoring błędów)
SENTRY_DSN = os.getenv("SENTRY_DSN", "")
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[FlaskIntegration()],
        traces_sample_rate=1.0,
        environment=os.getenv("ENV", "development"),
    )
    print("✅ Sentry monitoring enabled")
else:
    print("⚠️  Sentry DSN not set – monitoring wyłączony")

# Import aplikacji Flask
from src.main import app

# Dla App Engine, aplikacja musi być dostępna jako 'app'
if __name__ == "__main__":
    # Dla lokalnego uruchomienia
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)), debug=False)
