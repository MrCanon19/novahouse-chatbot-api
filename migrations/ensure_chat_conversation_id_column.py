#!/usr/bin/env python3
"""
Ensure chat_conversations table has an auto-incrementing integer primary key (id).
This fixes production errors where the table was created without the `id` column
and ORM queries expect it.

Run with: python migrations/ensure_chat_conversation_id_column.py
"""

import os
import sys
from typing import List

from sqlalchemy import text

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.main import app, db  # noqa: E402


def _get_primary_key_columns() -> List[str]:
    """Return the list of primary key columns for chat_conversations."""
    pk_query = text(
        """
        SELECT kcu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
            AND tc.table_schema = kcu.table_schema
        WHERE tc.table_name = 'chat_conversations'
          AND tc.constraint_type = 'PRIMARY KEY'
        ORDER BY kcu.ordinal_position
        """
    )
    result = db.session.execute(pk_query).fetchall()
    return [row[0] for row in result]


def _get_primary_key_name() -> str | None:
    """Return current primary key constraint name if present."""
    name_query = text(
        """
        SELECT tc.constraint_name
        FROM information_schema.table_constraints tc
        WHERE tc.table_name = 'chat_conversations'
          AND tc.constraint_type = 'PRIMARY KEY'
        LIMIT 1
        """
    )
    result = db.session.execute(name_query).fetchone()
    return result[0] if result else None


def _ensure_session_id_unique():
    """Ensure session_id stays unique after adjusting primary key."""
    unique_check = text(
        """
        SELECT tc.constraint_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
            AND tc.table_schema = kcu.table_schema
        WHERE tc.table_name = 'chat_conversations'
          AND tc.constraint_type = 'UNIQUE'
          AND kcu.column_name = 'session_id'
        LIMIT 1
        """
    )
    exists = db.session.execute(unique_check).fetchone()
    if exists:
        print("⏭️  Unique constraint on session_id already exists")
        return

    print("✅ Creating unique constraint on session_id")
    db.session.execute(
        text("ALTER TABLE chat_conversations ADD CONSTRAINT chat_conversations_session_id_key UNIQUE (session_id)")
    )
    db.session.commit()


def ensure_id_column():
    """Add missing id column and primary key for chat_conversations."""
    with app.app_context():
        if db.engine.dialect.name != "postgresql":
            print("⚠️  This migration currently supports only PostgreSQL. Skipping.")
            return

        column_check = text(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name = 'chat_conversations'
              AND column_name = 'id'
            LIMIT 1
            """
        )
        has_id = db.session.execute(column_check).fetchone()

        if has_id:
            print("⏭️  id column already exists - ensuring unique constraint only")
            _ensure_session_id_unique()
            return

        print("🚧 Adding missing id column to chat_conversations")
        # 1. Add the column with a sequence (bigserial behaviour)
        db.session.execute(
            text(
                "ALTER TABLE chat_conversations ADD COLUMN id BIGSERIAL"
            )
        )
        db.session.commit()

        # 2. Populate existing rows
        db.session.execute(
            text(
                """
                UPDATE chat_conversations
                SET id = nextval(pg_get_serial_sequence('chat_conversations', 'id'))
                WHERE id IS NULL
                """
            )
        )
        db.session.commit()

        # 3. Drop old primary key if it is not on id
        current_pk_columns = _get_primary_key_columns()
        if current_pk_columns and current_pk_columns != ["id"]:
            pk_name = _get_primary_key_name()
            print(f"🔧 Dropping existing primary key: {pk_name} ({current_pk_columns})")
            db.session.execute(text(f"ALTER TABLE chat_conversations DROP CONSTRAINT {pk_name}"))
            db.session.commit()

        # 4. Add primary key on id
        current_pk_columns = _get_primary_key_columns()
        if current_pk_columns != ["id"]:
            print("✅ Creating primary key on id")
            db.session.execute(
                text("ALTER TABLE chat_conversations ADD CONSTRAINT chat_conversations_pkey PRIMARY KEY (id)")
            )
            db.session.commit()

        # 5. Preserve uniqueness on session_id
        _ensure_session_id_unique()

        # 6. Mark column as NOT NULL for safety
        db.session.execute(text("ALTER TABLE chat_conversations ALTER COLUMN id SET NOT NULL"))
        db.session.commit()

        print("🎉 Migration completed - id column ensured")


if __name__ == "__main__":
    ensure_id_column()
