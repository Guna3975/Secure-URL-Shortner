-- =============================================
-- Migration: 002_create_short_urls.sql
-- Description: Creates table for storing shortened URLs
-- =============================================

CREATE TABLE short_urls (
    id            NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    short_code    VARCHAR2(20) UNIQUE NOT NULL,
    original_url  VARCHAR2(2000) NOT NULL,
    user_id       NUMBER,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at    TIMESTAMP,
    click_count   NUMBER DEFAULT 0,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES app_users(user_id)
);

COMMIT;

-- Optional: Add index for faster lookup by short_code
CREATE INDEX idx_short_code ON short_urls(short_code);