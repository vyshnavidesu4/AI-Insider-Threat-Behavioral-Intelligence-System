import enum
from sqlalchemy import Column, String, Text, Enum, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship
from app.core.database import BaseModel


class InvestigationStatus(str, enum.Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    UNDER_REVIEW = "UNDER_REVIEW"
    RESOLVED = "RESOLVED"
    REFERRED_TO_LEGAL = "REFERRED_TO_LEGAL"


class InvestigationPriority(str, enum.Enum):
    P1_URGENT = "P1_URGENT"
    P2_HIGH = "P2_HIGH"
    P3_MEDIUM = "P3_MEDIUM"
    P4_LOW = "P4_LOW"


class Investigation(BaseModel):
    __tablename__ = "investigations"

    case_number = Column(String(50), unique=True, index=True, nullable=False)  # e.g., INV-2026-0089
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    
    status = Column(
        Enum(InvestigationStatus, name="investigation_status_enum", values_callable=lambda obj: [e.value for e in obj]),
        default=InvestigationStatus.OPEN,
        nullable=False,
        index=True
    )
    
    priority = Column(
        Enum(InvestigationPriority, name="investigation_priority_enum", values_callable=lambda obj: [e.value for e in obj]),
        default=InvestigationPriority.P2_HIGH,
        nullable=False,
        index=True
    )

    target_employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="RESTRICT"), nullable=False, index=True)
    assigned_to_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    hypothesis = Column(Text, nullable=True)
    
    # Chronological key events marked by analysts during investigation
    timeline_events = Column(JSONB().with_variant(JSON, "sqlite"), default=list, nullable=False)
    
    findings_summary = Column(Text, nullable=True)

    # Relationships
    target_employee = relationship("Employee", back_populates="investigations", foreign_keys=[target_employee_id])
    assigned_to_user = relationship("User", back_populates="assigned_investigations", foreign_keys=[assigned_to_user_id])
    alerts = relationship("Alert", back_populates="investigation")

    __table_args__ = (
        Index("ix_investigations_status_priority", "status", "priority"),
    )
