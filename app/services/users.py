from sqlalchemy import or_
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models import User

from app.schema import UserCreate, UserLogin, Token
from app.core.db import get_db
from app.core.security import get_password_hash, verify_password, create_access_token, check_password_strength

router = APIRouter()


@router.post("/register", status_code=201)
def register_user(payload: UserCreate, db: Session = Depends(get_db)):

    user = db.query(User).filter(
        or_(User.username == payload.username, User.email == payload.email)
    ).first()

    if user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    check_password_strength(payload.password)
    
    valid_roles = ["reader", "admin"]
    if payload.role not in valid_roles:
        payload.role = "reader"

    hashed_pw = get_password_hash(payload.password)
    new_user = User(
        username=payload.username,
        email=payload.email,
        hashed_password=hashed_pw,
        role=payload.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"username": new_user.username, "email": new_user.email, "role": new_user.role}


@router.post("/login", response_model=Token)
def login_user(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == payload.username).first()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({"username": user.username, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/logout")
def logout_user():
    return {"detail": "Logout successful. Client should discard token."}
