@echo off
echo Instalando Business Analyst Backend...

REM Crear entorno virtual
python -m venv venv

REM Activar entorno virtual
call venv\Scripts\activate

REM Actualizar pip
python -m pip install --upgrade pip

REM Instalar dependencias básicas primero
echo Instalando dependencias básicas...
pip install fastapi==0.104.1
pip install uvicorn[standard]==0.24.0
pip install python-multipart==0.0.6
pip install pydantic==2.5.0
pip install pydantic-settings==2.1.0
pip install python-dotenv==1.0.0
pip install sqlalchemy==2.0.23
pip install structlog==23.2.0

REM Instalar LangChain sin versiones específicas para evitar conflictos
echo Instalando LangChain...
pip install langchain
pip install langchain-community
pip install langchain-groq
pip install langchain-openai

REM Instalar dependencias adicionales
echo Instalando dependencias adicionales...
pip install httpx==0.25.2
pip install alembic==1.13.0

REM Crear archivo de configuración
if not exist .env (
    python create_env.py
)

echo.
echo Instalacion completada!
echo.
echo Para ejecutar el backend:
echo 1. Activa el entorno virtual: venv\Scripts\activate
echo 2. Configura tu .env con las API keys
echo 3. Ejecuta: python run.py
echo.
pause
