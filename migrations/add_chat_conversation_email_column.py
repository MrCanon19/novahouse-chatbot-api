"""Add email column to chat_conversations table if missing."""

from sqlalchemy import text
from src.models.chatbot import db


TABLE_NAME = "chat_conversations"
COLUMN_NAME = "email"
INDEX_NAME = "ix_chat_conversations_email"


def add_email_column():
    try:
        with db.engine.begin() as conn:
            column_result = conn.execute(
                text(
                    """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name=:table_name
                AND column_name=:column_name
            """
                ),
                {"table_name": TABLE_NAME, "column_name": COLUMN_NAME},
            )

            if column_result.fetchone() is None:
                print("[Migration] Adding email column to chat_conversations...")
                conn.execute(
                    text(
                        "ALTER TABLE chat_conversations ADD COLUMN IF NOT EXISTS email VARCHAR(255)"
                    )
                )
                print("✅ email column added successfully")
            else:
                print("⚠️  email column already exists")

            index_result = conn.execute(
                text(
                    """
                SELECT indexname
                FROM pg_indexes
                WHERE tablename=:table_name
                AND indexname=:index_name
            """
                ),
                {"table_name": TABLE_NAME, "index_name": INDEX_NAME},
            )

            if index_result.fetchone() is None:
                print("[Migration] Creating email index on chat_conversations...")
                conn.execute(
                    text(
                        "CREATE INDEX IF NOT EXISTS ix_chat_conversations_email ON chat_conversations(email)"
                    )
                )
                print("✅ email index created successfully")
            else:
                print("⚠️  email index already exists")

            return "✅ email column/index ensured"
    except Exception as e:
        error_msg = f"❌ Error adding email column: {e}"
        print(error_msg)
        return error_msg


if __name__ == "__main__":
    add_email_column()
