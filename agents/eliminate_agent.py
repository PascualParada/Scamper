from typing import List
from models.schemas import UserInput, ScamperResult, ScamperTechnique
from utils.gemini_client import gemini_client

class EliminateAgent:
    """Agente especializado en la técnica SCAMPER de ELIMINAR"""
    
    def __init__(self):
        self.name = "Eliminate Agent"
        self.technique = ScamperTechnique.ELIMINATE
        self.description = "Especialista en simplificar, reducir y eliminar elementos innecesarios"
    
    async def generate_ideas(self, user_input: UserInput) -> ScamperResult:
        """
        Genera ideas usando la técnica ELIMINAR
        
        Args:
            user_input: Entrada del usuario con problema y contexto
            
        Returns:
            Resultado con ideas de eliminación
        """
        print(f"✂️ {self.name}: Identificando elementos para eliminar...")
        
        try:
            # Generar ideas específicas de eliminación
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
            
            print(f"✅ {self.name}: {len(ideas)} ideas de eliminación generadas")
            return result
            
        except Exception as e:
            print(f"❌ {self.name}: Error generando ideas - {e}")
            return ScamperResult(
                technique=self.technique,
                ideas=[f"Error en agente de eliminación: {str(e)}"],
                explanation="No se pudieron generar ideas de eliminación debido a un error técnico."
            )
    
    def _create_explanation(self, problem: str) -> str:
        """Crea explicación específica para la técnica ELIMINAR"""
        return f"""El Agente de Eliminación analizó '{problem}' preguntándose:
        
• ¿Qué elementos son innecesarios y se pueden quitar completamente?
• ¿Qué procesos redundantes se pueden eliminar para mayor eficiencia?
• ¿Qué complejidades se pueden simplificar o reducir?
• ¿Qué obstáculos o fricciones se pueden remover del sistema?

Esta técnica busca la elegancia y eficiencia mediante la simplificación estratégica."""

    def get_capabilities(self) -> dict:
        """Retorna las capacidades del agente"""
        return {
            "agent_name": self.name,
            "technique": self.technique.value,
            "specialization": "Simplificación y eliminación estratégica",
            "focus_areas": [
                "Reducción de complejidad",
                "Eliminación de redundancias",
                "Simplificación de procesos",
                "Remoción de obstáculos",
                "Optimización minimalista"
            ]
        }

# Instancia global del agente
eliminate_agent = EliminateAgent()