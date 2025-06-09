from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class ScamperTechnique(str, Enum):
    """Técnicas SCAMPER disponibles"""
    SUBSTITUTE = "substitute"
    COMBINE = "combine"
    ADAPT = "adapt"
    MODIFY = "modify"
    PUT_TO_OTHER_USES = "put_to_other_uses"
    ELIMINATE = "eliminate"
    REVERSE = "reverse"

class UserInput(BaseModel):
    """Entrada del usuario con el problema a resolver"""
    problem: str = Field(..., description="Descripción del problema o desafío creativo")
    context: Optional[str] = Field(None, description="Contexto adicional del problema")

class ScamperResult(BaseModel):
    """Resultado de una técnica SCAMPER específica"""
    technique: ScamperTechnique = Field(..., description="Técnica SCAMPER utilizada")
    ideas: List[str] = Field(..., description="Lista de ideas generadas")
    explanation: str = Field(..., description="Explicación de cómo se aplicó la técnica")

class ScamperResponse(BaseModel):
    """Respuesta completa del sistema SCAMPER"""
    original_problem: str = Field(..., description="Problema original del usuario")
    results: List[ScamperResult] = Field(..., description="Resultados de cada técnica SCAMPER")
    summary: str = Field(..., description="Resumen ejecutivo de todas las ideas")

class AgentMessage(BaseModel):
    """Mensaje entre agentes"""
    sender: str = Field(..., description="Agente que envía el mensaje")
    content: str = Field(..., description="Contenido del mensaje")
    metadata: Optional[dict] = Field(None, description="Metadatos adicionales")