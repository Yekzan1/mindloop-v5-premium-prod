import bcrypt
import re
from datetime import datetime, timedelta
import secrets

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def check_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except Exception:
        return False

def validate_email(email: str) -> bool:
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def generate_session_token() -> str:
    return secrets.token_urlsafe(32)

def is_strong_password(password: str) -> bool:
    # At least 8 chars, 1 letter, 1 number
    return len(password) >= 8 and any(c.isdigit() for c in password) and any(c.isalpha() for c in password)
