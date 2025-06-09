from typing import List
from models.schemas import UserInput, ScamperResult, ScamperTechnique
from utils.gemini_client import gemini_client

class CombineAgent:
    """Agente especializado en la técnica SCAMPER de COMBINAR"""
    
    def __init__(self):
        self.name = "Combine Agent"
        self.technique = ScamperTechnique.COMBINE
        self.description = "Especialista en fusionar ideas, elementos y conceptos para crear sinergias"
    
    async def generate_ideas(self, user_input: UserInput) -> ScamperResult:
        """
        Genera ideas usando la técnica COMBINAR
        
        Args:
            user_input: Entrada del usuario con problema y contexto
            
        Returns:
            Resultado con ideas de combinación
        """
        print(f"🔗 {self.name}: Buscando elementos para combinar...")
        
        try:
            # Generar ideas específicas de combinación
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
            
            print(f"✅ {self.name}: {len(ideas)} ideas de combinación generadas")
            return result
            
        except Exception as e:
            print(f"❌ {self.name}: Error generando ideas - {e}")
            return ScamperResult(
                technique=self.technique,
                ideas=[f"Error en agente de combinación: {str(e)}"],
                explanation="No se pudieron generar ideas de combinación debido a un error técnico."
            )
    
    def _create_explanation(self, problem: str) -> str:
        """Crea explicación específica para la técnica COMBINAR"""
        return f"""El Agente de Combinación analizó '{problem}' preguntándose:
        
• ¿Qué elementos separados se pueden fusionar para crear valor?
• ¿Qué funciones diferentes se pueden unir en una sola solución?
• ¿Qué ideas independientes pueden trabajar juntas sinérgicamente?
• ¿Qué recursos o capacidades se pueden combinar para mayor eficiencia?

Esta técnica busca crear soluciones más poderosas mediante la fusión estratégica de elementos."""

    def get_capabilities(self) -> dict:
        """Retorna las capacidades del agente"""
        return {
            "agent_name": self.name,
            "technique": self.technique.value,
            "specialization": "Fusión sinérgica de elementos",
            "focus_areas": [
                "Unión de funcionalidades",
                "Integración de sistemas",
                "Fusión de recursos",
                "Combinación de ideas",
                "Sinergias creativas"
            ]
        }

# Instancia global del agente
combine_agent = CombineAgent()