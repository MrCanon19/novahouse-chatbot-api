#!/usr/bin/env python3
"""
Uruchomienie migracji analytics dla NovaHouse chatbot
"""

import sys
import os

# Dodaj ścieżkę do projektu
sys.path.insert(0, '/home/ubuntu/CZATNR3/novahouse_chatbot_gcp_deployment/novahouse_chatbot_api')

# Ustaw zmienne środowiskowe
os.environ['MONDAY_API_KEY'] = 'eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjQ0NzE5NjI5NSwiYWFpIjoxMSwidWlkIjo2NzU0NzQ0MywiaWFkIjoiMjAyNC0wOS0wN1QwODoyNjoyNy4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6MjU5NzE5NzMsInJnbiI6InVzZTEifQ.Wy7Uy6Qs_Oj8Uw_5YdQJJdqfJGfJGfJGfJGfJGfJGfJ'
os.environ['OPENAI_API_KEY'] = 'sk-proj-test-key'  # Placeholder

try:
    from src.main import app
    from src.models.analytics_migration import add_analytics_columns
    
    print("🚀 Uruchamianie migracji analytics...")
    
    with app.app_context():
        add_analytics_columns()
    
    print("✅ Migracja zakończona pomyślnie!")
    
except Exception as e:
    print(f"❌ Błąd migracji: {e}")
    sys.exit(1)

