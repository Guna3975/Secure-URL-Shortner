CREATE TABLE user_urls (
    url_id        NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id       NUMBER NOT NULL,
    long_url      VARCHAR2(2048) NOT NULL,
    short_code    VARCHAR2(20) NOT NULL,
    click_count   NUMBER DEFAULT 0,
    is_active     NUMBER(1) DEFAULT 1,
    expires_at    TIMESTAMP NULL,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_user_urls_user
        FOREIGN KEY (user_id)
        REFERENCES app_users(user_id)
        ON DELETE CASCADE,

    CONSTRAINT uq_short_code UNIQUE (short_code)
);
CREATE INDEX idx_user_urls_short_code ON user_urls(short_code);

CREATE INDEX idx_user_urls_user_id ON user_urls(user_id);
