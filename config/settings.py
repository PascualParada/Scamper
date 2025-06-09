import os
from dotenv import load_dotenv
from ratelimit import limits, sleep_and_retry

# Cargar variables de entorno
load_dotenv()

# Rate limiting constants
ONE_MINUTE = 60
MAX_CALLS_PER_MINUTE = 60

class Settings:
    """Configuración global del sistema"""
    
    # API Keys
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Configuración de Gemini
    GEMINI_MODEL = "gemini-pro"
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
        if not 0 <= cls.GEMINI_TEMPERATURE <= 1:
            raise ValueError("GEMINI_TEMPERATURE debe estar entre 0 y 1")
        if cls.GEMINI_MAX_TOKENS <= 0:
            raise ValueError("GEMINI_MAX_TOKENS debe ser positivo")
        return True

    @classmethod
    @sleep_and_retry
    @limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
    def rate_limited_call(cls):
        """Decorador para limitar las llamadas a la API"""
        pass

class GeminiAPIError(Exception):
    pass

class ConfigurationError(Exception):
    pass

# Instancia global
settings = Settings()

# En settings.py
API_TIMEOUT = 30  # segundos
MAX_RETRIES = 3

@sleep_and_retry
@limits(calls=MAX_CALLS_PER_MINUTE, period=ONE_MINUTE)
def call_gemini_api():
    # Implementación
    pass

def validate_input(problema: str, contexto: str) -> bool:
    if not problema or len(problema) < 10:
        raise ValueError("El problema debe tener al menos 10 caracteres")
    if not contexto or len(contexto) < 10:
        raise ValueError("El contexto debe tener al menos 10 caracteres")
    return True