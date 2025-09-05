"""
API para gestión de leads
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.lead import LeadCreateRequest, LeadCreateResponse, LeadCreate
from app.models.lead import Lead
import structlog

logger = structlog.get_logger()
router = APIRouter()

@router.post("/create", response_model=LeadCreateResponse)
async def create_lead(
    request: LeadCreateRequest,
    db: Session = Depends(get_db)
):
    """
    Crear nuevo lead
    """
    try:
        # Crear nuevo lead
        lead = Lead(
            brief_id=request.brief_id,
            contact_info=request.contact_info,
            status="new",
            priority="medium"
        )
        
        db.add(lead)
        db.commit()
        db.refresh(lead)
        
        logger.info("Lead creado exitosamente", lead_id=lead.id)
        
        return LeadCreateResponse(
            success=True,
            lead_id=lead.id,
            message="Lead creado exitosamente. Te contactaremos pronto."
        )
        
    except Exception as e:
        logger.error("Error creando lead", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Error creando lead"
        )

@router.get("/{lead_id}")
async def get_lead(lead_id: int, db: Session = Depends(get_db)):
    """
    Obtener lead por ID
    """
    try:
        lead = db.query(Lead).filter(Lead.id == lead_id).first()
        if not lead:
            raise HTTPException(status_code=404, detail="Lead no encontrado")
        
        return lead.to_dict()
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error obteniendo lead", error=str(e), lead_id=lead_id)
        raise HTTPException(
            status_code=500,
            detail="Error obteniendo lead"
        )
