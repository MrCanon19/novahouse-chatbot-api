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
current DATABASE_URL configuration and suggests the **manual SQL** you should
apply to make the table match the model (`id` integer PK, unique `session_id`).
"""

import os
import sys
from typing import Dict, List, Optional, Sequence

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


def _describe_columns(connection) -> Sequence[Dict[str, Optional[str]]]:
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
        return []

    print("📋 Columns:")
    column_dicts: List[Dict[str, Optional[str]]] = []
    for name, dtype, nullable, default in rows:
        print(f"- {name}: {dtype}, nullable={nullable}, default={default}")
        column_dicts.append(
            {
                "name": name,
                "data_type": dtype,
                "is_nullable": nullable,
                "column_default": default,
            }
        )
    return column_dicts


def _describe_constraints(connection) -> Sequence[Dict[str, str]]:
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
        return []

    print("🔐 Constraints:")
    constraint_dicts: List[Dict[str, str]] = []
    for name, ctype, column in rows:
        print(f"- {ctype}: {name} on {column}")
        constraint_dicts.append({"name": name, "type": ctype, "column": column})
    return constraint_dicts


def _has_unique_session_id(constraints: Sequence[Dict[str, str]]) -> bool:
    return any(
        c["type"] in {"UNIQUE", "PRIMARY KEY"} and c["column"] == "session_id"
        for c in constraints
    )


def _summarize_needed_actions(
    columns: Sequence[Dict[str, Optional[str]]],
    pk_columns: Sequence[str],
    constraints: Sequence[Dict[str, str]],
):
    print("\n🧭 Suggested actions to align with the ORM model (id PK, unique session_id):")

    column_names = {col["name"] for col in columns}
    has_id_column = "id" in column_names
    has_session_id = "session_id" in column_names
    has_pk_on_id = pk_columns == ["id"]
    has_any_pk = bool(pk_columns)
    has_unique_session = _has_unique_session_id(constraints)

    if not has_id_column:
        print("- Add id column and primary key:")
        print("    ALTER TABLE chat_conversations ADD COLUMN id BIGSERIAL;")
        if has_any_pk:
            print("    -- Drop existing PK before adding a new one")
            print("    ALTER TABLE chat_conversations DROP CONSTRAINT <current_pkey_name>;")
        print(
            "    ALTER TABLE chat_conversations ADD CONSTRAINT chat_conversations_pkey PRIMARY KEY (id);"
        )
    elif not has_pk_on_id:
        if has_any_pk:
            print("- Move primary key onto id:")
            print("    ALTER TABLE chat_conversations DROP CONSTRAINT <current_pkey_name>;")
        else:
            print("- Add primary key on existing id column:")
        print(
            "    ALTER TABLE chat_conversations ADD CONSTRAINT chat_conversations_pkey PRIMARY KEY (id);"
        )
    else:
        print("- ✅ id column already present and set as primary key.")

    if not has_session_id:
        print("- ⚠️ session_id column missing; add it to match the model if required.")
    elif not has_unique_session:
        print("- Add uniqueness on session_id (if required by your code):")
        print(
            "    ALTER TABLE chat_conversations ADD CONSTRAINT chat_conversations_session_id_key UNIQUE (session_id);"
        )
    else:
        print("- ✅ session_id already unique (via UNIQUE constraint or PK).")

    print("\nNotes:")
    print("- Replace <current_pkey_name> with the actual constraint name from above output.")
    print("- Run these statements manually (psql/Cloud SQL) before creating a migration.")
    print("- After aligning the table, redeploy to verify the SQLAlchemy error disappears.")


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

            columns = _describe_columns(connection)
            constraints = _describe_constraints(connection)
            pk_columns = _get_primary_key_columns(connection)

        if columns:
            _summarize_needed_actions(columns, pk_columns, constraints)

        print("✅ Inspection complete. Review the above output and plan the exact migration.")


if __name__ == "__main__":
    describe_chat_conversations_table()
