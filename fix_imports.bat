@echo off
echo 🔧 Business Analyst Backend - Corrección de Importaciones
echo ========================================================

REM Activar entorno virtual
call venv\Scripts\activate

echo 🧹 Desinstalando paquetes problemáticos...
pip uninstall -y langchain langchain-community langchain-groq langchain-openai 2>nul

echo 📦 Reinstalando LangChain con versiones compatibles...
pip install langchain
pip install langchain-community
pip install langchain-groq
pip install langchain-openai

echo 🧪 Probando importaciones...
python test_imports.py

echo.
echo ✅ Corrección completada!
echo.
echo Para ejecutar el servidor:
echo python run.py
echo.
pause
