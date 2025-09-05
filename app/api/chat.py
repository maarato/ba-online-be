"""
API de chat con LLM
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.chat import ChatRequest, ChatResponse, ChatMessageCreate
from app.services.llm_service import LLMService
from app.models.chat import ChatSession, ChatMessage
from app.models.brief import ProjectBrief
import uuid
import structlog
from datetime import datetime

logger = structlog.get_logger()
router = APIRouter()

@router.post("/stream", response_model=ChatResponse)
async def chat_stream(
    request: ChatRequest,
    db: Session = Depends(get_db)
):
    """
    Procesar mensaje del chat y generar respuesta del LLM
    """
    try:
        # Obtener o crear sesión de chat
        session = await get_or_create_chat_session(db, request.session_id, request.device_token)
        
        # Guardar mensaje del usuario
        user_message = ChatMessage(
            session_id=session.id,
            role="user",
            content=request.message
        )
        db.add(user_message)
        db.commit()
        
        # Obtener brief actual
        brief_data = await get_current_brief_data(db, session.id)
        
        # Generar respuesta con LLM
        llm_service = LLMService()
        llm_response = llm_service.generate_business_analyst_response(
            user_message=request.message,
            brief_data=brief_data,
            current_step=session.current_step,
            current_question_key=session.current_question_key
        )
        
        # Guardar respuesta del bot
        bot_message = ChatMessage(
            session_id=session.id,
            role="bot",
            content=llm_response["message"]
        )
        db.add(bot_message)
        
        # Actualizar estado de la sesión
        session.current_step = llm_response.get("step", session.current_step)
        session.current_question_key = llm_response.get("current_key")
        session.last_activity = datetime.utcnow()
        
        db.commit()
        
        # Preparar respuesta
        response = ChatResponse(
            message=llm_response["message"],
            step=llm_response.get("step"),
            current_key=llm_response.get("current_key"),
            suggestions=llm_response.get("suggestions"),
            summary=llm_response.get("summary")
        )
        
        logger.info("Respuesta de chat generada", session_id=session.session_id)
        return response
        
    except Exception as e:
        logger.error("Error procesando chat", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Error procesando mensaje del chat"
        )

async def get_or_create_chat_session(db: Session, session_id: str = None, device_token: str = None):
    """Obtener o crear sesión de chat"""
    if session_id:
        session = db.query(ChatSession).filter(ChatSession.session_id == session_id).first()
        if session:
            return session
    
    # Crear nueva sesión
    new_session_id = session_id or f"session_{uuid.uuid4().hex[:16]}"
    session = ChatSession(
        session_id=new_session_id,
        device_token=device_token,
        current_step="intro"
    )
    db.add(session)
    db.commit()
    db.refresh(session)
    
    return session

async def get_current_brief_data(db: Session, session_id: int) -> dict:
    """Obtener datos actuales del brief"""
    # Por ahora retornamos un diccionario vacío
    # En una implementación completa, esto obtendría los datos del brief asociado
    return {
        "business_goal": None,
        "audience": None,
        "use_cases": [],
        "data_sources": [],
        "integrations": [],
        "constraints": [],
        "budget_range": None,
        "timeline": None
    }
