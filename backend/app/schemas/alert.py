from datetime import datetime
from uuid import UUID
from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict
from app.models.alert import AlertSeverity, AlertStatus


class AlertBase(BaseModel):
    alert_id: str
    employee_id: UUID
    title: str
    description: Optional[str] = None
    severity: AlertSeverity = AlertSeverity.MEDIUM
    status: AlertStatus = AlertStatus.NEW
    risk_score_at_trigger: float
    trigger_reasons: Dict[str, Any] = {}
    triggered_at: datetime
    triaged_by_user_id: Optional[UUID] = None
    triaged_at: Optional[datetime] = None
    triage_notes: Optional[str] = None
    investigation_id: Optional[UUID] = None


class AlertCreate(BaseModel):
    alert_id: str
    employee_id: UUID
    title: str
    description: Optional[str] = None
    severity: AlertSeverity = AlertSeverity.MEDIUM
    risk_score_at_trigger: float
    trigger_reasons: Dict[str, Any] = {}


class AlertUpdate(BaseModel):
    severity: Optional[AlertSeverity] = None
    status: Optional[AlertStatus] = None
    triage_notes: Optional[str] = None
    investigation_id: Optional[UUID] = None


class AlertResponse(AlertBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
