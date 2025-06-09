import asyncio
from typing import List, Dict
from models.schemas import UserInput, ScamperResponse, ScamperResult, ScamperTechnique
from utils.gemini_client import gemini_client
from config.settings import settings

# Importar todos los agentes especializados
from .substitute_agent import substitute_agent
from .combine_agent import combine_agent
from .adapt_agent import adapt_agent
from .modify_agent import modify_agent
from .other_uses_agent import other_uses_agent
from .eliminate_agent import eliminate_agent
from .reverse_agent import reverse_agent

class OrchestratorAgent:
    """Agente orquestador que coordina todos los agentes SCAMPER especializados"""
    
    def __init__(self):
        self.name = "Orchestrator"
        self.specialized_agents = {
            ScamperTechnique.SUBSTITUTE: substitute_agent,
            ScamperTechnique.COMBINE: combine_agent,
            ScamperTechnique.ADAPT: adapt_agent,
            ScamperTechnique.MODIFY: modify_agent,
            ScamperTechnique.PUT_TO_OTHER_USES: other_uses_agent,
            ScamperTechnique.ELIMINATE: eliminate_agent,
            ScamperTechnique.REVERSE: reverse_agent
        }
    
    async def process_user_input(self, user_input: UserInput) -> ScamperResponse:
        """
        Procesa la entrada del usuario coordinando todos los agentes SCAMPER especializados
        
        Args:
            user_input: Entrada del usuario con problema y contexto
            
        Returns:
            Respuesta completa con todas las ideas SCAMPER
        """
        print(f"🎯 {self.name}: Iniciando análisis multi-agente...")
        print(f"   Problema: {user_input.problem}")
        print(f"   Agentes disponibles: {len(self.specialized_agents)}")
        
        # Ejecutar todos los agentes especializados
        if settings.ENABLE_PARALLEL_EXECUTION:
            results = await self._coordinate_parallel_agents(user_input)
        else:
            results = await self._coordinate_sequential_agents(user_input)
        
        # Generar resumen ejecutivo
        summary = await self._generate_executive_summary(user_input.problem, results)
        
        # Crear respuesta completa
        response = ScamperResponse(
            original_problem=user_input.problem,
            results=results,
            summary=summary
        )
        
        print(f"✅ {self.name}: Análisis multi-agente completado.")
        print(f"   Resultados obtenidos: {len(results)} técnicas")
        return response
    
    async def _coordinate_parallel_agents(self, user_input: UserInput) -> List[ScamperResult]:
        """Coordina todos los agentes especializados en paralelo"""
        print(f"🚀 {self.name}: Coordinando agentes en paralelo...")
        
        # Crear tareas para todos los agentes especializados
        tasks = []
        for technique, agent in self.specialized_agents.items():
            print(f"   📋 Asignando tarea a {agent.name}")
            task = agent.generate_ideas(user_input)
            tasks.append(task)
        
        # Ejecutar todas las tareas en paralelo
        print(f"   ⚡ Ejecutando {len(tasks)} agentes simultáneamente...")
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Procesar resultados y manejar excepciones
        processed_results = []
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                technique = list(self.specialized_agents.keys())[i]
                agent_name = list(self.specialized_agents.values())[i].name
                print(f"   ❌ {agent_name}: Falló con error - {result}")
                # Crear resultado de error
                error_result = ScamperResult(
                    technique=technique,
                    ideas=[f"Error en {agent_name}: {str(result)}"],
                    explanation=f"El agente {agent_name} no pudo completar su análisis."
                )
                processed_results.append(error_result)
            else:
                processed_results.append(result)
        
        return processed_results
    
    async def _coordinate_sequential_agents(self, user_input: UserInput) -> List[ScamperResult]:
        """Coordina todos los agentes especializados secuencialmente"""
        print(f"⏳ {self.name}: Coordinando agentes secuencialmente...")
        
        results = []
        for technique, agent in self.specialized_agents.items():
            print(f"   🔄 Ejecutando {agent.name}...")
            try:
                result = await agent.generate_ideas(user_input)
                results.append(result)
            except Exception as e:
                print(f"   ❌ {agent.name}: Error - {e}")
                # Crear resultado de error
                error_result = ScamperResult(
                    technique=technique,
                    ideas=[f"Error en {agent.name}: {str(e)}"],
                    explanation=f"El agente {agent.name} no pudo completar su análisis."
                )
                results.append(error_result)
        
        return results
    
    async def _generate_executive_summary(self, problem: str, results: List[ScamperResult]) -> str:
        """Genera un resumen ejecutivo inteligente de todos los resultados"""
        
        # Contar métricas
        total_ideas = sum(len(result.ideas) for result in results)
        successful_agents = len([r for r in results if not any("Error" in idea for idea in r.ideas)])
        
        # Extraer las mejores ideas de cada técnica para el resumen
        best_ideas = []
        for result in results:
            if result.ideas and not any("Error" in idea for idea in result.ideas):
                # Tomar la primera idea de cada técnica exitosa
                best_ideas.append(f"{result.technique.value.replace('_', ' ').title()}: {result.ideas[0]}")
        
        # Crear prompt para resumen inteligente
        summary_prompt = f"""
        Eres un consultor de innovación experto. Analiza las siguientes ideas generadas por un sistema multi-agente SCAMPER y crea un resumen ejecutivo de máximo 4 oraciones.

        Problema analizado: {problem}

        Ideas principales por técnica:
        {chr(10).join(best_ideas[:5])}  # Limitar a 5 para no sobrecargar

        El resumen debe:
        1. Destacar las direcciones más prometedoras
        2. Identificar patrones o temas emergentes
        3. Sugerir próximos pasos o recomendaciones
        4. Ser conciso pero perspicaz

        Resumen ejecutivo:
        """
        
        try:
            summary = await gemini_client.generate_response(summary_prompt)
            return summary.strip()
        except Exception as e:
            print(f"   ⚠️ Error generando resumen: {e}")
            return f"El análisis multi-agente SCAMPER generó {total_ideas} ideas utilizando {successful_agents} técnicas especializadas. Las ideas exploran sustituciones estratégicas, combinaciones sinérgicas, adaptaciones cross-industry, modificaciones de escala, nuevos usos, simplificaciones y enfoques contraintuitivos para abordar '{problem}' desde múltiples perspectivas innovadoras."
    
    def get_system_status(self) -> Dict[str, any]:
        """Retorna el estado del sistema multi-agente"""
        agent_status = {}
        for technique, agent in self.specialized_agents.items():
            agent_status[technique.value] = {
                "agent_name": agent.name,
                "specialization": agent.description,
                "capabilities": agent.get_capabilities()
            }
        
        return {
            "orchestrator_name": self.name,
            "total_agents": len(self.specialized_agents),
            "execution_mode": "Parallel" if settings.ENABLE_PARALLEL_EXECUTION else "Sequential",
            "max_ideas_per_agent": settings.MAX_IDEAS_PER_TECHNIQUE,
            "specialized_agents": agent_status
        }
    
    async def test_all_agents(self) -> Dict[str, bool]:
        """Prueba que todos los agentes especializados funcionen correctamente"""
        print(f"🧪 {self.name}: Probando todos los agentes especializados...")
        
        test_input = UserInput(
            problem="Mejorar la comunicación en equipos remotos",
            context="Empresa de tecnología con trabajadores distribuidos globalmente"
        )
        
        agent_health = {}
        for technique, agent in self.specialized_agents.items():
            try:
                print(f"   🔍 Probando {agent.name}...")
                result = await agent.generate_ideas(test_input)
                # Verificar que el resultado sea válido
                is_healthy = (
                    len(result.ideas) > 0 and 
                    not any("Error" in idea for idea in result.ideas) and
                    result.explanation is not None
                )
                agent_health[agent.name] = is_healthy
                status = "✅ OK" if is_healthy else "❌ FALLO"
                print(f"     {status}")
            except Exception as e:
                agent_health[agent.name] = False
                print(f"     ❌ EXCEPCIÓN: {e}")
        
        healthy_count = sum(agent_health.values())
        total_count = len(agent_health)
        print(f"🏥 Estado del sistema: {healthy_count}/{total_count} agentes funcionando")
        
        return agent_health

# Instancia global del orquestador
orchestrator = OrchestratorAgent()