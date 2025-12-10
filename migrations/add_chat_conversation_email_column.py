"""Add email column to chat_conversations with safety checks."""

import os
import sys

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError


def get_db_url() -> str:
    db_url = os.getenv("DATABASE_URL") or os.getenv("SQLALCHEMY_DATABASE_URI")
    if not db_url:
        raise RuntimeError(
            "Brak konfiguracji bazy. Ustaw DATABASE_URL lub SQLALCHEMY_DATABASE_URI."
        )
    return db_url


def add_email_column():
    try:
        engine = create_engine(get_db_url())
        with engine.begin() as conn:
            exists = conn.execute(
                text(
                    """
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_name = 'chat_conversations'
                      AND column_name = 'email'
                    LIMIT 1
                    """
                )
            ).scalar()

            if exists:
                msg = "⚠️  email column already exists"
                print(msg)
                return msg

            conn.execute(
                text(
                    """
                    ALTER TABLE chat_conversations
                    ADD COLUMN IF NOT EXISTS email VARCHAR(255)
                    """
                )
            )
            conn.execute(
                text(
                    """
                    CREATE INDEX IF NOT EXISTS ix_chat_conversations_email
                    ON chat_conversations (email)
                    """
                )
            )

            msg = "✅ email column added with index"
            print(msg)
            return msg
    except (SQLAlchemyError, RuntimeError) as exc:  # pragma: no cover
        msg = f"❌ Error adding email column: {exc}"
        print(msg, file=sys.stderr)
        return msg


if __name__ == "__main__":
    add_email_column()
