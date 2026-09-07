import enum
from sqlalchemy import Column, String, Enum
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship
from app.core.database import BaseModel


class DepartmentCode(str, enum.Enum):
    RETAIL_BANKING = "RETAIL_BANKING"
    WEALTH_MANAGEMENT = "WEALTH_MANAGEMENT"
    TREASURY_OPERATIONS = "TREASURY_OPERATIONS"
    LOAN_ORIGINATION = "LOAN_ORIGINATION"
    COMPLIANCE_AND_RISK = "COMPLIANCE_AND_RISK"
    IT_OPERATIONS = "IT_OPERATIONS"


class RiskTier(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Department(BaseModel):
    __tablename__ = "departments"

    code = Column(
        Enum(DepartmentCode, name="department_code_enum", values_callable=lambda obj: [e.value for e in obj]),
        unique=True,
        index=True,
        nullable=False
    )
    name = Column(String(255), nullable=False)
    description = Column(String(500), nullable=True)
    risk_tier = Column(
        Enum(RiskTier, name="department_risk_tier_enum", values_callable=lambda obj: [e.value for e in obj]),
        default=RiskTier.MEDIUM,
        nullable=False
    )
    # Bank policies: e.g. max authorized daily wire transfer, sensitivity classification, allowed access hours
    data_access_policies = Column(JSONB().with_variant(JSON, "sqlite"), default=dict, nullable=False)

    # Relationships
    employees = relationship("Employee", back_populates="department", cascade="all, delete-orphan")
