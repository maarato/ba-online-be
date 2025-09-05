"""
Esquemas Pydantic para Brief
"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProjectBriefBase(BaseModel):
    business_goal: Optional[str] = None
    audience: Optional[str] = None
    use_cases: List[str] = []
    data_sources: List[str] = []
    integrations: List[str] = []
    constraints: List[str] = []
    budget_range: Optional[str] = None
    timeline: Optional[str] = None

class ProjectBriefCreate(ProjectBriefBase):
    device_token: Optional[str] = None
    session_id: Optional[str] = None

class ProjectBriefUpdate(ProjectBriefBase):
    pass

class ProjectBriefResponse(ProjectBriefBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class BriefSaveRequest(BaseModel):
    brief: ProjectBriefBase
    device_token: Optional[str] = None
    session_id: Optional[str] = None

class BriefSaveResponse(BaseModel):
    success: bool
    brief_id: Optional[int] = None
    message: str
