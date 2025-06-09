from typing import List
from models.schemas import UserInput, ScamperResult, ScamperTechnique
from utils.gemini_client import gemini_client

class AdaptAgent:
    """Agente especializado en la técnica SCAMPER de ADAPTAR"""
    
    def __init__(self):
        self.name = "Adapt Agent"
        self.technique = ScamperTechnique.ADAPT
        self.description = "Especialista en adaptar soluciones exitosas de otros contextos"
    
    async def generate_ideas(self, user_input: UserInput) -> ScamperResult:
        """
        Genera ideas usando la técnica ADAPTAR
        
        Args:
            user_input: Entrada del usuario con problema y contexto
            
        Returns:
            Resultado con ideas de adaptación
        """
        print(f"🔄 {self.name}: Explorando adaptaciones de otros contextos...")
        
        try:
            # Generar ideas específicas de adaptación
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
            
            print(f"✅ {self.name}: {len(ideas)} ideas de adaptación generadas")
            return result
            
        except Exception as e:
            print(f"❌ {self.name}: Error generando ideas - {e}")
            return ScamperResult(
                technique=self.technique,
                ideas=[f"Error en agente de adaptación: {str(e)}"],
                explanation="No se pudieron generar ideas de adaptación debido a un error técnico."
            )
    
    def _create_explanation(self, problem: str) -> str:
        """Crea explicación específica para la técnica ADAPTAR"""
        return f"""El Agente de Adaptación analizó '{problem}' preguntándose:
        
• ¿Qué soluciones exitosas de otras industrias se pueden adaptar?
• ¿Qué enfoques del pasado se pueden modernizar para este contexto?
• ¿Qué prácticas de otros campos se pueden aplicar aquí?
• ¿Qué métodos de culturas o regiones diferentes son transferibles?

Esta técnica busca aprovechar el conocimiento existente adaptándolo creativamente."""

    def get_capabilities(self) -> dict:
        """Retorna las capacidades del agente"""
        return {
            "agent_name": self.name,
            "technique": self.technique.value,
            "specialization": "Adaptación cross-industry y contextual",
            "focus_areas": [
                "Transferencia entre industrias",
                "Modernización de métodos clásicos",
                "Adaptación cultural",
                "Aplicación de mejores prácticas",
                "Inspiración cross-funcional"
            ]
        }

# Instancia global del agente
adapt_agent = AdaptAgent()