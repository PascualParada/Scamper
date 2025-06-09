#!/usr/bin/env python3
"""
Sistema Multi-Agente SCAMPER
Potencia tu creatividad con técnicas de innovación sistemática
"""

import asyncio
import sys
from config.settings import settings
from interface.chatbot import chatbot

def print_banner():
    """Imprime el banner del sistema"""
    banner = """
    ╔══════════════════════════════════════════════════════════════╗
    ║                    SISTEMA SCAMPER                           ║
    ║              Potencia tu Creatividad con IA                  ║
    ║                                                              ║
    ║  S - Sustituir    |  C - Combinar     |  A - Adaptar        ║
    ║  M - Modificar    |  P - Otros Usos   |  E - Eliminar       ║
    ║  R - Reorganizar                                             ║
    ╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)

def validate_environment():
    """Valida que el entorno esté configurado correctamente"""
    try:
        settings.validate()
        print("✅ Configuración validada correctamente")
        return True
    except ValueError as e:
        print(f"❌ Error de configuración: {e}")
        print("\n🔧 Para configurar el sistema:")
        print("1. Crea un archivo .env en la raíz del proyecto")
        print("2. Agrega tu API key: GEMINI_API_KEY=tu_api_key_aquí")
        print("3. Obtén tu API key en: https://makersuite.google.com/app/apikey")
        return False

async def main():
    """Función principal del sistema"""
    print_banner()
    
    # Validar configuración
    if not validate_environment():
        sys.exit(1)
    
    # Mostrar información del sistema
    print(f"🤖 Modelo: {settings.GEMINI_MODEL}")
    print(f"🎛️  Temperatura: {settings.GEMINI_TEMPERATURE}")
    print(f"💭 Ideas máximas por técnica: {settings.MAX_IDEAS_PER_TECHNIQUE}")
    print(f"⚡ Ejecución paralela: {'Habilitada' if settings.ENABLE_PARALLEL_EXECUTION else 'Deshabilitada'}")
    
    try:
        # Iniciar chatbot
        await chatbot.start_conversation()
        
    except KeyboardInterrupt:
        print("\n\n👋 Sistema cerrado por el usuario")
    except Exception as e:
        print(f"\n❌ Error crítico: {e}")
        print("Por favor, revisa tu configuración e intenta de nuevo")

def run_demo():
    """Ejecuta una demostración rápida del sistema"""
    print_banner()
    print("🚀 MODO DEMOSTRACIÓN")
    print("=" * 50)
    
    async def demo():
        # Validar configuración
        if not validate_environment():
            return
        
        # Problema de ejemplo
        problema_demo = "Quiero aumentar la participación de los empleados en las reuniones de equipo"
        contexto_demo = "Empresa de tecnología, equipos remotos, reuniones virtuales semanales"
        
        print(f"📝 Problema de ejemplo: {problema_demo}")
        print(f"🔍 Contexto: {contexto_demo}")
        print("\n🚀 Aplicando SCAMPER...")
        
        try:
            response = await chatbot.process_single_problem(problema_demo, contexto_demo)
            chatbot._display_results(response)
        except Exception as e:
            print(f"❌ Error en demostración: {e}")
    
    asyncio.run(demo())

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Sistema Multi-Agente SCAMPER")
    parser.add_argument("--demo", action="store_true", help="Ejecutar demostración")
    parser.add_argument("--version", action="version", version="SCAMPER System v1.0")
    
    args = parser.parse_args()
    
    if args.demo:
        run_demo()
    else:
        asyncio.run(main())