from sqlalchemy import Column, Float, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship
from app.core.database import BaseModel


class RiskScore(BaseModel):
    __tablename__ = "risk_scores"

    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    calculated_at = Column(DateTime(timezone=True), nullable=False, index=True)

    # The 5 weighted risk score dimensions (0-100 scale)
    # Weight: 35% - Unusual data volumes, anomaly clustering, anomalous outbound activity
    behavioral_anomalies_score = Column(Float, default=0.0, nullable=False)
    
    # Weight: 25% - Unauthorized attempts, elevation of rights, unusual administrative tooling
    privilege_misuse_score = Column(Float, default=0.0, nullable=False)
    
    # Weight: 20% - Bulk customer PII access, high-risk wire folder inspection, non-departmental assets
    data_access_violations_score = Column(Float, default=0.0, nullable=False)
    
    # Weight: 10% - Off-hour/weekend spikes, unexpected geo/IP origins, rapid device hopping
    access_pattern_deviations_score = Column(Float, default=0.0, nullable=False)
    
    # Weight: 10% - Past confirmed alerts, security policy acknowledgements, DLP incident history
    historical_security_events_score = Column(Float, default=0.0, nullable=False)

    # Final weighted composite score (0-100)
    # Formula: 0.35*behavioral + 0.25*privilege + 0.20*data_access + 0.10*access_pattern + 0.10*historical
    composite_score = Column(Float, default=0.0, nullable=False, index=True)

    # Structured JSONB explanation for SOC analysts (e.g., top 3 contributing factors, human-readable rationale)
    risk_factors = Column(JSONB().with_variant(JSON, "sqlite"), default=dict, nullable=False)

    # Relationships
    employee = relationship("Employee", back_populates="risk_scores")

    __table_args__ = (
        Index("ix_risk_scores_emp_calculated", "employee_id", "calculated_at"),
        Index("ix_risk_scores_composite", "composite_score"),
    )
