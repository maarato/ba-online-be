@echo off
echo 🚀 Business Analyst Backend - Inicio Rápido
echo ==========================================

REM Verificar si Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado. Por favor, instala Python 3.8+ desde https://python.org
    pause
    exit /b 1
)

echo ✅ Python detectado

REM Crear entorno virtual si no existe
if not exist venv (
    echo 📦 Creando entorno virtual...
    python -m venv venv
)

REM Activar entorno virtual
echo 🔧 Activando entorno virtual...
call venv\Scripts\activate

REM Actualizar pip
echo 📥 Actualizando pip...
python -m pip install --upgrade pip

REM Instalar dependencias
echo 📦 Instalando dependencias...
pip install fastapi==0.104.1 uvicorn[standard]==0.24.0 python-multipart==0.0.6
pip install pydantic==2.5.0 pydantic-settings==2.1.0 python-dotenv==1.0.0
pip install sqlalchemy==2.0.23 structlog==23.2.0 httpx==0.25.2 alembic==1.13.0
pip install langchain langchain-community langchain-groq langchain-openai

REM Crear archivo .env si no existe
if not exist .env (
    echo ⚙️ Creando archivo de configuración...
    python create_env.py
    echo.
)

REM Probar instalación
echo 🧪 Probando instalación...
python test_backend.py

echo.
echo 🎉 ¡Instalación completada!
echo.
echo Para ejecutar el backend:
echo 1. Activa el entorno virtual: venv\Scripts\activate
echo 2. Configura tu .env con las API keys
echo 3. Ejecuta: python run.py
echo.
echo El servidor estará disponible en: http://localhost:8000
echo.
pause
