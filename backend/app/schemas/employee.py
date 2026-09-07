from datetime import datetime, date
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict
from app.models.employee import ClearanceLevel, EmploymentStatus
from app.schemas.department import DepartmentResponse


class EmployeeBase(BaseModel):
    employee_number: str
    department_id: UUID
    full_name: str
    email: EmailStr
    job_title: str
    clearance_level: ClearanceLevel = ClearanceLevel.STANDARD
    is_privileged: bool = False
    status: EmploymentStatus = EmploymentStatus.ACTIVE
    hire_date: Optional[date] = None


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    department_id: Optional[UUID] = None
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    job_title: Optional[str] = None
    clearance_level: Optional[ClearanceLevel] = None
    is_privileged: Optional[bool] = None
    status: Optional[EmploymentStatus] = None


class EmployeeResponse(EmployeeBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    department: Optional[DepartmentResponse] = None

    model_config = ConfigDict(from_attributes=True)
