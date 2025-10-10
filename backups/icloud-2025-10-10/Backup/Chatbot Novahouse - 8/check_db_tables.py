#!/usr/bin/env python3
"""
Sprawdzenie struktury bazy danych PostgreSQL
"""

import psycopg2

# Konfiguracja bazy danych
DB_CONFIG = {
    'host': '35.205.83.191',
    'database': 'chatbot_db', 
    'user': 'chatbot_user',
    'password': 'NovaHouse2024SecurePass',
    'port': 5432
}

def main():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("🔍 Sprawdzanie tabel w bazie danych...")
        
        # Lista wszystkich tabel
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        tables = cursor.fetchall()
        print(f"\n📋 Znalezione tabele ({len(tables)}):")
        for table in tables:
            print(f"  - {table[0]}")
        
        # Sprawdzenie struktury każdej tabeli
        for table in tables:
            table_name = table[0]
            print(f"\n🔧 Struktura tabeli '{table_name}':")
            
            cursor.execute(f"""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = '{table_name}'
                ORDER BY ordinal_position;
            """)
            
            columns = cursor.fetchall()
            for col in columns:
                print(f"  - {col[0]} ({col[1]}) {'NULL' if col[2] == 'YES' else 'NOT NULL'}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Błąd: {e}")

if __name__ == "__main__":
    main()

