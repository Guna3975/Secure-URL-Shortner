CREATE TABLE url_click_logs (
    log_id     NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    url_id     NUMBER NOT NULL,
    ip_address VARCHAR2(45),
    user_agent VARCHAR2(500),
    clicked_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_click_url
        FOREIGN KEY (url_id)
        REFERENCES user_urls(url_id)
        ON DELETE CASCADE
);
