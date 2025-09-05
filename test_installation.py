#!/usr/bin/env python3
"""
Script para probar la instalación del backend
"""

def test_imports():
    """Probar que todas las dependencias se pueden importar"""
    try:
        print("Probando imports...")
        
        # FastAPI
        import fastapi
        print("✅ FastAPI:", fastapi.__version__)
        
        # Uvicorn
        import uvicorn
        print("✅ Uvicorn:", uvicorn.__version__)
        
        # Pydantic
        import pydantic
        print("✅ Pydantic:", pydantic.__version__)
        
        # SQLAlchemy
        import sqlalchemy
        print("✅ SQLAlchemy:", sqlalchemy.__version__)
        
        # LangChain
        import langchain
        print("✅ LangChain:", langchain.__version__)
        
        # LangChain Community
        import langchain_community
        print("✅ LangChain Community:", langchain_community.__version__)
        
        # LangChain Groq
        import langchain_groq
        print("✅ LangChain Groq:", langchain_groq.__version__)
        
        # LangChain OpenAI
        import langchain_openai
        print("✅ LangChain OpenAI:", langchain_openai.__version__)
        
        # Structlog
        import structlog
        print("✅ Structlog:", structlog.__version__)
        
        print("\n🎉 ¡Todas las dependencias se instalaron correctamente!")
        return True
        
    except ImportError as e:
        print(f"❌ Error importando: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_llm_services():
    """Probar que los servicios de LLM se pueden inicializar"""
    try:
        print("\nProbando servicios de LLM...")
        
        from app.services.llm_service import LLMService
        
        # Probar con Groq (si está configurado)
        try:
            groq_service = LLMService("groq")
            print("✅ Servicio Groq inicializado correctamente")
        except Exception as e:
            print(f"⚠️  Servicio Groq no disponible: {e}")
        
        # Probar con OpenAI (si está configurado)
        try:
            openai_service = LLMService("openai")
            print("✅ Servicio OpenAI inicializado correctamente")
        except Exception as e:
            print(f"⚠️  Servicio OpenAI no disponible: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando servicios de LLM: {e}")
        return False

def test_database():
    """Probar que la base de datos se puede inicializar"""
    try:
        print("\nProbando base de datos...")
        
        from app.core.database import engine, Base
        from app.models.brief import ProjectBrief
        from app.models.chat import ChatSession, ChatMessage
        from app.models.lead import Lead
        
        # Crear tablas
        Base.metadata.create_all(bind=engine)
        print("✅ Base de datos inicializada correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando base de datos: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Probando instalación del Business Analyst Backend...\n")
    
    success = True
    
    # Probar imports
    if not test_imports():
        success = False
    
    # Probar servicios de LLM
    if not test_llm_services():
        success = False
    
    # Probar base de datos
    if not test_database():
        success = False
    
    if success:
        print("\n🎉 ¡Todas las pruebas pasaron! El backend está listo para usar.")
        print("\nPara ejecutar el servidor:")
        print("python run.py")
    else:
        print("\n❌ Algunas pruebas fallaron. Revisa los errores arriba.")
        print("\nPara reinstalar dependencias:")
        print("pip install -r requirements-simple.txt")
