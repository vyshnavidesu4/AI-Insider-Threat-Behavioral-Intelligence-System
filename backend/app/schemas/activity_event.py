from datetime import datetime
from uuid import UUID
from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict
from app.models.activity_event import EventType, SensitivityLevel


class ActivityEventBase(BaseModel):
    employee_id: UUID
    timestamp: datetime
    event_type: EventType
    source_ip: Optional[str] = None
    host_machine: Optional[str] = None
    target_resource: str
    sensitivity_level: SensitivityLevel = SensitivityLevel.INTERNAL
    volume_mb: float = 0.0
    event_metadata: Dict[str, Any] = {}
    is_anomalous: bool = False


class ActivityEventCreate(ActivityEventBase):
    pass


class ActivityEventResponse(ActivityEventBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
