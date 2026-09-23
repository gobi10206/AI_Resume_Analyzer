import hashlib
import hmac
import base64
import json
import time
import re
import html
from typing import Optional, Dict, Any
from app.core.config import settings

def hash_password(password: str, salt: Optional[str] = None) -> str:
    """PBKDF2-HMAC-SHA256 password hashing with salt."""
    if salt is None:
        salt = base64.b64encode(os_urandom(16)).decode("ascii")
    derived = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt.encode("utf-8"), 100000)
    hash_b64 = base64.b64encode(derived).decode("ascii")
    return f"{salt}${hash_b64}"

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against stored salt$hash."""
    try:
        salt, hash_val = hashed_password.split("$", 1)
        expected = hash_password(plain_password, salt=salt)
        return hmac.compare_digest(expected, hashed_password)
    except Exception:
        return False

def _b64_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")

def _b64_decode(data: str) -> bytes:
    padding = 4 - (len(data) % 4)
    if padding != 4:
        data += "=" * padding
    return base64.urlsafe_b64decode(data.encode("ascii"))

def create_access_token(data: dict, expires_delta_seconds: Optional[int] = None) -> str:
    """Create HS256 JWT access token."""
    header = {"alg": settings.ALGORITHM, "typ": "JWT"}
    payload = data.copy()
    now = int(time.time())
    if expires_delta_seconds is not None:
        payload["exp"] = now + expires_delta_seconds
    else:
        payload["exp"] = now + (settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    payload["iat"] = now
    
    header_b64 = _b64_encode(json.dumps(header, separators=(",", ":")).encode("utf-8"))
    payload_b64 = _b64_encode(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    
    signing_input = f"{header_b64}.{payload_b64}"
    signature = hmac.new(
        settings.SECRET_KEY.encode("utf-8"),
        signing_input.encode("ascii"),
        hashlib.sha256
    ).digest()
    sig_b64 = _b64_encode(signature)
    return f"{signing_input}.{sig_b64}"

def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode and verify HS256 JWT access token."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        header_b64, payload_b64, sig_b64 = parts
        
        signing_input = f"{header_b64}.{payload_b64}"
        expected_sig = hmac.new(
            settings.SECRET_KEY.encode("utf-8"),
            signing_input.encode("ascii"),
            hashlib.sha256
        ).digest()
        if not hmac.compare_digest(_b64_encode(expected_sig), sig_b64):
            return None
            
        payload = json.loads(_b64_decode(payload_b64).decode("utf-8"))
        if "exp" in payload and payload["exp"] < int(time.time()):
            return None  # Expired
        return payload
    except Exception:
        return None

def sanitize_input(text: str) -> str:
    """Sanitize user text input against XSS and HTML tags."""
    if not text:
        return ""
    # Strip HTML tags
    cleaned = re.sub(r"<[^>]*?>", "", text)
    # Escape special characters
    return html.escape(cleaned.strip())

import os
def os_urandom(n: int) -> bytes:
    return os.urandom(n)
