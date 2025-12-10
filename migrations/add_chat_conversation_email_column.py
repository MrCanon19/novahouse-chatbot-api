"""Add email column to chat_conversations with safety checks."""

from sqlalchemy import text

from src.models.chatbot import db


def add_email_column():
    try:
        with db.engine.connect() as conn:
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
            conn.commit()
            msg = "✅ email column added with index"
            print(msg)
            return msg
    except Exception as exc:  # pragma: no cover
        msg = f"❌ Error adding email column: {exc}"
        print(msg)
        return msg


if __name__ == "__main__":
    add_email_column()
