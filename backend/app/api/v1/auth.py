import uuid
from fastapi import APIRouter, HTTPException, status, Depends
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.core.security import hash_password, verify_password, create_access_token, sanitize_input
from app.core.database import get_db_connection
from app.api.deps import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=Token)
def register(user_in: UserCreate):
    clean_email = sanitize_input(user_in.email).lower()
    clean_name = sanitize_input(user_in.full_name or "")
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (clean_email,))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email address already exists."
        )
        
    user_id = str(uuid.uuid4())
    hashed_pwd = hash_password(user_in.password)
    
    cursor.execute("""
    INSERT INTO users (id, email, hashed_password, full_name)
    VALUES (?, ?, ?, ?)
    """, (user_id, clean_email, hashed_pwd, clean_name))
    conn.commit()
    conn.close()
    
    access_token = create_access_token({"sub": user_id, "email": clean_email})
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(id=user_id, email=clean_email, full_name=clean_name)
    )

@router.post("/login", response_model=Token)
def login(creds: UserLogin):
    clean_email = sanitize_input(creds.email).lower()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (clean_email,))
    user = cursor.fetchone()
    conn.close()
    
    if not user or not verify_password(creds.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password."
        )
        
    access_token = create_access_token({"sub": user["id"], "email": user["email"]})
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserResponse(id=user["id"], email=user["email"], full_name=user["full_name"])
    )

@router.get("/me", response_model=UserResponse)
def get_me(current_user: dict = Depends(get_current_user)):
    return UserResponse(
        id=current_user["id"],
        email=current_user["email"],
        full_name=current_user.get("full_name"),
        created_at=str(current_user.get("created_at", ""))
    )
