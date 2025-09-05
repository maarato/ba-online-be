"""
Configuración de la aplicación
"""

from pydantic_settings import BaseSettings
from typing import List
import os

class Settings(BaseSettings):
    # Configuración de la aplicación
    APP_NAME: str = "Business Analyst API"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Configuración del servidor
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS
    ALLOWED_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000,http://localhost:3001,http://127.0.0.1:3001"
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Convertir ALLOWED_ORIGINS string a lista"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]
    
    # Base de datos
    DATABASE_URL: str = "sqlite:///./business_analyst.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # LLM Configuration
    # Groq
    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama3-8b-8192"
    
    # OpenAI
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    
    # Configuración por defecto del LLM
    DEFAULT_LLM_PROVIDER: str = "groq"  # "groq" o "openai"
    
    # Configuración del chat
    MAX_CHAT_HISTORY: int = 50
    CHAT_TIMEOUT: int = 30
    
    # Configuración de autenticación
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Instancia global de configuración
settings = Settings()
