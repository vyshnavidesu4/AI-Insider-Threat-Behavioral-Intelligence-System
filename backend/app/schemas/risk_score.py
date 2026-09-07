from datetime import datetime
from uuid import UUID
from typing import Dict, Any
from pydantic import BaseModel, ConfigDict, Field


class RiskScoreBase(BaseModel):
    employee_id: UUID
    calculated_at: datetime
    
    # 5 Explicit component scores (0-100)
    behavioral_anomalies_score: float = Field(default=0.0, ge=0.0, le=100.0, description="Weight: 35%")
    privilege_misuse_score: float = Field(default=0.0, ge=0.0, le=100.0, description="Weight: 25%")
    data_access_violations_score: float = Field(default=0.0, ge=0.0, le=100.0, description="Weight: 20%")
    access_pattern_deviations_score: float = Field(default=0.0, ge=0.0, le=100.0, description="Weight: 10%")
    historical_security_events_score: float = Field(default=0.0, ge=0.0, le=100.0, description="Weight: 10%")
    
    # Final composite score (0-100)
    composite_score: float = Field(default=0.0, ge=0.0, le=100.0, description="Weighted composite")
    
    risk_factors: Dict[str, Any] = Field(default_factory=dict, description="Human-readable rationale and top driver tags")


class RiskScoreCreate(RiskScoreBase):
    pass


class RiskScoreResponse(RiskScoreBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
