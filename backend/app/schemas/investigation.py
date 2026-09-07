from datetime import datetime
from uuid import UUID
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict
from app.models.investigation import InvestigationStatus, InvestigationPriority


class InvestigationBase(BaseModel):
    case_number: str
    title: str
    description: Optional[str] = None
    status: InvestigationStatus = InvestigationStatus.OPEN
    priority: InvestigationPriority = InvestigationPriority.P2_HIGH
    target_employee_id: UUID
    assigned_to_user_id: Optional[UUID] = None
    hypothesis: Optional[str] = None
    timeline_events: List[Dict[str, Any]] = []
    findings_summary: Optional[str] = None


class InvestigationCreate(BaseModel):
    case_number: str
    title: str
    description: Optional[str] = None
    priority: InvestigationPriority = InvestigationPriority.P2_HIGH
    target_employee_id: UUID
    assigned_to_user_id: Optional[UUID] = None
    hypothesis: Optional[str] = None


class InvestigationUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[InvestigationStatus] = None
    priority: Optional[InvestigationPriority] = None
    assigned_to_user_id: Optional[UUID] = None
    hypothesis: Optional[str] = None
    timeline_events: Optional[List[Dict[str, Any]]] = None
    findings_summary: Optional[str] = None


class InvestigationResponse(InvestigationBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
