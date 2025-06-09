import asyncio
from typing import Optional
from models.schemas import UserInput, ScamperResponse
from agents.orchestrator import orchestrator

class ScamperChatbot:
    """Interfaz conversacional para el sistema SCAMPER"""
    
    def __init__(self):
        self.name = "SCAMPER Assistant"
        self.session_active = False
    
    def welcome_message(self) -> str:
        """Mensaje de bienvenida"""
        return """
🎯 ¡Hola! Soy tu asistente SCAMPER para potenciar tu creatividad.

SCAMPER es una técnica que te ayuda a generar ideas innovadoras através de 7 enfoques:
• SUSTITUIR: ¿Qué se puede reemplazar?
• COMBINAR: ¿Qué se puede fusionar?
• ADAPTAR: ¿Qué se puede adaptar de otros contextos?
• MODIFICAR: ¿Qué se puede amplificar o reducir?
• OTROS USOS: ¿Para qué más se puede usar?
• ELIMINAR: ¿Qué se puede simplificar?
• INVERTIR: ¿Qué se puede reorganizar?

Describe tu problema o desafío creativo y yo aplicaré todas las técnicas SCAMPER para generar ideas innovadoras.

¿Cuál es el problema o desafío en el que necesitas ayuda?
        """
    
    async def start_conversation(self):
        """Inicia una conversación interactiva con el usuario"""
        print(self.welcome_message())
        self.session_active = True
        
        while self.session_active:
            try:
                # Obtener entrada del usuario
                user_input = await self._get_user_input()
                
                if user_input is None:
                    continue
                
                # Procesar con SCAMPER
                print("\n🚀 Aplicando técnicas SCAMPER...")
                print("=" * 50)
                
                response = await orchestrator.process_user_input(user_input)
                
                # Mostrar resultados
                self._display_results(response)
                
                # Preguntar si quiere continuar
                if not self._ask_continue():
                    self.session_active = False
                    print("\n👋 ¡Gracias por usar SCAMPER! ¡Que tengas mucho éxito con tus ideas!")
                
            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta luego!")
                self.session_active = False
            except Exception as e:
                print(f"\n❌ Error inesperado: {e}")
                print("Intenta de nuevo...")
    
    async def _get_user_input(self) -> Optional[UserInput]:
        """Obtiene y valida la entrada del usuario"""
        
        # Obtener problema principal
        print("\n" + "=" * 50)
        problem = input("📝 Describe tu problema o desafío: ").strip()
        
        if not problem:
            print("⚠️  Por favor, describe un problema válido.")
            return None
        
        if len(problem) < 10:
            print("⚠️  Por favor, proporciona más detalles (mínimo 10 caracteres).")
            return None
        
        # Obtener contexto opcional
        print("\n💡 Contexto adicional (opcional):")
        print("   Ejemplos: industria, público objetivo, limitaciones, etc.")
        context = input("🔍 Contexto: ").strip()
        
        context = context if context else None
        
        return UserInput(problem=problem, context=context)
    
    def _display_results(self, response: ScamperResponse):
        """
        Muestra los resultados de forma organizada y atractiva.

        **NOTA IMPORTANTE PARA DESARROLLADORES DE GUI:**
        Este método está diseñado EXCLUSIVAMENTE para la salida en la interfaz de
        línea de comandos (CLI) utilizando la función `print()`.
        NO DEBE SER UTILIZADO por una aplicación GUI para mostrar resultados.
        Las GUIs deben tomar el objeto `ScamperResponse` (preferiblemente obtenido
        a través de `main.py:get_scamper_ideas_for_gui`) y renderizar los datos
        utilizando sus propios componentes y lógica de UI.
        """
        
        print(f"\n🎯 PROBLEMA ANALIZADO:")
        print(f"   {response.original_problem}")
        print("\n" + "=" * 70)
        print("🚀 IDEAS GENERADAS CON SCAMPER")
        print("=" * 70)
        
        # Mostrar cada técnica con sus ideas
        for i, result in enumerate(response.results, 1):
            technique_name = self._get_technique_display_name(result.technique.value)
            
            print(f"\n{i}. 🔧 {technique_name}")
            print("-" * 50)
            print(f"💭 {result.explanation}")
            print("\n💡 Ideas generadas:")
            
            for j, idea in enumerate(result.ideas, 1):
                print(f"   {j}. {idea}")
        
        # Mostrar resumen
        print("\n" + "=" * 70)
        print("📊 RESUMEN EJECUTIVO")
        print("=" * 70)
        print(f"✨ {response.summary}")
        
        # Estadísticas
        total_ideas = sum(len(result.ideas) for result in response.results)
        successful_techniques = len([r for r in response.results if not any("Error" in idea for idea in r.ideas)])
        
        print(f"\n📈 ESTADÍSTICAS:")
        print(f"   • Total de ideas generadas: {total_ideas}")
        print(f"   • Técnicas aplicadas exitosamente: {successful_techniques}/7")
        print(f"   • Promedio de ideas por técnica: {total_ideas/7:.1f}")
    
    def _get_technique_display_name(self, technique: str) -> str:
        """Convierte el nombre técnico a nombre para mostrar"""
        display_names = {
            "substitute": "SUSTITUIR - Reemplazar elementos",
            "combine": "COMBINAR - Fusionar ideas",
            "adapt": "ADAPTAR - Aplicar de otros contextos", 
            "modify": "MODIFICAR - Amplificar o reducir",
            "put_to_other_uses": "OTROS USOS - Nuevas aplicaciones",
            "eliminate": "ELIMINAR - Simplificar",
            "reverse": "INVERTIR - Reorganizar o hacer al revés"
        }
        return display_names.get(technique, technique.upper())
    
    def _ask_continue(self) -> bool:
        """Pregunta si el usuario quiere continuar"""
        print("\n" + "=" * 50)
        while True:
            choice = input("¿Quieres analizar otro problema? (s/n): ").strip().lower()
            if choice in ['s', 'sí', 'si', 'y', 'yes']:
                return True
            elif choice in ['n', 'no']:
                return False
            else:
                print("⚠️  Por favor, responde 's' para sí o 'n' para no.")
    
    async def process_single_problem(self, problem: str, context: Optional[str] = None) -> ScamperResponse:
        """
        Procesa un problema único sin interfaz interactiva.

        Este método es útil para uso programático, por ejemplo, si se integra
        con una GUI u otro sistema.

        Args:
            problem: El problema o desafío a analizar.
            context: Contexto adicional opcional para el problema.

        Returns:
            Un objeto `ScamperResponse` que contiene los resultados del análisis SCAMPER.
            El llamador es responsable de manejar la naturaleza asíncrona de esta función
            (por ejemplo, usando `await` en un contexto `async` o `asyncio.run()`).
        """
        user_input = UserInput(problem=problem, context=context)
        return await orchestrator.process_user_input(user_input)

# Instancia global del chatbot
chatbot = ScamperChatbot()
