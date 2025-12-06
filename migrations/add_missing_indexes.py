#!/usr/bin/env python3
"""
Add missing database indexes for performance
Run with: python migrations/add_missing_indexes.py
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from src.main import app, db


def add_indexes():
    """Add missing indexes to improve query performance"""

    indexes = [
        # Leads table - CRITICAL (most queried)
        ("idx_leads_session_id", "leads", "session_id"),
        ("idx_leads_status", "leads", "status"),
        ("idx_leads_created_at", "leads", "created_at"),
        ("idx_leads_email", "leads", "email"),  # For duplicate detection
        ("idx_leads_lead_score", "leads", "lead_score"),  # For filtering high quality
        # ChatConversation
        ("idx_chat_conv_session_id", "chat_conversations", "session_id"),
        ("idx_chat_conv_started_at", "chat_conversations", "started_at"),
        # ChatMessage
        ("idx_chat_msg_conversation_id", "chat_messages", "conversation_id"),
        ("idx_chat_msg_timestamp", "chat_messages", "timestamp"),
        # AuditLog (RODO)
        ("idx_audit_session_id", "audit_logs", "session_id"),
        ("idx_audit_action", "audit_logs", "action"),
        ("idx_audit_timestamp", "audit_logs", "timestamp"),
        # RodoConsent
        ("idx_rodo_session_id", "rodo_consents", "session_id"),
        # Bookings
        ("idx_bookings_lead_id", "bookings", "lead_id"),
        ("idx_bookings_session_id", "bookings", "session_id"),
        # CompetitiveIntel
        ("idx_competitive_session_id", "competitive_intel", "session_id"),
        ("idx_competitive_type", "competitive_intel", "intel_type"),
    ]

    with app.app_context():
        print("=" * 70)
        print("🚀 DATABASE INDEX MIGRATION")
        print("=" * 70)
        print()

        created_count = 0
        skipped_count = 0
        failed_count = 0

        for index_name, table_name, column_name in indexes:
            try:
                # Check if index exists (database-agnostic)
                if db.engine.dialect.name == "postgresql":
                    check_query = text(
                        """
                        SELECT 1 FROM pg_indexes
                        WHERE indexname = :index_name
                    """
                    )
                else:
                    # SQLite
                    check_query = text(
                        """
                        SELECT 1 FROM sqlite_master
                        WHERE type = 'index' AND name = :index_name
                    """
                    )

                result = db.session.execute(check_query, {"index_name": index_name}).fetchone()

                if not result:
                    print(f"Creating index: {index_name} on {table_name}({column_name})")
                    db.session.execute(
                        text(f"CREATE INDEX {index_name} ON {table_name} ({column_name})")
                    )
                    db.session.commit()
                    print(f"✅ Created {index_name}")
                    created_count += 1
                else:
                    print(f"⏭️  {index_name} already exists, skipping")
                    skipped_count += 1

            except Exception as e:
                print(f"❌ Error creating {index_name}: {e}")
                db.session.rollback()
                failed_count += 1

        print()
        print("=" * 70)
        print("📊 SUMMARY")
        print("=" * 70)
        print(f"✅ Created: {created_count}")
        print(f"⚠️  Skipped: {skipped_count}")
        print(f"❌ Failed: {failed_count}")
        print()

        if failed_count == 0:
            print("🎉 Index migration completed successfully!")
        else:
            print("⚠️  Some indexes failed to create. Check errors above.")
            sys.exit(1)


if __name__ == "__main__":
    add_indexes()
