     # app/core/config.py

class Settings:
    SECRET_KEY = "change-this-to-a-very-long-random-secret-2025-secure-url-project"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 1 day

    # Oracle connection – CHANGE THESE VALUES
    ORACLE_USER = "system"              # ← your actual username
    ORACLE_PASSWORD = "newpassword"     # ← your actual password
    ORACLE_DSN = "localhost:1521/XE"    # ← your SID/service name

settings = Settings()