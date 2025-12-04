-- Migration: Add Lead Verification & Assignment Fields
-- Database: glass-core-467907-e9:europe-west1:novahouse-chatbot-db
-- Run in GCP Console > Cloud SQL > novahouse-chatbot-db > Run SQL

-- Email verification fields
ALTER TABLE leads ADD COLUMN IF NOT EXISTS email_verified BOOLEAN DEFAULT FALSE;
ALTER TABLE leads ADD COLUMN IF NOT EXISTS email_verification_token VARCHAR(128);
ALTER TABLE leads ADD COLUMN IF NOT EXISTS email_verified_at TIMESTAMP;

-- Phone verification fields
ALTER TABLE leads ADD COLUMN IF NOT EXISTS phone_verified BOOLEAN DEFAULT FALSE;
ALTER TABLE leads ADD COLUMN IF NOT EXISTS phone_verification_code VARCHAR(6);
ALTER TABLE leads ADD COLUMN IF NOT EXISTS phone_verified_at TIMESTAMP;

-- Lead assignment fields
ALTER TABLE leads ADD COLUMN IF NOT EXISTS assigned_to_user_id VARCHAR(100);
ALTER TABLE leads ADD COLUMN IF NOT EXISTS assigned_at TIMESTAMP;
ALTER TABLE leads ADD COLUMN IF NOT EXISTS first_contact_at TIMESTAMP;
ALTER TABLE leads ADD COLUMN IF NOT EXISTS expected_contact_by TIMESTAMP;

-- Verify migration
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'leads'
AND column_name IN (
    'email_verified', 'email_verification_token', 'email_verified_at',
    'phone_verified', 'phone_verification_code', 'phone_verified_at',
    'assigned_to_user_id', 'assigned_at', 'first_contact_at', 'expected_contact_by'
)
ORDER BY column_name;
