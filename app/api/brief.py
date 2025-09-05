"""
API para gestión de briefs
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.brief import BriefSaveRequest, BriefSaveResponse, ProjectBriefCreate
from app.models.brief import ProjectBrief
import structlog

logger = structlog.get_logger()
router = APIRouter()

@router.post("/save", response_model=BriefSaveResponse)
async def save_brief(
    request: BriefSaveRequest,
    db: Session = Depends(get_db)
):
    """
    Guardar brief del proyecto
    """
    try:
        # Crear nuevo brief
        brief = ProjectBrief(
            business_goal=request.brief.business_goal,
            audience=request.brief.audience,
            use_cases=request.brief.use_cases,
            data_sources=request.brief.data_sources,
            integrations=request.brief.integrations,
            constraints=request.brief.constraints,
            budget_range=request.brief.budget_range,
            timeline=request.brief.timeline,
            device_token=request.device_token,
            session_id=request.session_id
        )
        
        db.add(brief)
        db.commit()
        db.refresh(brief)
        
        logger.info("Brief guardado exitosamente", brief_id=brief.id)
        
        return BriefSaveResponse(
            success=True,
            brief_id=brief.id,
            message="Brief guardado exitosamente"
        )
        
    except Exception as e:
        logger.error("Error guardando brief", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Error guardando brief del proyecto"
        )

@router.get("/{brief_id}")
async def get_brief(brief_id: int, db: Session = Depends(get_db)):
    """
    Obtener brief por ID
    """
    try:
        brief = db.query(ProjectBrief).filter(ProjectBrief.id == brief_id).first()
        if not brief:
            raise HTTPException(status_code=404, detail="Brief no encontrado")
        
        return brief.to_dict()
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Error obteniendo brief", error=str(e), brief_id=brief_id)
        raise HTTPException(
            status_code=500,
            detail="Error obteniendo brief"
        )
