# app/core/config.py

class Settings:
    SECRET_KEY = "change-this-to-a-very-long-random-secret-2025-secure-url-project"
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 1440

    # Oracle
    ORACLE_USER = "system"
    ORACLE_PASSWORD = "newpassword"
    ORACLE_DSN = "localhost:1521/XE"

    # Redis Cache
    REDIS_HOST = "localhost"
    REDIS_PORT = 6379
    REDIS_DB = 0
    REDIS_PASSWORD = None          # put password if you set one in Redis

settings = Settings()