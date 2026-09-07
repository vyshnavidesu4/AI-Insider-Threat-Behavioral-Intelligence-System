from typing import Optional
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    decode_token,
)
from app.models.user import User, UserRole
from app.schemas.auth import Token, LoginRequest, RefreshTokenRequest
from app.schemas.user import UserCreate


class AuthService:
    @staticmethod
    def authenticate_user(db: Session, login_data: LoginRequest) -> Token:
        """Authenticate user credentials and issue access + refresh JWT tokens."""
        user = db.query(User).filter(User.email == login_data.email.lower()).first()
        if not user or not verify_password(login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is deactivated",
            )
        
        access_token = create_access_token(subject=user.id, role=user.role.value)
        refresh_token = create_refresh_token(subject=user.id, role=user.role.value)
        
        return Token(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    @staticmethod
    def refresh_access_token(db: Session, refresh_data: RefreshTokenRequest) -> Token:
        """Validate refresh token and issue new token pair."""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
        payload = decode_token(refresh_data.refresh_token, settings.JWT_REFRESH_SECRET_KEY)
        if not payload:
            raise credentials_exception
        
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type: expected refresh token",
            )
        
        user_id_str: Optional[str] = payload.get("sub")
        if not user_id_str:
            raise credentials_exception
        
        try:
            user_id = UUID(user_id_str)
        except ValueError:
            raise credentials_exception
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_active:
            raise credentials_exception
        
        new_access_token = create_access_token(subject=user.id, role=user.role.value)
        new_refresh_token = create_refresh_token(subject=user.id, role=user.role.value)
        
        return Token(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            token_type="bearer",
            expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )

    @staticmethod
    def register_user(db: Session, user_data: UserCreate) -> User:
        """Register a new user account with hashed password."""
        existing_user = db.query(User).filter(User.email == user_data.email.lower()).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="A user with this email address already exists",
            )
        
        hashed_password = get_password_hash(user_data.password)
        new_user = User(
            email=user_data.email.lower(),
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            role=user_data.role,
            is_active=True,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user


auth_service = AuthService()
