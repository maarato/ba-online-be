@echo off
echo 🧹 Business Analyst Backend - Instalación Limpia
echo ================================================

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

REM Desinstalar paquetes conflictivos si existen
echo 🧹 Limpiando dependencias conflictivas...
pip uninstall -y ollama pydantic httpx langchain langchain-community langchain-groq langchain-openai 2>nul

REM Instalar dependencias básicas primero
echo 📦 Instalando dependencias básicas...
pip install fastapi==0.104.1
pip install uvicorn[standard]==0.24.0
pip install python-multipart==0.0.6
pip install python-dotenv==1.0.0
pip install sqlalchemy==2.0.23
pip install structlog==23.2.0

REM Instalar Pydantic compatible
echo 📦 Instalando Pydantic compatible...
pip install "pydantic>=2.9.0,<3.0.0"
pip install pydantic-settings==2.1.0

REM Instalar HTTP compatible
echo 📦 Instalando HTTP compatible...
pip install "httpx>=0.27,<0.29"

REM Instalar LangChain
echo 📦 Instalando LangChain...
pip install langchain
pip install langchain-community
pip install langchain-groq
pip install langchain-openai

REM Instalar dependencias adicionales
echo 📦 Instalando dependencias adicionales...
pip install alembic==1.13.0

REM Crear archivo .env si no existe
if not exist .env (
    echo ⚙️ Creando archivo de configuración...
    python create_env.py
)

REM Probar importaciones
echo 🧪 Probando importaciones...
python test_imports.py

REM Probar instalación completa
echo 🧪 Probando instalación completa...
python test_backend.py

REM Probar chat (opcional)
echo 🧪 Probando chat Business Analyst...
echo (Esto requiere que el servidor esté ejecutándose)
echo python test_chat.py

echo.
echo 🎉 ¡Instalación limpia completada!
echo.
echo Para ejecutar el backend:
echo 1. Activa el entorno virtual: venv\Scripts\activate
echo 2. Configura tu .env con las API keys
echo 3. Ejecuta: python run.py
echo.
echo El servidor estará disponible en: http://localhost:8000
echo.
pause
