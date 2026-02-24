-- 001_create_app_users.sql

CREATE TABLE app_users (
    user_id       NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email         VARCHAR2(255) UNIQUE NOT NULL,
    password_hash VARCHAR2(255) NOT NULL,
    is_active     NUMBER(1) DEFAULT 1,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_app_users_email ON app_users(email);