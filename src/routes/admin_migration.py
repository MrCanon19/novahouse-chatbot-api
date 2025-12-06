"""
Admin Migration Endpoint - One-time database migration
Access: /admin/migrate-database?secret=MIGRATION_SECRET_2025
"""

import os
from datetime import datetime, timezone

from flask import Blueprint, jsonify, request
from sqlalchemy import text
from src.models.chatbot import db

admin_migration_bp = Blueprint("admin_migration", __name__)

# Secret token to prevent unauthorized access
MIGRATION_SECRET = os.getenv("MIGRATION_SECRET", "NOVAHOUSE_MIGRATION_2025_SECURE")

# Flag to track if migration was already run
migration_executed = False


@admin_migration_bp.route("/migrate-database", methods=["GET"])
def run_database_migration():
    """
    One-time database migration endpoint
    Adds lead verification and assignment fields to leads table

    Usage: /admin/migrate-database?secret=MIGRATION_SECRET_2025
    """
    global migration_executed

    # Check secret token
    secret = request.args.get("secret", "")
    if secret != MIGRATION_SECRET:
        return jsonify({"error": "Unauthorized", "message": "Invalid secret token"}), 401

    # Check if already executed
    if migration_executed:
        return (
            jsonify(
                {
                    "status": "skipped",
                    "message": "Migration already executed in this session",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            ),
            200,
        )

    results = []
    errors = []

    # New columns to add
    new_columns = [
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

    try:
        for sql, column_name in new_columns:
            try:
                db.session.execute(text(sql))
                db.session.commit()
                results.append(
                    {
                        "column": column_name,
                        "status": "added",
                        "message": f"✅ Column {column_name} added successfully",
                    }
                )
            except Exception as e:
                db.session.rollback()
                error_str = str(e).lower()

                if "already exists" in error_str or "duplicate column" in error_str:
                    results.append(
                        {
                            "column": column_name,
                            "status": "exists",
                            "message": f"⏭️  Column {column_name} already exists",
                        }
                    )
                else:
                    errors.append({"column": column_name, "error": str(e)[:200]})
                    results.append(
                        {
                            "column": column_name,
                            "status": "error",
                            "message": f"❌ Error: {str(e)[:100]}",
                        }
                    )

        # Mark as executed
        migration_executed = True

        # Count results
        added = sum(1 for r in results if r["status"] == "added")
        exists = sum(1 for r in results if r["status"] == "exists")
        failed = sum(1 for r in results if r["status"] == "error")

        response = {
            "status": "success" if failed == 0 else "partial",
            "summary": {
                "total_columns": len(new_columns),
                "added": added,
                "already_exists": exists,
                "failed": failed,
            },
            "details": results,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if errors:
            response["errors"] = errors

        if added > 0:
            response["message"] = f"🎉 Migration completed! Added {added} columns to leads table."
        elif exists == len(new_columns):
            response["message"] = "✓ All columns already exist - database is up to date."
        else:
            response["message"] = f"⚠️  Migration completed with {failed} errors."

        return jsonify(response), 200 if failed == 0 else 500

    except Exception as e:
        db.session.rollback()
        return (
            jsonify(
                {
                    "status": "error",
                    "error": str(e),
                    "message": "Migration failed",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            ),
            500,
        )


@admin_migration_bp.route("/migrate-database/status", methods=["GET"])
def migration_status():
    """Check migration status without running it"""
    try:
        # Check which columns exist
        result = db.session.execute(
            text(
                """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'leads'
            AND column_name IN (
                'email_verified', 'email_verification_token', 'email_verified_at',
                'phone_verified', 'phone_verification_code', 'phone_verified_at',
                'assigned_to_user_id', 'assigned_at', 'first_contact_at', 'expected_contact_by'
            )
            ORDER BY column_name
        """
            )
        )

        existing_columns = [row[0] for row in result]

        required_columns = [
            "email_verified",
            "email_verification_token",
            "email_verified_at",
            "phone_verified",
            "phone_verification_code",
            "phone_verified_at",
            "assigned_to_user_id",
            "assigned_at",
            "first_contact_at",
            "expected_contact_by",
        ]

        missing_columns = [col for col in required_columns if col not in existing_columns]

        return (
            jsonify(
                {
                    "status": "ok",
                    "migration_needed": len(missing_columns) > 0,
                    "existing_columns": existing_columns,
                    "missing_columns": missing_columns,
                    "migration_executed_in_session": migration_executed,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            ),
            200,
        )

    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500
