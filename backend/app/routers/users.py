from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.dependencies import get_current_user, require_admin, require_manager
from app.models.user import User, UserRole
from app.schemas.user import UserResponse, UserUpdate
from app.services.user_service import user_service

router = APIRouter(prefix="/users", tags=["User Management"])


@router.get(
    "/",
    response_model=List[UserResponse],
    summary="List SOC team members",
    dependencies=[Depends(require_manager)]
)
def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
) -> List[UserResponse]:
    """List all SOC users. Restricted to Manager and Admin roles."""
    return user_service.get_all(db, skip=skip, limit=limit)


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get user details by ID"
)
def get_user_by_id(
    user_id: UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserResponse:
    """Retrieve user details. Analysts can only view their own profile; Managers/Admins can view any."""
    if current_user.role == UserRole.ANALYST and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Analysts are only authorized to view their own profile",
        )
    user = user_service.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update user details",
    dependencies=[Depends(require_admin)]
)
def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
) -> UserResponse:
    """Update user role, status, or details. Restricted to Admin role."""
    return user_service.update_user(db, user_id, user_update)
