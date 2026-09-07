from datetime import datetime
from uuid import UUID
from typing import Optional, Dict, Any
from pydantic import BaseModel, ConfigDict
from app.models.department import DepartmentCode, RiskTier


class DepartmentBase(BaseModel):
    code: DepartmentCode
    name: str
    description: Optional[str] = None
    risk_tier: RiskTier = RiskTier.MEDIUM
    data_access_policies: Dict[str, Any] = {}


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentResponse(DepartmentBase):
    id: UUID
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
