"""
Esquemas Pydantic para Lead
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class LeadBase(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    contact_info: Optional[Dict[str, Any]] = None
    notes: Optional[str] = None
    status: str = "new"
    priority: str = "medium"

class LeadCreate(LeadBase):
    brief_id: Optional[int] = None

class LeadUpdate(LeadBase):
    pass

class LeadResponse(LeadBase):
    id: int
    brief_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class LeadCreateRequest(BaseModel):
    brief_id: Optional[int] = None
    contact_info: Optional[Dict[str, Any]] = None

class LeadCreateResponse(BaseModel):
    success: bool
    lead_id: Optional[int] = None
    message: str
