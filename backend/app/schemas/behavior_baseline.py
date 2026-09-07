from datetime import datetime
from uuid import UUID
from typing import Dict, Any
from pydantic import BaseModel, ConfigDict


class BehaviorBaselineBase(BaseModel):
    employee_id: UUID
    metric_name: str
    mean_value: float
    std_dev: float
    p95_value: float
    window_start: datetime
    window_end: datetime
    calculated_at: datetime
    distribution_params: Dict[str, Any] = {}


class BehaviorBaselineCreate(BehaviorBaselineBase):
    pass


class BehaviorBaselineResponse(BehaviorBaselineBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
