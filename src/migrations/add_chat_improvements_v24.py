#!/usr/bin/env python3
"""
Migracja: Dodanie kolumn dla Chat Improvements V2.4
Data: 2025-11-20
Kolumny:
- ChatConversation: conversation_summary, needs_human_review, followup_count, last_followup_at
- ChatMessage: is_followup
"""

import os
import sys

# Dodaj ścieżkę do głównego katalogu projektu
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.main import app, db


def run_migration():
    """Uruchom migrację - dodaj nowe kolumny"""
    with app.app_context():
        print("Adding Chat Improvements V2.4 columns...")

        # SQL statements
        sql_statements = [
            # ChatConversation columns
            "ALTER TABLE chat_conversations ADD COLUMN IF NOT EXISTS conversation_summary TEXT",
            "ALTER TABLE chat_conversations ADD COLUMN IF NOT EXISTS needs_human_review BOOLEAN DEFAULT FALSE",
            "ALTER TABLE chat_conversations ADD COLUMN IF NOT EXISTS followup_count INTEGER DEFAULT 0",
            "ALTER TABLE chat_conversations ADD COLUMN IF NOT EXISTS last_followup_at TIMESTAMP",
            # ChatMessage column
            "ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS is_followup BOOLEAN DEFAULT FALSE",
        ]

        for sql in sql_statements:
            try:
                db.session.execute(db.text(sql))
                print(f"✅ {sql[:70]}...")
            except Exception as e:
                print(f"⚠️  Warning: {e}")

        db.session.commit()
        print("\n✅ Migration completed successfully!")

        # Verify columns
        from sqlalchemy import inspect

        inspector = inspect(db.engine)

        print("\nChatConversation columns:")
        for col in inspector.get_columns("chat_conversations"):
            if col["name"] in [
                "conversation_summary",
                "needs_human_review",
                "followup_count",
                "last_followup_at",
            ]:
                print(f"  ✓ {col['name']} ({col['type']})")

        print("\nChatMessage columns:")
        for col in inspector.get_columns("chat_messages"):
            if col["name"] == "is_followup":
                print(f"  ✓ {col['name']} ({col['type']})")


if __name__ == "__main__":
    try:
        run_migration()
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        sys.exit(1)
