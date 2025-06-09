from typing import List
from models.schemas import UserInput, ScamperResult, ScamperTechnique
from utils.gemini_client import gemini_client

class ModifyAgent:
    """Agente especializado en la técnica SCAMPER de MODIFICAR/MAGNIFICAR"""
    
    def __init__(self):
        self.name = "Modify Agent"
        self.technique = ScamperTechnique.MODIFY
        self.description = "Especialista en modificar, amplificar, reducir e intensificar elementos"
    
    async def generate_ideas(self, user_input: UserInput) -> ScamperResult:
        """
        Genera ideas usando la técnica MODIFICAR
        
        Args:
            user_input: Entrada del usuario con problema y contexto
            
        Returns:
            Resultado con ideas de modificación
        """
        print(f"🔧 {self.name}: Explorando modificaciones y amplificaciones...")
        
        try:
            # Generar ideas específicas de modificación
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
            
            print(f"✅ {self.name}: {len(ideas)} ideas de modificación generadas")
            return result
            
        except Exception as e:
            print(f"❌ {self.name}: Error generando ideas - {e}")
            return ScamperResult(
                technique=self.technique,
                ideas=[f"Error en agente de modificación: {str(e)}"],
                explanation="No se pudieron generar ideas de modificación debido a un error técnico."
            )
    
    def _create_explanation(self, problem: str) -> str:
        """Crea explicación específica para la técnica MODIFICAR"""
        return f"""El Agente de Modificación analizó '{problem}' preguntándose:
        
• ¿Qué aspectos se pueden amplificar o hacer más grandes/intensos?
• ¿Qué elementos se pueden reducir o minimizar para mayor eficiencia?
• ¿Qué características se pueden hacer más rápidas, lentas, fuertes o suaves?
• ¿Qué componentes se pueden exagerar o suavizar estratégicamente?

Esta técnica busca optimizar mediante cambios de escala, intensidad y proporción."""

    def get_capabilities(self) -> dict:
        """Retorna las capacidades del agente"""
        return {
            "agent_name": self.name,
            "technique": self.technique.value,
            "specialization": "Optimización mediante modificación de escalas",
            "focus_areas": [
                "Amplificación estratégica",
                "Reducción eficiente",
                "Intensificación de características",
                "Cambios de velocidad/ritmo",
                "Ajustes de proporción"
            ]
        }

# Instancia global del agente
modify_agent = ModifyAgent()