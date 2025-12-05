#!/usr/bin/env python3
"""
Główny plik aplikacji dla Google App Engine
"""


import os
import socket
import sys

# Dodanie ścieżki do modułów
sys.path.insert(0, os.path.dirname(__file__))

# Sentry monitoring - WYŁĄCZONY (za skomplikowany dla App Engine cold start)
# Zamiast Sentry używamy GCP Error Reporting (automatyczny w App Engine)

# Import aplikacji Flask
from src.main import app

# Dla App Engine, aplikacja musi być dostępna jako 'app'
if __name__ == "__main__":
    # Dla lokalnego uruchomienia
    default_port = int(os.environ.get("PORT", 8080))
    port = default_port

    # Jeśli port jest zajęty, wybierz wolny port, żeby uniknąć kolizji podczas lokalnego dev
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("0.0.0.0", default_port))
            s.listen(1)
        except OSError:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as probe:
                probe.bind(("0.0.0.0", 0))
                port = probe.getsockname()[1]
                print(f"⚠️  Port {default_port} zajęty, używam wolnego portu {port}")

    app.run(host="0.0.0.0", port=port, debug=False)
