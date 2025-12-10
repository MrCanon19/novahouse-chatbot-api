"""Add email column to chat_conversations table if missing."""

from sqlalchemy import text
from src.models.chatbot import db


TABLE_NAME = "chat_conversations"
COLUMN_NAME = "email"


def add_email_column():
    try:
        with db.engine.connect() as conn:
            result = conn.execute(
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

            if result.fetchone() is None:
                print("[Migration] Adding email column to chat_conversations...")
                conn.execute(
                    text(
                        "ALTER TABLE chat_conversations ADD COLUMN email VARCHAR(255)"
                    )
                )
                conn.commit()
                print("✅ email column added successfully")
                return "✅ email column added successfully"

            print("⚠️  email column already exists")
            return "⚠️  email column already exists"
    except Exception as e:
        error_msg = f"❌ Error adding email column: {e}"
        print(error_msg)
        return error_msg


if __name__ == "__main__":
    add_email_column()
