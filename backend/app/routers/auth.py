from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.auth import create_access_token, hash_password, verify_password
from app.db import get_db
from app.models import Streak, User
from app.schemas import Token, UserCreate, UserLogin, UserOut

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/register', response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(payload: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(status_code=400, detail='Email already registered')
    user = User(email=payload.email, password_hash=hash_password(payload.password), timezone=payload.timezone)
    db.add(user)
    db.flush()
    db.add(Streak(user_id=user.id, current_streak=0, longest_streak=0))
    db.commit()
    db.refresh(user)
    return user


@router.post('/login', response_model=Token)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(status_code=401, detail='Invalid credentials')
    return Token(access_token=create_access_token(str(user.id)))
