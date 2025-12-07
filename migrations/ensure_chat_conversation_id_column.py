#!/usr/bin/env python3
"""
Hardens the `chat_conversations` table schema so the ORM can rely on an integer
`id` primary key and a unique `session_id`.

Key safety guarantees
---------------------
* No-op unless the database is PostgreSQL **and** the table exists.
* Uses `IF NOT EXISTS` / existence checks for idempotency.
* Drops an existing primary key only when it is not already on `id`.
* Re-seeds NULL `id` values using the attached identity/sequence.

Run with: `python migrations/ensure_chat_conversation_id_column.py`
"""

import os
import sys
from typing import List

from sqlalchemy import text

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.main import app, db  # noqa: E402


def _table_exists(connection) -> bool:
    """Return True if the chat_conversations table is present."""

    exists_query = text(
        """
        SELECT 1
        FROM information_schema.tables
        WHERE table_name = 'chat_conversations'
          AND table_schema = current_schema()
        """
    )
    return bool(connection.execute(exists_query).fetchone())


def _get_primary_key_columns(connection) -> List[str]:
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
    result = connection.execute(pk_query).fetchall()
    return [row[0] for row in result]


def _get_primary_key_name(connection) -> str | None:
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
    result = connection.execute(name_query).fetchone()
    return result[0] if result else None


def _ensure_session_id_unique(connection):
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
    exists = connection.execute(unique_check).fetchone()
    if exists:
        print("⏭️  Unique constraint on session_id already exists")
        return

    print("✅ Creating unique constraint on session_id")
    connection.execute(
        text("ALTER TABLE chat_conversations ADD CONSTRAINT chat_conversations_session_id_key UNIQUE (session_id)")
    )


def _ensure_id_default(connection):
    """Ensure id has a working sequence default and backfill NULLs."""

    default_query = text(
        """
        SELECT column_default
        FROM information_schema.columns
        WHERE table_name = 'chat_conversations'
          AND column_name = 'id'
        LIMIT 1
        """
    )
    default = connection.execute(default_query).scalar()
    if default:
        return

    sequence_name = "chat_conversations_id_seq"
    print(f"🔧 Creating sequence {sequence_name} and attaching default")
    connection.execute(
        text(
            f"""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM pg_class WHERE relname = '{sequence_name}'
                ) THEN
                    CREATE SEQUENCE {sequence_name};
                END IF;

                ALTER SEQUENCE {sequence_name} OWNED BY chat_conversations.id;
                ALTER TABLE chat_conversations ALTER COLUMN id SET DEFAULT nextval('{sequence_name}');
            END;
            $$
            """
        )
    )

    connection.execute(
        text(
            f"UPDATE chat_conversations SET id = nextval('{sequence_name}') WHERE id IS NULL"
        )
    )


def ensure_id_column():
    """Add missing id column and primary key for chat_conversations."""

    with app.app_context():
        if db.engine.dialect.name != "postgresql":
            print("⚠️  This migration currently supports only PostgreSQL. Skipping.")
            return

        with db.engine.begin() as connection:
            if not _table_exists(connection):
                print("⚠️  chat_conversations table not found in current schema. Skipping.")
                return

            # 1. Ensure the id column exists with an attached identity/sequence
            print("🔎 Ensuring chat_conversations.id column exists")
            connection.execute(
                text(
                    "ALTER TABLE IF EXISTS chat_conversations "
                    "ADD COLUMN IF NOT EXISTS id BIGSERIAL"
                )
            )

            _ensure_id_default(connection)

            # 3. Drop old primary key if it is not on id
            current_pk_columns = _get_primary_key_columns(connection)
            if current_pk_columns and current_pk_columns != ["id"]:
                pk_name = _get_primary_key_name(connection)
                print(f"🔧 Dropping existing primary key: {pk_name} ({current_pk_columns})")
                connection.execute(text(f"ALTER TABLE chat_conversations DROP CONSTRAINT {pk_name}"))

            # 4. Add primary key on id
            current_pk_columns = _get_primary_key_columns(connection)
            if current_pk_columns != ["id"]:
                print("✅ Creating primary key on id")
                connection.execute(
                    text(
                        "ALTER TABLE chat_conversations "
                        "ADD CONSTRAINT chat_conversations_pkey PRIMARY KEY (id)"
                    )
                )

            # 5. Preserve uniqueness on session_id
            _ensure_session_id_unique(connection)

            # 6. Mark column as NOT NULL for safety
            connection.execute(text("ALTER TABLE chat_conversations ALTER COLUMN id SET NOT NULL"))

        print("🎉 Migration completed - id column ensured")


if __name__ == "__main__":
    ensure_id_column()
