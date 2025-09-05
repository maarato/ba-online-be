"""
API de autenticación y dispositivos
"""

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.chat import DeviceInitRequest, DeviceInitResponse
import uuid
import hashlib
import structlog

logger = structlog.get_logger()
router = APIRouter()

@router.post("/device/init", response_model=DeviceInitResponse)
async def init_device(
    request: DeviceInitRequest,
    db: Session = Depends(get_db)
):
    """
    Inicializar dispositivo y generar token de sesión
    """
    try:
        # Generar token único para el dispositivo
        device_token = f"device_{uuid.uuid4().hex[:16]}"
        
        # Generar salt para fingerprint si se proporciona
        fingerprint_salt = f"salt_{uuid.uuid4().hex[:16]}"
        
        logger.info("Dispositivo inicializado", device_token=device_token)
        
        return DeviceInitResponse(
            success=True,
            device_token=device_token,
            fingerprint_salt=fingerprint_salt,
            message="Dispositivo inicializado correctamente"
        )
        
    except Exception as e:
        logger.error("Error inicializando dispositivo", error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor"
        )
