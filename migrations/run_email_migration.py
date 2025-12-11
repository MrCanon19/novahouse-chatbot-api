#!/usr/bin/env python3
"""
Production Migration Script - Add email column to chat_conversations
Can be run locally (with DATABASE_URL) or via API endpoint
"""

import os
import sys
import requests
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

# Production URL (from GAE)
PRODUCTION_URL = "https://glass-core-467907-e9.ey.r.appspot.com"

# Get API key from environment or .env
API_KEY = os.getenv("API_KEY") or os.getenv("ADMIN_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL") or os.getenv("SQLALCHEMY_DATABASE_URI")


def run_migration_via_api():
    """Run migration via API endpoint"""
    if not API_KEY:
        print("❌ API_KEY not found in environment")
        print("   Set API_KEY or ADMIN_API_KEY environment variable")
        return False
    
    print("=" * 70)
    print("🚀 MIGRACJA PRZEZ API ENDPOINT")
    print("=" * 70)
    print(f"📡 URL: {PRODUCTION_URL}")
    print(f"🔑 API Key: {'*' * (len(API_KEY) - 4)}{API_KEY[-4:]}")
    print()
    
    try:
        response = requests.post(
            f"{PRODUCTION_URL}/api/migration/create-dead-letter-queue",
            headers={
                "X-API-KEY": API_KEY,
                "Content-Type": "application/json"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Migracja zakończona pomyślnie!")
            print(f"   Message: {result.get('message', 'N/A')}")
            if 'tables' in result:
                print(f"   Tables: {result.get('tables', [])}")
            if 'indexes' in result:
                print(f"   Indexes: {result.get('indexes', [])}")
            return True
        else:
            print(f"❌ Błąd migracji: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Błąd połączenia: {e}")
        return False


def run_migration_direct():
    """Run migration directly on database"""
    if not DATABASE_URL:
        print("❌ DATABASE_URL not found in environment")
        print("   Set DATABASE_URL or SQLALCHEMY_DATABASE_URI environment variable")
        return False
    
    print("=" * 70)
    print("🚀 MIGRACJA BEZPOŚREDNIO NA BAZIE DANYCH")
    print("=" * 70)
    print(f"📦 Database: {DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else 'N/A'}")
    print()
    
    try:
        engine = create_engine(DATABASE_URL)
        inspector = inspect(engine)
        
        # Check if column exists
        chat_conv_columns = [col.name for col in inspector.get_columns("chat_conversations")]
        
        if "email" in chat_conv_columns:
            print("✅ Kolumna 'email' już istnieje w chat_conversations")
            return True
        
        # Add email column
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE chat_conversations ADD COLUMN email VARCHAR(255)"))
            conn.execute(text("CREATE INDEX idx_chat_conversations_email ON chat_conversations(email)"))
            
            # Migrate existing email data from context_data JSON to email column
            try:
                conn.execute(text("""
                    UPDATE chat_conversations 
                    SET email = (context_data::json->>'email')::text
                    WHERE email IS NULL
                    AND context_data IS NOT NULL
                    AND context_data::json->>'email' IS NOT NULL
                """))
            except Exception as e:
                print(f"⚠️  Nie udało się zmigrować danych z context_data: {e}")
                print("   (Kolumna została dodana, ale dane nie zostały zmigrowane)")
        
        print("✅ Kolumna 'email' została dodana do chat_conversations")
        print("✅ Indeks został utworzony")
        return True
        
    except Exception as e:
        print(f"❌ Błąd migracji: {e}")
        return False


if __name__ == "__main__":
    print()
    print("🔧 MIGRACJA: Dodanie kolumny email do chat_conversations")
    print()
    
    # Try API first (preferred for production)
    if API_KEY:
        print("📡 Próba migracji przez API endpoint...")
        if run_migration_via_api():
            sys.exit(0)
        print()
        print("⚠️  Migracja przez API nie powiodła się, próba bezpośrednia...")
        print()
    
    # Fallback to direct database migration
    if DATABASE_URL:
        print("📦 Próba migracji bezpośrednio na bazie danych...")
        if run_migration_direct():
            sys.exit(0)
    
    print()
    print("❌ Nie udało się uruchomić migracji")
    print()
    print("💡 Wymagane zmienne środowiskowe:")
    print("   - API_KEY lub ADMIN_API_KEY (dla migracji przez API)")
    print("   - DATABASE_URL lub SQLALCHEMY_DATABASE_URI (dla migracji bezpośredniej)")
    print()
    print("📝 Przykład użycia:")
    print("   export API_KEY='your-api-key'")
    print("   python migrations/run_email_migration.py")
    print()
    sys.exit(1)

