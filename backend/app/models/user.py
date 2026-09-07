import enum
from sqlalchemy import Column, String, Boolean, Enum
from sqlalchemy.orm import relationship
from app.core.database import BaseModel


class UserRole(str, enum.Enum):
    ANALYST = "analyst"
    MANAGER = "manager"
    ADMIN = "admin"


class User(BaseModel):
    __tablename__ = "users"

    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(
        Enum(UserRole, name="user_role_enum", values_callable=lambda obj: [e.value for e in obj]),
        default=UserRole.ANALYST,
        nullable=False,
        index=True
    )
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    assigned_investigations = relationship("Investigation", back_populates="assigned_to_user", foreign_keys="Investigation.assigned_to_user_id")
    triaged_alerts = relationship("Alert", back_populates="triaged_by_user", foreign_keys="Alert.triaged_by_user_id")
