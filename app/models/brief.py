"""
Modelo de Brief del proyecto
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from app.core.database import Base

class ProjectBrief(Base):
    __tablename__ = "project_briefs"
    
    id = Column(Integer, primary_key=True, index=True)
    business_goal = Column(Text, nullable=True)
    audience = Column(Text, nullable=True)
    use_cases = Column(JSON, nullable=True)  # Lista de strings
    data_sources = Column(JSON, nullable=True)  # Lista de strings
    integrations = Column(JSON, nullable=True)  # Lista de strings
    constraints = Column(JSON, nullable=True)  # Lista de strings
    budget_range = Column(String(50), nullable=True)
    timeline = Column(String(100), nullable=True)
    
    # Metadatos
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Información del dispositivo/sesión
    device_token = Column(String(255), nullable=True)
    session_id = Column(String(255), nullable=True)
    
    def to_dict(self):
        """Convertir a diccionario"""
        return {
            "id": self.id,
            "business_goal": self.business_goal,
            "audience": self.audience,
            "use_cases": self.use_cases or [],
            "data_sources": self.data_sources or [],
            "integrations": self.integrations or [],
            "constraints": self.constraints or [],
            "budget_range": self.budget_range,
            "timeline": self.timeline,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
