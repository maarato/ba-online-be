#!/usr/bin/env python3
"""
Script para probar las importaciones de LangChain
"""

def test_langchain_imports():
    """Probar que se pueden importar todos los módulos de LangChain"""
    try:
        print("🧪 Probando importaciones de LangChain...")
        
        # Probar importaciones básicas
        import langchain
        print(f"✅ LangChain: {langchain.__version__}")
        
        import langchain_community
        print(f"✅ LangChain Community: {langchain_community.__version__}")
        
        import langchain_core
        print(f"✅ LangChain Core: {langchain_core.__version__}")
        
        # Probar importaciones específicas
        from langchain_core.messages import HumanMessage, SystemMessage
        print("✅ LangChain Core Messages")
        
        from langchain_core.prompts import ChatPromptTemplate
        print("✅ LangChain Core Prompts")
        
        # Probar ChatGroq
        try:
            from langchain_groq import ChatGroq
            print("✅ LangChain Groq")
        except ImportError as e:
            print(f"❌ Error importando LangChain Groq: {e}")
            return False
        
        # Probar ChatOpenAI
        try:
            from langchain_openai import ChatOpenAI
            print("✅ LangChain OpenAI")
        except ImportError as e:
            print(f"❌ Error importando LangChain OpenAI: {e}")
            return False
        
        # Probar que se pueden crear instancias
        print("\n🧪 Probando creación de instancias...")
        
        # Probar ChatGroq (sin API key)
        try:
            groq = ChatGroq(
                groq_api_key="test-key",
                model_name="llama3-8b-8192",
                temperature=0.7
            )
            print("✅ ChatGroq se puede instanciar")
        except Exception as e:
            print(f"⚠️  ChatGroq error (esperado sin API key): {e}")
        
        # Probar ChatOpenAI (sin API key)
        try:
            openai = ChatOpenAI(
                openai_api_key="test-key",
                model_name="gpt-3.5-turbo",
                temperature=0.7
            )
            print("✅ ChatOpenAI se puede instanciar")
        except Exception as e:
            print(f"⚠️  ChatOpenAI error (esperado sin API key): {e}")
        
        print("\n🎉 ¡Todas las importaciones funcionan correctamente!")
        return True
        
    except ImportError as e:
        print(f"❌ Error importando: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_llm_service():
    """Probar que el servicio LLM se puede importar"""
    try:
        print("\n🧪 Probando servicio LLM...")
        
        from app.services.llm_service import LLMService
        print("✅ Servicio LLM importado correctamente")
        
        # Probar que se puede instanciar (sin API key)
        try:
            service = LLMService("groq")
            print("✅ Servicio LLM se puede instanciar")
        except ValueError as e:
            if "no está configurada" in str(e):
                print("✅ Servicio LLM funciona (error esperado sin API key)")
            else:
                print(f"❌ Error inesperado: {e}")
                return False
        except Exception as e:
            print(f"❌ Error inesperado: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error probando servicio LLM: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Business Analyst Backend - Prueba de Importaciones")
    print("=" * 60)
    
    success = True
    
    # Probar importaciones de LangChain
    if not test_langchain_imports():
        success = False
    
    # Probar servicio LLM
    if not test_llm_service():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ¡Todas las pruebas pasaron! Las importaciones funcionan correctamente.")
        print("\nPara ejecutar el servidor:")
        print("python run.py")
    else:
        print("❌ Algunas pruebas fallaron. Revisa los errores arriba.")
        print("\nPara reinstalar dependencias:")
        print("pip install -r requirements-clean.txt")
    
    return success
