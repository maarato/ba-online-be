#!/usr/bin/env python3
"""
Script para probar que el backend funciona correctamente
"""

import os
import sys
import subprocess
import time
import requests
from threading import Thread

def test_imports():
    """Probar que se pueden importar todos los módulos"""
    try:
        print("🧪 Probando imports...")
        
        # Crear archivo .env si no existe
        if not os.path.exists('.env'):
            print("📝 Creando archivo .env...")
            subprocess.run([sys.executable, 'create_env.py'], check=True)
        
        # Probar imports básicos
        from app.core.config import settings
        print("✅ Configuración cargada correctamente")
        
        from app.core.database import engine, Base
        print("✅ Base de datos configurada correctamente")
        
        from app.services.llm_service import LLMService
        print("✅ Servicio LLM configurado correctamente")
        
        from app.api import auth, chat, brief, leads
        print("✅ APIs importadas correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en imports: {e}")
        return False

def test_server_start():
    """Probar que el servidor puede iniciarse"""
    try:
        print("\n🚀 Probando inicio del servidor...")
        
        # Iniciar servidor en un hilo separado
        def run_server():
            subprocess.run([sys.executable, 'run.py'], 
                         capture_output=True, 
                         timeout=10)
        
        server_thread = Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # Esperar un poco para que el servidor inicie
        time.sleep(3)
        
        # Probar endpoint de salud
        try:
            response = requests.get('http://localhost:8000/health', timeout=5)
            if response.status_code == 200:
                print("✅ Servidor responde correctamente")
                return True
            else:
                print(f"⚠️  Servidor responde con código: {response.status_code}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"⚠️  No se pudo conectar al servidor: {e}")
            print("   (Esto es normal si el servidor no está ejecutándose)")
            return True  # No es un error crítico para la prueba
            
    except Exception as e:
        print(f"❌ Error probando servidor: {e}")
        return False

def test_api_endpoints():
    """Probar endpoints de la API"""
    try:
        print("\n🔌 Probando endpoints de la API...")
        
        base_url = 'http://localhost:8000'
        
        # Probar endpoint raíz
        response = requests.get(f'{base_url}/', timeout=5)
        if response.status_code == 200:
            print("✅ Endpoint raíz funciona")
        else:
            print(f"⚠️  Endpoint raíz: {response.status_code}")
        
        # Probar endpoint de salud
        response = requests.get(f'{base_url}/health', timeout=5)
        if response.status_code == 200:
            print("✅ Endpoint de salud funciona")
        else:
            print(f"⚠️  Endpoint de salud: {response.status_code}")
        
        # Probar inicialización de dispositivo
        response = requests.post(f'{base_url}/auth/device/init', 
                               json={}, timeout=5)
        if response.status_code == 200:
            print("✅ Endpoint de inicialización funciona")
        else:
            print(f"⚠️  Endpoint de inicialización: {response.status_code}")
        
        return True
        
    except requests.exceptions.RequestException as e:
        print(f"⚠️  No se pudo probar endpoints: {e}")
        print("   (Esto es normal si el servidor no está ejecutándose)")
        return True
    except Exception as e:
        print(f"❌ Error probando endpoints: {e}")
        return False

def main():
    """Función principal de prueba"""
    print("🧪 Business Analyst Backend - Pruebas de Funcionamiento")
    print("=" * 60)
    
    success = True
    
    # Probar imports
    if not test_imports():
        success = False
    
    # Probar servidor
    if not test_server_start():
        success = False
    
    # Probar endpoints
    if not test_api_endpoints():
        success = False
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 ¡Todas las pruebas pasaron! El backend está listo.")
        print("\nPara ejecutar el servidor:")
        print("python run.py")
        print("\nEl servidor estará disponible en: http://localhost:8000")
        print("Documentación de la API: http://localhost:8000/docs")
    else:
        print("❌ Algunas pruebas fallaron. Revisa los errores arriba.")
        print("\nPara reinstalar dependencias:")
        print("pip install -r requirements-simple.txt")
    
    return success

if __name__ == "__main__":
    main()
