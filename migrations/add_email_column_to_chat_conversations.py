"""
Migration: Add email column to chat_conversations table
Date: 2025-12-11
Reason: RODO service requires email column for data export/deletion
"""

from sqlalchemy import text


def upgrade(connection):
    """Add email column to chat_conversations table"""
    try:
        # Check if column already exists
        result = connection.execute(text("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name='chat_conversations' AND column_name='email'
        """))
        
        if result.fetchone():
            print("✅ Column 'email' already exists in chat_conversations")
            return
        
        # Add email column
        connection.execute(text("""
            ALTER TABLE chat_conversations 
            ADD COLUMN email VARCHAR(255) NULL
        """))
        
        # Create index on email for faster lookups
        connection.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_chat_conversations_email 
            ON chat_conversations(email)
        """))
        
        # Migrate existing email data from context_data JSON to email column
        connection.execute(text("""
            UPDATE chat_conversations 
            SET email = (
                SELECT (context_data::json->>'email')::text
                WHERE context_data IS NOT NULL 
                AND context_data::json->>'email' IS NOT NULL
            )
            WHERE email IS NULL
            AND context_data IS NOT NULL
            AND context_data::json->>'email' IS NOT NULL
        """))
        
        connection.commit()
        print("✅ Successfully added email column to chat_conversations")
        
    except Exception as e:
        connection.rollback()
        print(f"⚠️  Error adding email column: {e}")
        # Don't fail migration if column already exists or other minor issues
        if "already exists" not in str(e).lower() and "duplicate" not in str(e).lower():
            raise


def downgrade(connection):
    """Remove email column from chat_conversations table"""
    try:
        # Drop index first
        connection.execute(text("""
            DROP INDEX IF EXISTS idx_chat_conversations_email
        """))
        
        # Drop column
        connection.execute(text("""
            ALTER TABLE chat_conversations 
            DROP COLUMN IF EXISTS email
        """))
        
        connection.commit()
        print("✅ Successfully removed email column from chat_conversations")
        
    except Exception as e:
        connection.rollback()
        print(f"⚠️  Error removing email column: {e}")
        raise

