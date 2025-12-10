"""
Simple migration script for A/B Testing and Competitive Intelligence
Run with: python3 migrations/run_migration_simple.py
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set env vars
os.environ["FLASK_ENV"] = "development"
os.environ["DATABASE_URL"] = os.getenv("DATABASE_URL", "postgresql://localhost/novahouse_chatbot")

from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker

print("=" * 60)
print("A/B Testing & Competitive Intelligence Migration")
print("=" * 60)

# Get database URL
db_url = os.getenv("DATABASE_URL")
if not db_url:
    print("❌ DATABASE_URL not set!")
    sys.exit(1)

    print("📦 Connecting to database...")

# Create engine
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()

inspector = inspect(engine)
existing_tables = inspector.get_table_names()

print(f"✅ Connected! Found {len(existing_tables)} existing tables")

# 1. Create followup_tests table
print("\n1️⃣  Creating followup_tests table...")
if "followup_tests" not in existing_tables:
    session.execute(
        text(
            """
        CREATE TABLE followup_tests (
            id SERIAL PRIMARY KEY,
            question_type VARCHAR(100) NOT NULL,
            variant_a TEXT NOT NULL,
            variant_b TEXT NOT NULL,
            variant_a_shown INTEGER DEFAULT 0,
            variant_b_shown INTEGER DEFAULT 0,
            variant_a_responses INTEGER DEFAULT 0,
            variant_b_responses INTEGER DEFAULT 0,
            is_active BOOLEAN DEFAULT true,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
        )
    )
    session.commit()
    print("   ✅ followup_tests table created")
else:
    print("   ⚠️  followup_tests already exists, skipping")

# 2. Create competitive_intel table
print("\n2️⃣  Creating competitive_intel table...")
if "competitive_intel" not in existing_tables:
    session.execute(
        text(
            """
        CREATE TABLE competitive_intel (
            id SERIAL PRIMARY KEY,
            session_id VARCHAR(100) NOT NULL,
            intel_type VARCHAR(50) NOT NULL,
            competitor_name VARCHAR(100),
            user_message TEXT NOT NULL,
            context TEXT,
            sentiment VARCHAR(20),
            priority VARCHAR(20) DEFAULT 'medium',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
        )
    )
    session.commit()
    print("   ✅ competitive_intel table created")
else:
    print("   ⚠️  competitive_intel already exists, skipping")

# 3. Add email column to chat_conversations
print("\n3️⃣  Adding email to chat_conversations...")
try:
    result = session.execute(
        text(
            """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name='chat_conversations'
        AND column_name='email'
    """
        )
    )

    if result.fetchone() is None:
        session.execute(
            text(
                "ALTER TABLE chat_conversations ADD COLUMN IF NOT EXISTS email VARCHAR(255)"
            )
        )
        session.commit()
        print("   ✅ email column added")
    else:
        print("   ⚠️  email already exists, skipping")

    index_result = session.execute(
        text(
            """
        SELECT indexname
        FROM pg_indexes
        WHERE tablename='chat_conversations'
        AND indexname='ix_chat_conversations_email'
    """
        )
    )

    if index_result.fetchone() is None:
        session.execute(
            text(
                "CREATE INDEX IF NOT EXISTS ix_chat_conversations_email ON chat_conversations(email)"
            )
        )
        session.commit()
        print("   ✅ email index created")
    else:
        print("   ⚠️  email index already exists, skipping")
except Exception as e:
    print(f"   ❌ Error: {e}")
    session.rollback()

# 4. Add followup_variant column to chat_conversations
print("\n4️⃣  Adding followup_variant to chat_conversations...")
try:
    result = session.execute(
        text(
            """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name='chat_conversations'
        AND column_name='followup_variant'
    """
        )
    )

    if result.fetchone() is None:
        session.execute(
            text("ALTER TABLE chat_conversations ADD COLUMN followup_variant VARCHAR(10)")
        )
        session.commit()
        print("   ✅ followup_variant column added")
    else:
        print("   ⚠️  followup_variant already exists, skipping")
except Exception as e:
    print(f"   ❌ Error: {e}")
    session.rollback()

# 5. Insert default A/B tests
print("\n5️⃣  Adding default A/B tests...")

default_tests = [
    {
        "type": "package_to_sqm",
        "a": "💡 **A jaki jest mniej więcej metraż Twojego mieszkania?** To pomoże mi lepiej dopasować ofertę.",
        "b": "📐 **Ile metrów kwadratowych ma Twoje mieszkanie?** Na tej podstawie przygotuję dokładną wycenę.",
    },
    {
        "type": "sqm_to_location",
        "a": "📍 **W jakim mieście szukasz wykonawcy?** Mamy zespoły w całej Polsce.",
        "b": "🗺️ **Gdzie znajduje się Twoje mieszkanie?** Sprawdzę dostępność naszych ekip w Twojej okolicy.",
    },
    {
        "type": "price_to_budget",
        "a": "💰 **Masz już określony budżet? Mogę pokazać opcje finansowania i rozłożenia płatności.**",
        "b": "💵 **Jaki budżet planujesz przeznaczyć na wykończenie?** Dopasuję najlepszą opcję dla Ciebie.",
    },
]

for test in default_tests:
    # Check if exists
    result = session.execute(
        text(f"SELECT id FROM followup_tests WHERE question_type = '{test['type']}'")
    )

    if result.fetchone() is None:
        session.execute(
            text(
                f"""
            INSERT INTO followup_tests (question_type, variant_a, variant_b, is_active)
            VALUES ('{test['type']}', :variant_a, :variant_b, true)
        """
            ),
            {"variant_a": test["a"], "variant_b": test["b"]},
        )
        session.commit()
        print(f"   ✅ Added A/B test: {test['type']}")
    else:
        print(f"   ⚠️  Test already exists: {test['type']}")

print("\n" + "=" * 60)
print("✅ Migration completed successfully!")
print("=" * 60)

session.close()
