#!/usr/bin/env python3
"""
Sistema Multi-Agente SCAMPER
Potencia tu creatividad con técnicas de innovación sistemática
"""

import asyncio
import sys
from config.settings import settings
from interface.chatbot import chatbot
from typing import Optional, Dict, Any # Added Dict, Any
from models.schemas import ScamperResponse # Assuming chatbot.process_single_problem returns this


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


async def get_scamper_ideas_async(problem: str, context: Optional[str] = None) -> ScamperResponse:
    """Helper async function to call the chatbot's processing method."""
    # This reuses the chatbot instance already imported.
    return await chatbot.process_single_problem(problem, context)

def get_scamper_ideas_for_gui(problem: str, context: Optional[str] = None) -> Dict[str, Any]:
    """
    Recommended entry point for GUI applications to fetch SCAMPER ideas.

    This function handles the asynchronous call to the chatbot and converts the
    SCAMPER response into a standard Python dictionary.

    Args:
        problem: The problem statement or question to brainstorm ideas for.
        context: Optional additional context for the problem.

    Returns:
        A dictionary containing the SCAMPER ideas.
        On success, the dictionary typically includes keys like 'original_problem',
        'scamper_technique', 'results' (a list of ideas for each technique),
        and 'summary'. The exact structure is defined by ScamperResponse.model_dump().
        On failure (e.g., API error, internal error), it returns a dictionary
        with an 'error' key (e.g., {"error": "description", "details": "..."}).

    Note:
        The GUI is responsible for validating the `problem` and `context` strings
        (e.g., for length, content) before passing them to this function if needed.
        This function assumes the application's environment (e.g., API keys) is
        already validated and loaded, typically done at application startup.
    """
    try:
        # Run the async function
        response_model = asyncio.run(get_scamper_ideas_async(problem, context))
        # Convert Pydantic model to dictionary
        return response_model.model_dump()
    except Exception as e:
        # Handle potential exceptions during the async call or model conversion
        # Log the error server-side if possible
        print(f"Error in get_scamper_ideas_for_gui: {e}") # Or use proper logging
        return {"error": str(e), "details": "Failed to generate SCAMPER ideas."}

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Sistema Multi-Agente SCAMPER")
    parser.add_argument("--demo", action="store_true", help="Ejecutar demostración")
    parser.add_argument("--version", action="version", version="SCAMPER System v1.0")
    parser.add_argument("--get_ideas", type=str, help="Problem description for GUI function test")
    parser.add_argument("--get_ideas_context", type=str, help="Optional context for GUI function test")
    
    args = parser.parse_args()
    
    if args.get_ideas:
        if not validate_environment(): # Ensure environment is validated first
            sys.exit(1)
        print("🧪 Testing get_scamper_ideas_for_gui...")
        output = get_scamper_ideas_for_gui(args.get_ideas, args.get_ideas_context)
        import json
        print(json.dumps(output, indent=2, ensure_ascii=False)) # ensure_ascii for non-latin chars
    elif args.demo:
        run_demo()
    else:
        asyncio.run(main())
