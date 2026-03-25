# app/database/connection.py

import oracledb
from app.core.config import settings

def get_db():
    connection = oracledb.connect(
        user=settings.ORACLE_USER,
        password=settings.ORACLE_PASSWORD,
        dsn=settings.ORACLE_DSN
    )
    try:
        yield connection
    finally:
        connection.close()