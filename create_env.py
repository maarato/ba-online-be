#!/usr/bin/env python3
"""
Script para crear el archivo .env por defecto
"""

import os

def create_env_file():
    """Crear archivo .env con configuración por defecto"""
    
    env_content = """# Configuración de la aplicación
APP_NAME="Business Analyst API"
VERSION="1.0.0"
DEBUG=false

# Configuración del servidor
HOST=0.0.0.0
PORT=8000

# CORS - URLs permitidas (separadas por coma, sin espacios)
ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000,http://localhost:3001,http://127.0.0.1:3001

# Base de datos
DATABASE_URL=sqlite:///./business_analyst.db

# Redis (opcional)
REDIS_URL=redis://localhost:6379

# LLM Configuration
# Groq
GROQ_API_KEY=
GROQ_MODEL=llama3-8b-8192

# OpenAI
OPENAI_API_KEY=
OPENAI_MODEL=gpt-3.5-turbo

# Proveedor por defecto (groq o openai)
DEFAULT_LLM_PROVIDER=groq

# Configuración del chat
MAX_CHAT_HISTORY=50
CHAT_TIMEOUT=30

# Configuración de autenticación
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
"""
    
    if not os.path.exists('.env'):
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        print("✅ Archivo .env creado exitosamente")
        print("⚠️  IMPORTANTE: Configura tus API keys en el archivo .env")
        print("   - GROQ_API_KEY=tu_groq_api_key")
        print("   - OPENAI_API_KEY=tu_openai_api_key")
    else:
        print("ℹ️  El archivo .env ya existe")

if __name__ == "__main__":
    create_env_file()
