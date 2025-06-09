import google.generativeai as genai
import asyncio
from typing import Optional, List
from config.settings import settings

class GeminiClient:
    """Cliente para interactuar con la API de Gemini"""
    
    def __init__(self):
        """Inicializa el cliente de Gemini"""
        self._configure_api()
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
    
    def _configure_api(self):
        """Configura la API de Gemini con la API key"""
        if not settings.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY no está configurada")
        genai.configure(api_key=settings.GEMINI_API_KEY)
    
    async def generate_response(self, prompt: str) -> str:
        """
        Genera una respuesta usando Gemini
        
        Args:
            prompt: El prompt para enviar a Gemini
            
        Returns:
            Respuesta generada por Gemini
        """
        try:
            # Configuración de generación
            generation_config = genai.types.GenerationConfig(
                temperature=settings.GEMINI_TEMPERATURE,
                max_output_tokens=settings.GEMINI_MAX_TOKENS,
            )
            
            # Generar respuesta
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            return response.text
            
        except Exception as e:
            print(f"Error generando respuesta: {e}")
            return f"Error: No se pudo generar respuesta - {str(e)}"
    
    async def generate_scamper_ideas(self, technique: str, problem: str, context: Optional[str] = None) -> List[str]:
        """
        Genera ideas específicas para una técnica SCAMPER
        
        Args:
            technique: Técnica SCAMPER a aplicar
            problem: Problema a resolver
            context: Contexto adicional (opcional)
            
        Returns:
            Lista de ideas generadas
        """
        # Crear prompt específico para la técnica SCAMPER
        prompt = self._create_scamper_prompt(technique, problem, context)
        
        try:
            response = await self.generate_response(prompt)
            ideas = self._parse_ideas_from_response(response)
            return ideas[:settings.MAX_IDEAS_PER_TECHNIQUE]  # Limitar número de ideas
            
        except Exception as e:
            print(f"Error generando ideas SCAMPER: {e}")
            return [f"Error generando ideas para {technique}"]
    
    def _create_scamper_prompt(self, technique: str, problem: str, context: Optional[str] = None) -> str:
        """Crea un prompt específico para cada técnica SCAMPER"""
        
        technique_prompts = {
            "substitute": f"""
            Aplica la técnica SCAMPER de SUSTITUIR al siguiente problema:
            Problema: {problem}
            {f'Contexto: {context}' if context else ''}
            
            Genera exactamente 3 ideas creativas preguntándote:
            - ¿Qué se puede sustituir?
            - ¿Qué materiales, procesos o elementos se pueden reemplazar?
            - ¿Qué alternativas existen?
            
            Formato de respuesta:
            1. [Idea específica y concreta]
            2. [Idea específica y concreta]  
            3. [Idea específica y concreta]
            """,
            
            "combine": f"""
            Aplica la técnica SCAMPER de COMBINAR al siguiente problema:
            Problema: {problem}
            {f'Contexto: {context}' if context else ''}
            
            Genera exactamente 3 ideas creativas preguntándote:
            - ¿Qué se puede combinar o fusionar?
            - ¿Qué ideas, funciones o características se pueden unir?
            - ¿Qué sinergias se pueden crear?
            
            Formato de respuesta:
            1. [Idea específica y concreta]
            2. [Idea específica y concreta]
            3. [Idea específica y concreta]
            """,
            
            "adapt": f"""
            Aplica la técnica SCAMPER de ADAPTAR al siguiente problema:
            Problema: {problem}
            {f'Contexto: {context}' if context else ''}
            
            Genera exactamente 3 ideas creativas preguntándote:
            - ¿Qué se puede adaptar de otros contextos?
            - ¿Qué soluciones de otras industrias se pueden aplicar?
            - ¿Qué se puede copiar o modificar de ideas existentes?
            
            Formato de respuesta:
            1. [Idea específica y concreta]
            2. [Idea específica y concreta]
            3. [Idea específica y concreta]
            """,
            
            "modify": f"""
            Aplica la técnica SCAMPER de MODIFICAR/MAGNIFICAR al siguiente problema:
            Problema: {problem}
            {f'Contexto: {context}' if context else ''}
            
            Genera exactamente 3 ideas creativas preguntándote:
            - ¿Qué se puede modificar, amplificar o exagerar?
            - ¿Qué se puede hacer más grande, pequeño, fuerte, rápido?
            - ¿Qué características se pueden intensificar?
            
            Formato de respuesta:
            1. [Idea específica y concreta]
            2. [Idea específica y concreta]
            3. [Idea específica y concreta]
            """,
            
            "put_to_other_uses": f"""
            Aplica la técnica SCAMPER de OTROS USOS al siguiente problema:
            Problema: {problem}
            {f'Contexto: {context}' if context else ''}
            
            Genera exactamente 3 ideas creativas preguntándote:
            - ¿Para qué más se puede usar?
            - ¿Qué otros mercados o aplicaciones podría tener?
            - ¿Cómo se puede reutilizar de forma diferente?
            
            Formato de respuesta:
            1. [Idea específica y concreta]
            2. [Idea específica y concreta]
            3. [Idea específica y concreta]
            """,
            
            "eliminate": f"""
            Aplica la técnica SCAMPER de ELIMINAR al siguiente problema:
            Problema: {problem}
            {f'Contexto: {context}' if context else ''}
            
            Genera exactamente 3 ideas creativas preguntándote:
            - ¿Qué se puede eliminar, simplificar o reducir?
            - ¿Qué es innecesario o redundante?
            - ¿Cómo se puede hacer más minimalista?
            
            Formato de respuesta:
            1. [Idea específica y concreta]
            2. [Idea específica y concreta]
            3. [Idea específica y concreta]
            """,
            
            "reverse": f"""
            Aplica la técnica SCAMPER de INVERTIR/REORGANIZAR al siguiente problema:
            Problema: {problem}
            {f'Contexto: {context}' if context else ''}
            
            Genera exactamente 3 ideas creativas preguntándote:
            - ¿Qué se puede invertir, reorganizar o hacer al revés?
            - ¿Qué pasaría si cambiamos el orden o la secuencia?
            - ¿Cómo se puede abordar desde el extremo opuesto?
            
            Formato de respuesta:
            1. [Idea específica y concreta]
            2. [Idea específica y concreta]
            3. [Idea específica y concreta]
            """
        }
        
        return technique_prompts.get(technique, f"Aplica SCAMPER al problema: {problem}")
    
    def _parse_ideas_from_response(self, response: str) -> List[str]:
        """Parsea las ideas de la respuesta de Gemini"""
        ideas = []
        lines = response.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            # Buscar líneas que empiecen con números (1., 2., 3., etc.)
            if line and (line[0].isdigit() or line.startswith('-') or line.startswith('•')):
                # Limpiar el formato (quitar números, guiones, etc.)
                clean_idea = line
                for prefix in ['1.', '2.', '3.', '4.', '5.', '-', '•', '*']:
                    if clean_idea.startswith(prefix):
                        clean_idea = clean_idea[len(prefix):].strip()
                        break
                
                if clean_idea:
                    ideas.append(clean_idea)
        
        # Si no encontró ideas con formato, tomar toda la respuesta
        if not ideas:
            ideas = [response.strip()]
        
        return ideas

# Instancia global del cliente
gemini_client = GeminiClient()