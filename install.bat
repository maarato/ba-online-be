@echo off
echo Instalando Business Analyst Backend...

REM Crear entorno virtual
python -m venv venv

REM Activar entorno virtual
call venv\Scripts\activate

REM Instalar dependencias
pip install -r requirements.txt

REM Copiar archivo de configuración
if not exist .env (
    copy env.example .env
    echo Archivo .env creado. Por favor, configura tus API keys.
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
