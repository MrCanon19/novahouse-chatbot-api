-- Chat Improvements V2.4 - Database Migration
-- Run this in Cloud SQL PostgreSQL

-- Add new columns to chat_conversations
ALTER TABLE chat_conversations ADD COLUMN IF NOT EXISTS conversation_summary TEXT;
ALTER TABLE chat_conversations ADD COLUMN IF NOT EXISTS needs_human_review BOOLEAN DEFAULT FALSE;
ALTER TABLE chat_conversations ADD COLUMN IF NOT EXISTS followup_count INTEGER DEFAULT 0;
ALTER TABLE chat_conversations ADD COLUMN IF NOT EXISTS last_followup_at TIMESTAMP;

-- Add new column to chat_messages
ALTER TABLE chat_messages ADD COLUMN IF NOT EXISTS is_followup BOOLEAN DEFAULT FALSE;

-- Verify columns exist
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'chat_conversations'
AND column_name IN ('conversation_summary', 'needs_human_review', 'followup_count', 'last_followup_at');

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'chat_messages'
AND column_name = 'is_followup';
