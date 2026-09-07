from typing import List, Optional
from uuid import UUID
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.database import get_db
from app.core.security import decode_token
from app.models.user import User, UserRole

# HTTP Bearer security scheme for Swagger UI & API header parsing
security_scheme = HTTPBearer(auto_error=False)


async def get_token_from_header(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security_scheme)
) -> str:
    """Extract Bearer token from Authorization header with explicit 401 on missing token."""
    if not credentials or not credentials.credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required: missing Bearer token in Authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return credentials.credentials


async def get_current_user(
    token: str = Depends(get_token_from_header),
    db: Session = Depends(get_db),
) -> User:
    """Validate access token and return the authenticated User model."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials or token expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_token(token, settings.JWT_SECRET_KEY)
    if not payload:
        raise credentials_exception
    
    token_type = payload.get("type")
    if token_type != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type: expected access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id_str: Optional[str] = payload.get("sub")
    if not user_id_str:
        raise credentials_exception

    try:
        user_id = UUID(user_id_str)
    except ValueError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user account",
        )

    return user


class RoleChecker:
    """Dependency for enforcing role-based access control (RBAC)."""
    
    def __init__(self, allowed_roles: List[UserRole]):
        self.allowed_roles = allowed_roles

    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied: Operation requires one of the following roles: {[r.value for r in self.allowed_roles]}",
            )
        return current_user


# Pre-configured role dependencies
require_analyst = RoleChecker([UserRole.ANALYST, UserRole.MANAGER, UserRole.ADMIN])
require_manager = RoleChecker([UserRole.MANAGER, UserRole.ADMIN])
require_admin = RoleChecker([UserRole.ADMIN])


def require_role(allowed_roles: List[UserRole]) -> RoleChecker:
    """Factory function for custom role restrictions."""
    return RoleChecker(allowed_roles)
