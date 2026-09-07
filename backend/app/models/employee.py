import enum
from sqlalchemy import Column, String, Boolean, Enum, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.core.database import BaseModel


class ClearanceLevel(str, enum.Enum):
    STANDARD = "STANDARD"
    CONFIDENTIAL = "CONFIDENTIAL"
    RESTRICTED = "RESTRICTED"
    HIGH_RISK = "HIGH_RISK"


class EmploymentStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    ON_NOTICE = "ON_NOTICE"
    PROBATION = "PROBATION"
    TERMINATED = "TERMINATED"


class Employee(BaseModel):
    __tablename__ = "employees"

    employee_number = Column(String(50), unique=True, index=True, nullable=False)
    department_id = Column(UUID(as_uuid=True), ForeignKey("departments.id", ondelete="RESTRICT"), nullable=False, index=True)
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    job_title = Column(String(255), nullable=False)
    clearance_level = Column(
        Enum(ClearanceLevel, name="clearance_level_enum", values_callable=lambda obj: [e.value for e in obj]),
        default=ClearanceLevel.STANDARD,
        nullable=False
    )
    is_privileged = Column(Boolean, default=False, nullable=False)  # Admin / DBA / Treasury Approval authority
    status = Column(
        Enum(EmploymentStatus, name="employment_status_enum", values_callable=lambda obj: [e.value for e in obj]),
        default=EmploymentStatus.ACTIVE,
        nullable=False,
        index=True
    )
    hire_date = Column(Date, nullable=True)

    # Relationships
    department = relationship("Department", back_populates="employees")
    activity_events = relationship("ActivityEvent", back_populates="employee", cascade="all, delete-orphan")
    behavior_baselines = relationship("BehaviorBaseline", back_populates="employee", cascade="all, delete-orphan")
    risk_scores = relationship("RiskScore", back_populates="employee", cascade="all, delete-orphan")
    alerts = relationship("Alert", back_populates="employee", cascade="all, delete-orphan")
    investigations = relationship("Investigation", back_populates="target_employee", foreign_keys="Investigation.target_employee_id")
