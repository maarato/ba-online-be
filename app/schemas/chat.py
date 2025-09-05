"""
Esquemas Pydantic para Chat
"""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChatMessageBase(BaseModel):
    role: str  # "user" o "bot"
    content: str

class ChatMessageCreate(ChatMessageBase):
    session_id: Optional[str] = None

class ChatMessageResponse(ChatMessageBase):
    id: int
    session_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    device_token: Optional[str] = None

class ChatResponse(BaseModel):
    message: str
    step: Optional[str] = None  # "asking" o "done"
    current_key: Optional[str] = None
    suggestions: Optional[List[str]] = None
    summary: Optional[str] = None

class ChatSessionResponse(BaseModel):
    id: int
    session_id: str
    current_step: str
    current_question_key: Optional[str] = None
    created_at: datetime
    last_activity: datetime
    
    class Config:
        from_attributes = True

class DeviceInitRequest(BaseModel):
    device_fingerprint: Optional[str] = None

class DeviceInitResponse(BaseModel):
    success: bool
    device_token: str
    fingerprint_salt: str
    message: str
