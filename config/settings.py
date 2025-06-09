import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Settings:
    """Configuración global del sistema"""
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Configuración de Gemini
    GEMINI_MODEL = "gemini-1.5-flash"
    GEMINI_TEMPERATURE = 0.7
    GEMINI_MAX_TOKENS = 1000
    
    # Configuración del sistema
    MAX_IDEAS_PER_TECHNIQUE = 3
    ENABLE_PARALLEL_EXECUTION = True
    
    # Validación
    @classmethod
    def validate(cls):
        if not cls.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY no está configurada. Crear archivo .env con tu API key.")
        return True

# Instancia global
settings = Settings()

# En settings.py
API_TIMEOUT = 30  # segundos
MAX_RETRIES = 3

def validate_input(problema: str, contexto: str) -> bool:
    if not problema or len(problema) < 10:
        raise ValueError("El problema debe tener al menos 10 caracteres")
    if not contexto or len(contexto) < 10:
        raise ValueError("El contexto debe tener al menos 10 caracteres")
    return True