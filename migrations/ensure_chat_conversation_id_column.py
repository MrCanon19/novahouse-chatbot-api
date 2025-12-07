#!/usr/bin/env python3
"""
Diagnostics-only helper to reveal the **actual** schema of the
`chat_conversations` table before making any structural changes.

Why this exists
---------------
Recent production errors (`Could not locate column in row for column
chat_conversations.id`) show that the table shape diverges from the ORM model.
Blindly applying ALTERs without knowing the live schema risks data loss or
locks. This script therefore performs **read-only** inspection so that you can
decide the correct manual or Alembic migration.

Run with: `python migrations/ensure_chat_conversation_id_column.py`
This prints the column list and constraints for `chat_conversations` using the
current DATABASE_URL configuration.
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


def _describe_columns(connection):
    columns_query = text(
        """
        SELECT column_name, data_type, is_nullable, column_default
        FROM information_schema.columns
        WHERE table_name = 'chat_conversations'
          AND table_schema = current_schema()
        ORDER BY ordinal_position
        """
    )
    rows = connection.execute(columns_query).fetchall()
    if not rows:
        print("⚠️  chat_conversations table does not exist in this schema.")
        return

    print("📋 Columns:")
    for name, dtype, nullable, default in rows:
        print(f"- {name}: {dtype}, nullable={nullable}, default={default}")


def _describe_constraints(connection):
    constraints_query = text(
        """
        SELECT tc.constraint_name, tc.constraint_type, kcu.column_name
        FROM information_schema.table_constraints tc
        JOIN information_schema.key_column_usage kcu
            ON tc.constraint_name = kcu.constraint_name
            AND tc.table_schema = kcu.table_schema
        WHERE tc.table_name = 'chat_conversations'
          AND tc.table_schema = current_schema()
        ORDER BY tc.constraint_type, tc.constraint_name, kcu.ordinal_position
        """
    )
    rows = connection.execute(constraints_query).fetchall()
    if not rows:
        print("(no constraints found)")
        return

    print("🔐 Constraints:")
    for name, ctype, column in rows:
        print(f"- {ctype}: {name} on {column}")


def describe_chat_conversations_table():
    """Print the current schema of chat_conversations without modifying it."""

    with app.app_context():
        if db.engine.dialect.name != "postgresql":
            print("⚠️  This diagnostic currently supports only PostgreSQL. Skipping.")
            return

        with db.engine.begin() as connection:
            if not _table_exists(connection):
                print("⚠️  chat_conversations table not found in current schema.")
                return

            _describe_columns(connection)
            _describe_constraints(connection)

        print("✅ Inspection complete. Review the above output and plan the exact migration.")


if __name__ == "__main__":
    describe_chat_conversations_table()
