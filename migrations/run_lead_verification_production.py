#!/usr/bin/env python3
"""
Production Migration Script - Add Lead Verification & Assignment Fields
Connects directly to production database via Cloud SQL Proxy
"""

import os
import sys

# Production DATABASE_URL from app.yaml
DATABASE_URL = "postgresql://chatbot_user:vicNRNoO3TpLZzQ_BkAVbz886dW_J0Yo@/chatbot?host=/cloudsql/glass-core-467907-e9:europe-west1:novahouse-chatbot-db"

# Override environment
os.environ["DATABASE_URL"] = DATABASE_URL

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

print("=" * 70)
print("🚀 PRODUCTION MIGRATION: Lead Verification & Assignment Fields")
print("=" * 70)
print("📦 Database: glass-core-467907-e9:europe-west1:novahouse-chatbot-db")
print()

try:
    # Create engine
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    print("✅ Connected to production database")
    print()

    # New columns to add
    new_columns = [
        # Email verification fields
        (
            "ALTER TABLE leads ADD COLUMN email_verified BOOLEAN DEFAULT FALSE",
            "email_verified",
        ),
        (
            "ALTER TABLE leads ADD COLUMN email_verification_token VARCHAR(128)",
            "email_verification_token",
        ),
        ("ALTER TABLE leads ADD COLUMN email_verified_at TIMESTAMP", "email_verified_at"),
        # Phone verification fields
        (
            "ALTER TABLE leads ADD COLUMN phone_verified BOOLEAN DEFAULT FALSE",
            "phone_verified",
        ),
        (
            "ALTER TABLE leads ADD COLUMN phone_verification_code VARCHAR(6)",
            "phone_verification_code",
        ),
        ("ALTER TABLE leads ADD COLUMN phone_verified_at TIMESTAMP", "phone_verified_at"),
        # Lead assignment fields
        (
            "ALTER TABLE leads ADD COLUMN assigned_to_user_id VARCHAR(100)",
            "assigned_to_user_id",
        ),
        ("ALTER TABLE leads ADD COLUMN assigned_at TIMESTAMP", "assigned_at"),
        ("ALTER TABLE leads ADD COLUMN first_contact_at TIMESTAMP", "first_contact_at"),
        (
            "ALTER TABLE leads ADD COLUMN expected_contact_by TIMESTAMP",
            "expected_contact_by",
        ),
    ]

    added_count = 0
    skipped_count = 0

    for sql, column_name in new_columns:
        try:
            session.execute(text(sql))
            session.commit()
            print(f"✅ Added column: {column_name}")
            added_count += 1
        except Exception as e:
            session.rollback()
            if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
                print(f"⏭️  Column {column_name} already exists, skipping")
                skipped_count += 1
            else:
                print(f"❌ Error adding {column_name}: {str(e)[:150]}")

    print()
    print("=" * 70)
    print("📊 SUMMARY")
    print("=" * 70)
    print(f"✅ Added: {added_count} columns")
    print(f"⏭️  Skipped: {skipped_count} columns (already exist)")
    print()

    if added_count > 0:
        print("🎉 Migration completed successfully!")
        print()
        print("🔄 Next steps:")
        print("   1. Restart the application to load the new schema")
        print("   2. Test the analytics dashboard")
    else:
        print("✓ All columns already exist - no changes needed")

    session.close()

except Exception as e:
    print(f"❌ Migration failed: {e}")
    sys.exit(1)
