import cx_Oracle
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthenticationError(Exception):
    pass


def authenticate_user(email: str, password: str, connection):
    # 1️⃣ Basic input validation
    if not email or not password:
        raise AuthenticationError("Email and password are required.")

    cursor = connection.cursor()

    # 2️⃣ Fetch user by email
    cursor.execute("""
        SELECT password_hash, is_active
        FROM app_users
        WHERE email = :email
    """, {"email": email})

    row = cursor.fetchone()

    # 3️⃣ Check if user exists
    if not row:
        raise AuthenticationError("User does not exist.")

    stored_hash, is_active = row

    # 4️⃣ Check if account is active
    if is_active != 1:
        raise AuthenticationError("User account is inactive.")

    # 5️⃣ Verify password hash
    if not pwd_context.verify(password, stored_hash):
        raise AuthenticationError("Invalid password.")

    return True
