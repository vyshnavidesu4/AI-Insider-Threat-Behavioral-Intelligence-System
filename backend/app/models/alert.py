import enum
from datetime import datetime, timezone
from sqlalchemy import Column, String, Float, DateTime, Enum, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship
from app.core.database import BaseModel


class AlertSeverity(str, enum.Enum):
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFORMATIONAL = "INFORMATIONAL"


class AlertStatus(str, enum.Enum):
    NEW = "NEW"
    TRIAGED = "TRIAGED"
    ESCALATED = "ESCALATED"
    CLOSED_BENIGN = "CLOSED_BENIGN"
    CLOSED_MALICIOUS = "CLOSED_MALICIOUS"


class Alert(BaseModel):
    __tablename__ = "alerts"

    alert_id = Column(String(50), unique=True, index=True, nullable=False)  # e.g., ALT-2026-00412
    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    
    severity = Column(
        Enum(AlertSeverity, name="alert_severity_enum", values_callable=lambda obj: [e.value for e in obj]),
        default=AlertSeverity.MEDIUM,
        nullable=False,
        index=True
    )
    
    status = Column(
        Enum(AlertStatus, name="alert_status_enum", values_callable=lambda obj: [e.value for e in obj]),
        default=AlertStatus.NEW,
        nullable=False,
        index=True
    )
    
    risk_score_at_trigger = Column(Float, nullable=False)
    
    # Specific rule violations, anomaly scores, or indicator signatures that triggered this alert
    trigger_reasons = Column(JSONB().with_variant(JSON, "sqlite"), default=dict, nullable=False)
    
    triggered_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    
    triaged_by_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    triaged_at = Column(DateTime(timezone=True), nullable=True)
    triage_notes = Column(String(1000), nullable=True)

    # Optional linkage to an active investigation case
    investigation_id = Column(UUID(as_uuid=True), ForeignKey("investigations.id", ondelete="SET NULL"), nullable=True, index=True)

    # Relationships
    employee = relationship("Employee", back_populates="alerts")
    triaged_by_user = relationship("User", back_populates="triaged_alerts", foreign_keys=[triaged_by_user_id])
    investigation = relationship("Investigation", back_populates="alerts")

    __table_args__ = (
        Index("ix_alerts_severity_status", "severity", "status"),
    )
