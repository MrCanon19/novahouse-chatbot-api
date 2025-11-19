#!/usr/bin/env python3
"""
Migracja: Dodanie tabel analytics
Data: 2025-10-11
"""

import sys
import os

# Dodaj ścieżkę do głównego katalogu projektu
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.main import app, db

def run_migration():
    """Uruchom migrację - utwórz tabele analytics"""
    with app.app_context():
        print("Creating analytics tables...")

        # Utwórz tabele
        db.create_all()

        print("✅ Analytics tables created successfully!")
        print("\nTables created:")
        print("  - chat_analytics")
        print("  - user_engagement")
        print("  - intent_analytics")
        print("  - performance_metrics")

        # Sprawdź czy tabele zostały utworzone
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()

        print("\nAll tables in database:")
        for table in sorted(tables):
            print(f"  - {table}")

if __name__ == '__main__':
    run_migration()