"""
Business Analyst Backend API
Backend para el chatbot Business Analyst con integración de LLMs
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer
import uvicorn
import os
from dotenv import load_dotenv

from app.api import auth, chat, brief, leads
from app.core.config import settings
from app.core.database import engine, Base
from app.core.logging import setup_logging

# Cargar variables de entorno
load_dotenv()

# Configurar logging
setup_logging()

# Crear tablas de base de datos
Base.metadata.create_all(bind=engine)

# Crear aplicación FastAPI
app = FastAPI(
    title="Business Analyst API",
    description="API para el chatbot Business Analyst con integración de LLMs",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(brief.router, prefix="/brief", tags=["brief"])
app.include_router(leads.router, prefix="/leads", tags=["leads"])

@app.get("/")
async def root():
    """Endpoint de salud de la API"""
    return {
        "message": "Business Analyst API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
