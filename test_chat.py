#!/usr/bin/env python3
"""
Script para probar el chat Business Analyst
"""

import requests
import json
import time

def test_chat_flow():
    """Probar el flujo completo del chat"""
    base_url = "http://localhost:8000"
    
    print("🧪 Probando flujo de chat Business Analyst...")
    
    # Mensajes de prueba
    test_messages = [
        "inicio",  # Mensaje de inicio
        "Sí, estoy listo",  # Confirmación
        "Quiero crear una plataforma de e-commerce",  # Objetivo
        "Empresas pequeñas y medianas",  # Audiencia
        "Catálogo de productos, carrito de compras, sistema de pagos",  # Funcionalidades
        "Tenemos una base de datos de productos en Excel",  # Fuentes de datos
        "PayPal, Stripe, sistema de inventario",  # Integraciones
        "Entre 30-80k",  # Presupuesto
        "6 meses"  # Timeline
    ]
    
    session_id = f"test_session_{int(time.time())}"
    
    for i, message in enumerate(test_messages):
        print(f"\n📝 Mensaje {i+1}: {message}")
        
        try:
            response = requests.post(
                f"{base_url}/chat/stream",
                json={
                    "message": message,
                    "session_id": session_id,
                    "device_token": "test_token"
                },
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Respuesta: {data['message'][:100]}...")
                print(f"   Paso: {data.get('step', 'N/A')}")
                print(f"   Clave actual: {data.get('current_key', 'N/A')}")
                
                if data.get('suggestions'):
                    print(f"   Sugerencias: {len(data['suggestions'])} encontradas")
                
            else:
                print(f"❌ Error: {response.status_code} - {response.text}")
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error de conexión: {e}")
            return False
        
        # Pequeña pausa entre mensajes
        time.sleep(1)
    
    print("\n🎉 ¡Flujo de chat completado exitosamente!")
    return True

def test_api_endpoints():
    """Probar endpoints básicos"""
    base_url = "http://localhost:8000"
    
    print("🔌 Probando endpoints de la API...")
    
    # Probar endpoint de salud
    try:
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Endpoint de salud funciona")
        else:
            print(f"❌ Endpoint de salud: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error probando salud: {e}")
        return False
    
    # Probar inicialización de dispositivo
    try:
        response = requests.post(f"{base_url}/auth/device/init", json={}, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Inicialización de dispositivo: {data['device_token']}")
        else:
            print(f"❌ Inicialización de dispositivo: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error probando inicialización: {e}")
        return False
    
    return True

def main():
    """Función principal de prueba"""
    print("🧪 Business Analyst Backend - Prueba de Chat")
    print("=" * 50)
    
    # Probar endpoints básicos
    if not test_api_endpoints():
        print("\n❌ Fallaron las pruebas básicas")
        return False
    
    # Probar flujo de chat
    if not test_chat_flow():
        print("\n❌ Falló el flujo de chat")
        return False
    
    print("\n🎉 ¡Todas las pruebas pasaron!")
    print("\nEl chat Business Analyst está funcionando correctamente.")
    print("Puedes probarlo en el frontend en: http://localhost:3000")
    
    return True

if __name__ == "__main__":
    main()
