BEGIN;

CREATE EXTENSION IF NOT EXISTS pgcrypto;

DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM pg_type
        WHERE typname = 'roadmap_generated_by'
    ) THEN
        CREATE TYPE roadmap_generated_by AS ENUM ('ai', 'manager', 'hr', 'organization');
    END IF;
END $$;

COMMIT;
