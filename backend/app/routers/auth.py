from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth import Token, LoginRequest, RefreshTokenRequest
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=Token, summary="Authenticate SOC user")
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
) -> Token:
    """Authenticate with email and password to receive JWT access and refresh tokens."""
    return auth_service.authenticate_user(db, login_data)


@router.post("/refresh", response_model=Token, summary="Refresh access token")
def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db),
) -> Token:
    """Submit a valid refresh token to obtain a fresh access + refresh token pair."""
    return auth_service.refresh_access_token(db, refresh_data)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Register SOC user")
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
) -> UserResponse:
    """Register a new SOC analyst, manager, or admin user."""
    return auth_service.register_user(db, user_data)


@router.get("/me", response_model=UserResponse, summary="Get current user profile")
def get_current_user_profile(
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Retrieve the currently authenticated SOC user profile."""
    return current_user
