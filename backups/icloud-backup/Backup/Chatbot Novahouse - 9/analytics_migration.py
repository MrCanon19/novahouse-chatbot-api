"""
Migracja bazy danych - dodanie kolumn analytics do tabeli conversations
"""

from src.models.chatbot import db
from sqlalchemy import text

def add_analytics_columns():
    """Dodanie kolumn analytics do tabeli conversations"""
    
    try:
        # Sprawdź czy kolumny już istnieją
        result = db.session.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'conversations' 
            AND column_name IN ('response_time_ms', 'input_tokens', 'output_tokens', 'total_tokens', 'cost_usd', 'lead_created')
        """))
        
        existing_columns = [row[0] for row in result.fetchall()]
        
        # Dodaj brakujące kolumny
        columns_to_add = [
            ('response_time_ms', 'INTEGER DEFAULT 0'),
            ('input_tokens', 'INTEGER DEFAULT 0'),
            ('output_tokens', 'INTEGER DEFAULT 0'),
            ('total_tokens', 'INTEGER DEFAULT 0'),
            ('cost_usd', 'DECIMAL(10,6) DEFAULT 0.0'),
            ('lead_created', 'BOOLEAN DEFAULT FALSE')
        ]
        
        for column_name, column_def in columns_to_add:
            if column_name not in existing_columns:
                sql = f"ALTER TABLE conversations ADD COLUMN {column_name} {column_def}"
                db.session.execute(text(sql))
                print(f"✅ Dodano kolumnę: {column_name}")
            else:
                print(f"⚠️ Kolumna już istnieje: {column_name}")
        
        db.session.commit()
        print("✅ Migracja analytics zakończona pomyślnie!")
        
    except Exception as e:
        print(f"❌ Błąd migracji: {e}")
        db.session.rollback()
        raise

if __name__ == "__main__":
    add_analytics_columns()

