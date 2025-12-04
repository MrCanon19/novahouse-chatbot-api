"""
Automatic database migration on app startup
Ensures all required columns exist in the leads table
"""

import logging

from sqlalchemy import text

logger = logging.getLogger(__name__)


def run_auto_migration(db):
    """
    Run automatic migration to add missing columns to leads table
    Called on app startup - safe to run multiple times (uses IF NOT EXISTS)
    """
    try:
        logger.info("🔄 Starting automatic database migration...")

        # List of columns to add
        migrations = [
            (
                "ALTER TABLE leads ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT FALSE",
                "email_verified",
            ),
            (
                "ALTER TABLE leads ADD COLUMN IF NOT EXISTS email_verification_token VARCHAR(128)",
                "email_verification_token",
            ),
            (
                "ALTER TABLE leads ADD COLUMN IF NOT EXISTS email_verified_at TIMESTAMP",
                "email_verified_at",
            ),
            (
                "ALTER TABLE leads ADD COLUMN IF NOT EXISTS phone_verified BOOLEAN DEFAULT FALSE",
                "phone_verified",
            ),
            (
                "ALTER TABLE leads ADD COLUMN IF NOT EXISTS phone_verification_code VARCHAR(6)",
                "phone_verification_code",
            ),
            (
                "ALTER TABLE leads ADD COLUMN IF NOT EXISTS phone_verified_at TIMESTAMP",
                "phone_verified_at",
            ),
            (
                "ALTER TABLE leads ADD COLUMN IF NOT EXISTS assigned_to_user_id VARCHAR(100)",
                "assigned_to_user_id",
            ),
            ("ALTER TABLE leads ADD COLUMN IF NOT EXISTS assigned_at TIMESTAMP", "assigned_at"),
            (
                "ALTER TABLE leads ADD COLUMN IF NOT EXISTS first_contact_at TIMESTAMP",
                "first_contact_at",
            ),
            (
                "ALTER TABLE leads ADD COLUMN IF NOT EXISTS expected_contact_by TIMESTAMP",
                "expected_contact_by",
            ),
        ]

        added_count = 0
        exists_count = 0

        for sql, column_name in migrations:
            try:
                db.session.execute(text(sql))
                db.session.commit()
                added_count += 1
                logger.info(f"✅ Column {column_name} added successfully")
            except Exception as e:
                db.session.rollback()
                error_str = str(e).lower()

                if "already exists" in error_str or "duplicate column" in error_str:
                    exists_count += 1
                    logger.info(f"⏭️  Column {column_name} already exists")
                else:
                    logger.warning(f"⚠️  Error adding {column_name}: {str(e)[:100]}")

        logger.info(f"✅ Migration complete: {added_count} added, {exists_count} already exist")
        return True

    except Exception as e:
        logger.error(f"❌ Auto-migration failed: {str(e)}")
        # Don't crash the app, just log the error
        return False
