from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta, timezone
from app.database.connection import get_db
from app.core.config import settings
import oracledb   
from pydantic import BaseModel, EmailStr, validator
import dns.resolver
import dns.exception

router = APIRouter(prefix="/auth", tags=["auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"



class UserCreate(BaseModel):
    email: EmailStr
    password: str

    @validator('email')
    def validate_real_email_domain(cls, v):
        domain = v.split('@')[1].lower()

        # Optional: still enforce common providers if you want
        # common_providers = {'gmail.com', 'yahoo.com', 'outlook.com', ...}
        # if domain not in common_providers:
        #     raise ValueError("Please use email from Gmail, Yahoo, Outlook, etc.")

        try:
            # Query MX records
            answers = dns.resolver.resolve(domain, 'MX')
            if not answers:
                raise ValueError("No mail servers found for this domain")
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.exception.Timeout):
            raise ValueError("Invalid or non-existent email domain")
        except Exception as e:
            raise ValueError(f"Email domain check failed: {str(e)}")

        return v


class UserOut(BaseModel):
    user_id: int
    email: EmailStr

# app/routes/auth_routes.py

@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db=Depends(get_db)):
    cursor = db.cursor()

    # Check if email already exists
    cursor.execute("SELECT user_id FROM app_users WHERE email = :email", email=user.email)
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Safe password handling for bcrypt limit
    password_bytes = user.password.encode('utf-8')
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    hashed_password = pwd_context.hash(password_bytes.decode('utf-8'))

    try:
        # Create output variable for RETURNING user_id
        new_id_var = cursor.var(oracledb.NUMBER)

        cursor.execute("""
            INSERT INTO app_users (email, password_hash, is_active)
            VALUES (:email, :pwd_hash, 1)
            RETURNING user_id INTO :new_id
        """, 
        email=user.email,
        pwd_hash=hashed_password,
        new_id=new_id_var)

        # Get the returned user_id – it's a list containing one value
        returned_value = new_id_var.getvalue()
        
        # Extract the actual number (first element of the list)
        if returned_value is None or len(returned_value) == 0:
            raise ValueError("No user_id returned after insert")
        
        new_user_id = int(returned_value[0])  # ← this is the fix

        db.commit()

        return {"user_id": new_user_id, "email": user.email}

    except oracledb.DatabaseError as e:
        db.rollback()
        error, = e.args
        raise HTTPException(status_code=500, detail=f"Database error: {error.message}")
    except ValueError as ve:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Data error: {str(ve)}")
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("""
        SELECT user_id, password_hash
        FROM app_users
        WHERE email = :email AND is_active = 1
    """, email=form_data.username)

    row = cursor.fetchone()
    if not row or not pwd_context.verify(form_data.password, row[1]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = row[0]
    access_token = jwt.encode(
        {
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        },
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return {"access_token": access_token}