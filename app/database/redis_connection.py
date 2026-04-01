# app/database/redis_connection.py

import redis
from app.core.config import settings

# Create Redis connection pool
redis_client = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    password=settings.REDIS_PASSWORD,
    decode_responses=True,      # automatically convert bytes to str
    socket_timeout=5
)

def get_redis():
    """Return Redis client for dependency injection"""
    try:
        redis_client.ping()     # test connection
        return redis_client
    except redis.ConnectionError:
        raise Exception("Redis server is not running")