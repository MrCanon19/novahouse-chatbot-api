#!/usr/bin/env python3
"""
Główny plik aplikacji dla Google App Engine
"""

import os
import sys

# Dodanie ścieżki do modułów
sys.path.insert(0, os.path.dirname(__file__))

# Import aplikacji Flask
from src.main import app

# Dla App Engine, aplikacja musi być dostępna jako 'app'
if __name__ == '__main__':
    # Dla lokalnego uruchomienia
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=False)

