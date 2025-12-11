#!/usr/bin/env python3
"""
Standalone migration script to add email column to chat_conversations
Can be run directly with DATABASE_URL environment variable
"""

import os
import sys
from sqlalchemy import create_engine, inspect, text

def get_db_url() -> str:
    db_url = os.getenv("DATABASE_URL") or os.getenv("SQLALCHEMY_DATABASE_URI")
    if not db_url:
        raise RuntimeError(
            "Brak konfiguracji bazy. Ustaw DATABASE_URL lub SQLALCHEMY_DATABASE_URI."
        )
    return db_url


def add_email_column():
    try:
        engine = create_engine(get_db_url())
        inspector = inspect(engine)
        
        # Check if column already exists
        chat_conv_columns = [col.name for col in inspector.get_columns("chat_conversations")]
        
        if "email" in chat_conv_columns:
            msg = "✅ Kolumna 'email' już istnieje w chat_conversations"
            print(msg)
            return msg
        
        # Add email column and index
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE chat_conversations ADD COLUMN email VARCHAR(255)"))
            conn.execute(text("CREATE INDEX IF NOT EXISTS idx_chat_conversations_email ON chat_conversations(email)"))
            
            # Migrate existing email data from context_data JSON to email column
            try:
                conn.execute(text("""
                    UPDATE chat_conversations 
                    SET email = (context_data::json->>'email')::text
                    WHERE email IS NULL
                    AND context_data IS NOT NULL
                    AND context_data::json->>'email' IS NOT NULL
                """))
                print("✅ Zmigrowano istniejące dane email z context_data")
            except Exception as e:
                print(f"⚠️  Nie udało się zmigrować danych z context_data: {e}")
                print("   (Kolumna została dodana, ale dane nie zostały zmigrowane)")
        
        msg = "✅ Kolumna 'email' została dodana do chat_conversations z indeksem"
        print(msg)
        return msg
        
    except Exception as e:
        msg = f"❌ Błąd dodawania kolumny email: {e}"
        print(msg, file=sys.stderr)
        raise


if __name__ == "__main__":
    print("=" * 70)
    print("🚀 MIGRACJA: Dodanie kolumny email do chat_conversations")
    print("=" * 70)
    print()
    
    try:
        add_email_column()
        print()
        print("✅ Migracja zakończona pomyślnie!")
        sys.exit(0)
    except Exception as e:
        print()
        print(f"❌ Migracja nie powiodła się: {e}")
        sys.exit(1)

