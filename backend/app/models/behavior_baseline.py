from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.types import JSON
from sqlalchemy.orm import relationship
from app.core.database import BaseModel


class BehaviorBaseline(BaseModel):
    __tablename__ = "behavior_baselines"

    employee_id = Column(UUID(as_uuid=True), ForeignKey("employees.id", ondelete="CASCADE"), nullable=False, index=True)
    metric_name = Column(String(100), nullable=False, index=True)  # e.g., "daily_download_mb", "daily_logon_hour", "sensitive_query_count", "wire_volume_usd"
    
    mean_value = Column(Float, default=0.0, nullable=False)
    std_dev = Column(Float, default=0.0, nullable=False)
    p95_value = Column(Float, default=0.0, nullable=False)
    
    # Statistical window bounds
    window_start = Column(DateTime(timezone=True), nullable=False)
    window_end = Column(DateTime(timezone=True), nullable=False)
    calculated_at = Column(DateTime(timezone=True), nullable=False, index=True)
    
    # Optional distribution details (e.g., histogram bins, hourly weights)
    distribution_params = Column(JSONB().with_variant(JSON, "sqlite"), default=dict, nullable=False)

    # Relationships
    employee = relationship("Employee", back_populates="behavior_baselines")

    __table_args__ = (
        Index("ix_behavior_baselines_emp_metric", "employee_id", "metric_name"),
    )
