#!/usr/bin/env python3
"""
Add Lead Verification and Assignment Fields Migration

Adds email/phone verification and lead assignment fields to leads table.
Run with: python migrations/add_lead_verification_fields.py
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from src.main import app, db


def add_verification_and_assignment_fields():
    """Add verification and assignment fields to leads table"""

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
        ("ALTER TABLE leads ADD COLUMN email_verified_at DATETIME", "email_verified_at"),
        # Phone verification fields
        (
            "ALTER TABLE leads ADD COLUMN phone_verified BOOLEAN DEFAULT FALSE",
            "phone_verified",
        ),
        (
            "ALTER TABLE leads ADD COLUMN phone_verification_code VARCHAR(6)",
            "phone_verification_code",
        ),
        ("ALTER TABLE leads ADD COLUMN phone_verified_at DATETIME", "phone_verified_at"),
        # Lead assignment fields
        (
            "ALTER TABLE leads ADD COLUMN assigned_to_user_id VARCHAR(100)",
            "assigned_to_user_id",
        ),
        ("ALTER TABLE leads ADD COLUMN assigned_at DATETIME", "assigned_at"),
        ("ALTER TABLE leads ADD COLUMN first_contact_at DATETIME", "first_contact_at"),
        (
            "ALTER TABLE leads ADD COLUMN expected_contact_by DATETIME",
            "expected_contact_by",
        ),
    ]

    with app.app_context():
        print("=" * 70)
        print("🚀 LEAD VERIFICATION & ASSIGNMENT MIGRATION")
        print("=" * 70)
        print()

        added_count = 0
        skipped_count = 0

        for sql, column_name in new_columns:
            try:
                db.session.execute(text(sql))
                db.session.commit()
                print(f"✅ Added column: {column_name}")
                added_count += 1
            except Exception as e:
                db.session.rollback()
                if "duplicate column" in str(e).lower() or "already exists" in str(e).lower():
                    print(f"⏭️  Column {column_name} already exists, skipping")
                    skipped_count += 1
                else:
                    print(f"❌ Error adding {column_name}: {str(e)[:100]}")

        print()
        print("=" * 70)
        print("📊 SUMMARY")
        print("=" * 70)
        print(f"✅ Added: {added_count} columns")
        print(f"⏭️  Skipped: {skipped_count} columns (already exist)")
        print()

        if added_count > 0:
            print("🎉 Migration completed successfully!")
        else:
            print("✓ All columns already exist - no changes needed")


if __name__ == "__main__":
    add_verification_and_assignment_fields()
