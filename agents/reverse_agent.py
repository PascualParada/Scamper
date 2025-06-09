from typing import List
from models.schemas import UserInput, ScamperResult, ScamperTechnique
from utils.gemini_client import gemini_client

class ReverseAgent:
    """Agente especializado en la técnica SCAMPER de INVERTIR/REORGANIZAR"""
    
    def __init__(self):
        self.name = "Reverse Agent"
        self.technique = ScamperTechnique.REVERSE
        self.description = "Especialista en invertir, reorganizar y abordar desde perspectivas opuestas"
    
    async def generate_ideas(self, user_input: UserInput) -> ScamperResult:
        """
        Genera ideas usando la técnica INVERTIR/REORGANIZAR
        
        Args:
            user_input: Entrada del usuario con problema y contexto
            
        Returns:
            Resultado con ideas de inversión/reorganización
        """
        print(f"🔄 {self.name}: Explorando inversiones y reorganizaciones...")
        
        try:
            # Generar ideas específicas de inversión/reorganización
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
            
            print(f"✅ {self.name}: {len(ideas)} ideas de inversión generadas")
            return result
            
        except Exception as e:
            print(f"❌ {self.name}: Error generando ideas - {e}")
            return ScamperResult(
                technique=self.technique,
                ideas=[f"Error en agente de inversión: {str(e)}"],
                explanation="No se pudieron generar ideas de inversión debido a un error técnico."
            )
    
    def _create_explanation(self, problem: str) -> str:
        """Crea explicación específica para la técnica INVERTIR"""
        return f"""El Agente de Inversión analizó '{problem}' preguntándose:
        
• ¿Qué pasaría si abordamos esto desde el extremo completamente opuesto?
• ¿Cómo se puede reorganizar la secuencia o el orden de los elementos?
• ¿Qué sucede si invertimos los roles, responsabilidades o flujos?
• ¿Qué perspectivas contraintuitivas pueden revelar nuevas soluciones?

Esta técnica busca breakthrough insights mediante el pensamiento contrario y la reorganización."""

    def get_capabilities(self) -> dict:
        """Retorna las capacidades del agente"""
        return {
            "agent_name": self.name,
            "technique": self.technique.value,
            "specialization": "Pensamiento contrario y reorganización estratégica",
            "focus_areas": [
                "Inversión de perspectivas",
                "Reorganización de secuencias",
                "Intercambio de roles",
                "Enfoques contraintuitivos",
                "Restructuración de flujos"
            ]
        }

# Instancia global del agente
reverse_agent = ReverseAgent()