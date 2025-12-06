"""
Quick migration to add missing context_data column
"""

from sqlalchemy import text
from src.models.chatbot import db


def add_context_data_column():
    """Add context_data column to chat_conversations table"""
    try:
        with db.engine.connect() as conn:
            # Check if column exists
            result = conn.execute(
                text(
                    """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name='chat_conversations'
                AND column_name='context_data'
            """
                )
            )

            if result.fetchone() is None:
                print("[Migration] Adding context_data column to chat_conversations...")
                conn.execute(text("ALTER TABLE chat_conversations ADD COLUMN context_data TEXT"))
                conn.commit()
                print("✅ context_data column added")
                return "✅ context_data column added successfully"
            else:
                print("⚠️  context_data column already exists")
                return "⚠️  context_data column already exists"
    except Exception as e:
        error_msg = f"❌ Error adding column: {e}"
        print(error_msg)
        return error_msg


if __name__ == "__main__":
    add_context_data_column()
