import json
from typing import Optional, Dict, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_access_token
from app.core.database import get_db_connection

security_bearer = HTTPBearer(auto_error=False)

def get_current_user(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_bearer)) -> Dict[str, Any]:
    """Extract and validate current user from JWT Bearer token or provide mock/demo user."""
    if not credentials:
        # Fallback to demo user for testing/unauthenticated access
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ?", ("demo@airesume.dev",))
        user = cursor.fetchone()
        if not user:
            # Create default demo user
            from app.core.security import hash_password
            cursor.execute("""
            INSERT INTO users (id, email, hashed_password, full_name)
            VALUES (?, ?, ?, ?)
            """, ("user_demo_1", "demo@airesume.dev", hash_password("demo123"), "Demo User"))
            conn.commit()
            cursor.execute("SELECT * FROM users WHERE email = ?", ("demo@airesume.dev",))
            user = cursor.fetchone()
        conn.close()
        return dict(user)

    token = credentials.credentials
    payload = decode_access_token(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )
        
    user_id = payload["sub"]
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    return dict(user)
