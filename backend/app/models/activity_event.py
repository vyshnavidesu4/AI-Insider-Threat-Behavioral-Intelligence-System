import enum
from sqlalchemy import Column, String, Boolean, Float, DateTime, Enum, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship
from app.core.database import BaseModel


class EventType(str, enum.Enum):
    LOGON = "LOGON"
    LOGOFF = "LOGOFF"
    FILE_ACCESS = "FILE_ACCESS"
    USB_TRANSFER = "USB_TRANSFER"
    EMAIL_SENT = "EMAIL_SENT"
    DB_QUERY = "DB_QUERY"
    WIRE_TRANSFER_INITIATED = "WIRE_TRANSFER_INITIATED"
    PRIVILEGE_CHANGE = "PRIVILEGE_CHANGE"


class SensitivityLevel(str, enum.Enum):
    PUBLIC = "PUBLIC"
    INTERNAL = "INTERNAL"
    CONFIDENTIAL = "CONFIDENTIAL"
    RESTRICTED_PII = "RESTRICTED_PII"
    WIRE_TRANSFER = "WIRE_TRANSFER"


class ActivityEvent(BaseModel):
    __tablename__ = "activity_events"

    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Neutral, factual event type
    event_type = Column(
        Enum(EventType, name="event_type_enum", values_callable=lambda obj: [e.value for e in obj]),
        nullable=False,
        index=True
    )
    
    source_ip = Column(String(45), nullable=True)  # Supports IPv4 and IPv6
    host_machine = Column(String(100), nullable=True)
    target_resource = Column(String(500), nullable=False)  # e.g., "core_banking.accounts_master", "smb://treasury/share/wire_approvals.xlsx"
    
    sensitivity_level = Column(
        Enum(SensitivityLevel, name="sensitivity_level_enum", values_callable=lambda obj: [e.value for e in obj]),
        default=SensitivityLevel.INTERNAL,
        nullable=False,
        index=True
    )
    
    volume_mb = Column(Float, default=0.0, nullable=False)
    
    # Contextual payload: SQL query text, recipient count, USB device serial, transfer amount, etc.
    event_metadata = Column("metadata", JSONB().with_variant(JSON, "sqlite"), default=dict, nullable=False)
    
    # Algorithmic anomaly label evaluated by behavioral engines
    is_anomalous = Column(Boolean, default=False, nullable=False, index=True)

    # Relationships
    employee = relationship("Employee", back_populates="activity_events")

    __table_args__ = (
        Index("ix_activity_events_emp_time", "employee_id", "timestamp"),
        Index("ix_activity_events_type_time", "event_type", "timestamp"),
    )
