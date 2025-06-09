from typing import List
from models.schemas import UserInput, ScamperResult, ScamperTechnique
from utils.gemini_client import gemini_client

class SubstituteAgent:
    """Agente especializado en la técnica SCAMPER de SUSTITUIR"""
    
    def __init__(self):
        self.name = "Substitute Agent"
        self.technique = ScamperTechnique.SUBSTITUTE
        self.description = "Especialista en encontrar elementos que se pueden reemplazar o intercambiar"
    
    async def generate_ideas(self, user_input: UserInput) -> ScamperResult:
        """
        Genera ideas usando la técnica SUSTITUIR
        
        Args:
            user_input: Entrada del usuario con problema y contexto
            
        Returns:
            Resultado con ideas de sustitución
        """
        print(f"🔄 {self.name}: Analizando qué se puede sustituir...")
        
        try:
            # Generar ideas específicas de sustitución
            ideas = await gemini_client.generate_scamper_ideas(
                technique=self.technique.value,
                problem=user_input.problem,
                context=user_input.context
            )
            
            # Crear explicación especializada
            explanation = self._create_explanation(user_input.problem)
            
            result = ScamperResult(
                technique=self.technique,
                ideas=ideas,
                explanation=explanation
            )
            
            print(f"✅ {self.name}: {len(ideas)} ideas de sustitución generadas")
            return result
            
        except Exception as e:
            print(f"❌ {self.name}: Error generando ideas - {e}")
            return ScamperResult(
                technique=self.technique,
                ideas=[f"Error en agente de sustitución: {str(e)}"],
                explanation="No se pudieron generar ideas de sustitución debido a un error técnico."
            )
    
    def _create_explanation(self, problem: str) -> str:
        """Crea explicación específica para la técnica SUSTITUIR"""
        return f"""El Agente de Sustitución analizó '{problem}' preguntándose:
        
• ¿Qué elementos actuales se pueden reemplazar por alternativas mejores?
• ¿Qué materiales, procesos o componentes tienen sustitutos disponibles?
• ¿Qué aspectos tradicionales se pueden intercambiar por enfoques modernos?
• ¿Qué personas, roles o responsabilidades se pueden redistribuir?

Esta técnica busca identificar oportunidades de mejora reemplazando lo existente por algo diferente."""

    def get_capabilities(self) -> dict:
        """Retorna las capacidades del agente"""
        return {
            "agent_name": self.name,
            "technique": self.technique.value,
            "specialization": "Identificación de elementos sustituibles",
            "focus_areas": [
                "Materiales alternativos",
                "Procesos de reemplazo", 
                "Tecnologías sustitutivas",
                "Enfoques diferentes",
                "Recursos alternativos"
            ]
        }

# Instancia global del agente
substitute_agent = SubstituteAgent()