#!/usr/bin/env python3
"""
Migracja: Dodanie nowych pól do tabeli Lead
Data: 2025-10-11
"""

import sys
import os

# Dodaj ścieżkę do głównego katalogu projektu
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.main import app, db
from sqlalchemy import text

def run_migration():
    """Uruchom migrację - dodaj nowe pola do Lead"""
    with app.app_context():
        print("Adding new fields to Lead table...")
        
        # Lista nowych kolumn do dodania
        new_columns = [
            "ALTER TABLE leads ADD COLUMN message TEXT",
            "ALTER TABLE leads ADD COLUMN source VARCHAR(50) DEFAULT 'chatbot'",
            "ALTER TABLE leads ADD COLUMN status VARCHAR(50) DEFAULT 'new'",
            "ALTER TABLE leads ADD COLUMN notes TEXT",
            "ALTER TABLE leads ADD COLUMN monday_item_id VARCHAR(100)",
            "ALTER TABLE leads ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP"
        ]
        
        for sql in new_columns:
            try:
                db.session.execute(text(sql))
                print(f"✅ Executed: {sql[:50]}...")
            except Exception as e:
                print(f"⚠️  Column might already exist: {str(e)[:80]}")
        
        try:
            db.session.commit()
            print("\n✅ Lead table migration completed successfully!")
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ Migration failed: {e}")

if __name__ == '__main__':
    run_migration()