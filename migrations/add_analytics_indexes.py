#!/usr/bin/env python3
"""
Add performance-focused indexes for analytics endpoints.
Run with: python migrations/add_analytics_indexes.py
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import text
from src.main import app, db

INDEXES = [
    # Conversations: used in counts and distinct session queries by timestamp
    ("idx_conversations_timestamp", "conversations", "timestamp"),
    ("idx_conversations_session_id", "conversations", "session_id"),
    # UserEngagement: filtered by first_interaction and aggregated by session
    ("idx_user_engagement_first_interaction", "user_engagement", "first_interaction"),
    ("idx_user_engagement_session_id", "user_engagement", "session_id"),
    # ChatAnalytics: analytics by timestamp
    ("idx_chat_analytics_timestamp", "chat_analytics", "timestamp"),
    # IntentAnalytics: filtered by date range
    ("idx_intent_analytics_date", "intent_analytics", "date"),
    # Leads: ensure created_at is indexed for range queries (skip if exists)
    ("idx_leads_created_at", "leads", "created_at"),
]


def add_indexes():
    with app.app_context():
        print("=" * 70)
        print("🚀 DATABASE INDEX MIGRATION (Analytics)")
        print("=" * 70)
        print()

        created_count = 0
        skipped_count = 0
        failed_count = 0

        for index_name, table_name, column_name in INDEXES:
            try:
                if db.engine.dialect.name == "postgresql":
                    check_query = text(
                        """
                        SELECT 1 FROM pg_indexes
                        WHERE indexname = :index_name
                        """
                    )
                else:
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
