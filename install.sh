#!/bin/bash

echo "Instalando Business Analyst Backend..."

# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
source venv/bin/activate

# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias básicas primero
echo "Instalando dependencias básicas..."
pip install fastapi==0.104.1
pip install uvicorn[standard]==0.24.0
pip install python-multipart==0.0.6
pip install pydantic==2.5.0
pip install pydantic-settings==2.1.0
pip install python-dotenv==1.0.0
pip install sqlalchemy==2.0.23
pip install structlog==23.2.0

# Instalar LangChain sin versiones específicas para evitar conflictos
echo "Instalando LangChain..."
pip install langchain
pip install langchain-community
pip install langchain-groq
pip install langchain-openai

# Instalar dependencias adicionales
echo "Instalando dependencias adicionales..."
pip install httpx==0.25.2
pip install alembic==1.13.0

# Copiar archivo de configuración
if [ ! -f .env ]; then
    cp env.example .env
    echo "Archivo .env creado. Por favor, configura tus API keys."
fi

echo ""
echo "Instalacion completada!"
echo ""
echo "Para ejecutar el backend:"
echo "1. Activa el entorno virtual: source venv/bin/activate"
echo "2. Configura tu .env con las API keys"
echo "3. Ejecuta: python run.py"
echo ""
