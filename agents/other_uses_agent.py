from typing import List
from models.schemas import UserInput, ScamperResult, ScamperTechnique
from utils.gemini_client import gemini_client

class OtherUsesAgent:
    """Agente especializado en la técnica SCAMPER de OTROS USOS"""
    
    def __init__(self):
        self.name = "Other Uses Agent"
        self.technique = ScamperTechnique.PUT_TO_OTHER_USES
        self.description = "Especialista en encontrar nuevas aplicaciones y mercados para elementos existentes"
    
    async def generate_ideas(self, user_input: UserInput) -> ScamperResult:
        """
        Genera ideas usando la técnica OTROS USOS
        
        Args:
            user_input: Entrada del usuario con problema y contexto
            
        Returns:
            Resultado con ideas de otros usos
        """
        print(f"🎯 {self.name}: Explorando nuevos usos y aplicaciones...")
        
        try:
            # Generar ideas específicas de otros usos
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
            
            print(f"✅ {self.name}: {len(ideas)} ideas de otros usos generadas")
            return result
            
        except Exception as e:
            print(f"❌ {self.name}: Error generando ideas - {e}")
            return ScamperResult(
                technique=self.technique,
                ideas=[f"Error en agente de otros usos: {str(e)}"],
                explanation="No se pudieron generar ideas de otros usos debido a un error técnico."
            )
    
    def _create_explanation(self, problem: str) -> str:
        """Crea explicación específica para la técnica OTROS USOS"""
        return f"""El Agente de Otros Usos analizó '{problem}' preguntándose:
        
• ¿Para qué otros propósitos se pueden usar los elementos existentes?
• ¿Qué nuevos mercados o audiencias podrían beneficiarse de esto?
• ¿Cómo se puede reutilizar de maneras no convencionales?
• ¿Qué aplicaciones secundarias o derivadas son posibles?

Esta técnica busca maximizar el valor encontrando múltiples aplicaciones para los recursos."""

    def get_capabilities(self) -> dict:
        """Retorna las capacidades del agente"""
        return {
            "agent_name": self.name,
            "technique": self.technique.value,
            "specialization": "Identificación de aplicaciones alternativas",
            "focus_areas": [
                "Nuevos mercados objetivo",
                "Usos no convencionales",
                "Aplicaciones derivadas",
                "Reutilización creativa",
                "Expansión de propósitos"
            ]
        }

# Instancia global del agente
other_uses_agent = OtherUsesAgent()