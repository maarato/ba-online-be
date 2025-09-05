"""
Modelo de Lead
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class Lead(Base):
    __tablename__ = "leads"
    
    id = Column(Integer, primary_key=True, index=True)
    brief_id = Column(Integer, ForeignKey("project_briefs.id"), nullable=True)
    
    # Información de contacto
    name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    company = Column(String(255), nullable=True)
    
    # Información adicional
    contact_info = Column(JSON, nullable=True)  # Información adicional de contacto
    notes = Column(Text, nullable=True)
    
    # Estado del lead
    status = Column(String(50), default="new")  # new, contacted, qualified, converted, lost
    priority = Column(String(20), default="medium")  # low, medium, high
    
    # Metadatos
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relación con brief
    brief = relationship("ProjectBrief", foreign_keys=[brief_id])
    
    def to_dict(self):
        return {
            "id": self.id,
            "brief_id": self.brief_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "company": self.company,
            "contact_info": self.contact_info or {},
            "notes": self.notes,
            "status": self.status,
            "priority": self.priority,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
