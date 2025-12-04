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
    Uses a single transaction for all migrations
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
        skipped_count = 0

        # Run all migrations in a single transaction
        for sql, column_name in migrations:
            try:
                logger.info(f"  ➜ Adding column {column_name}...")
                db.session.execute(text(sql))
                added_count += 1
                logger.info(f"  ✅ {column_name} ready")
            except Exception as e:
                error_str = str(e).lower()
                if "already exists" in error_str or "duplicate column" in error_str:
                    skipped_count += 1
                    logger.info(f"  ⏭️  {column_name} already exists")
                else:
                    logger.warning(f"  ⚠️  Error with {column_name}: {str(e)[:100]}")

        # Single commit at the end
        db.session.commit()
        logger.info(
            f"✅ Migration complete: {added_count} columns processed, {skipped_count} already exist"
        )
        return True

    except Exception as e:
        db.session.rollback()
        logger.error(f"❌ Auto-migration failed: {str(e)}")
        # Don't crash the app, just log the error
        return False
