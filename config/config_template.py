# Plantilla de configuración para OpenAI
# Copia este archivo como "config.py" y agrega tu API key

# Configuración de OpenAI
OPENAI_API_KEY = ""  # Agrega tu API key aquí: sk-proj-...
OPENAI_MODEL = "gpt-4o-mini"  # Modelo recomendado: preciso y económico

# Configuración de Privacidad y Anonimización
USE_FREE_TIER = True  # Usar tier gratuito de OpenAI (requiere compartir datos)
ANONYMIZE_DATA = True  # Anonimizar datos sensibles antes de enviar a IA
SHOW_PRIVACY_WARNING = False  # No mostrar advertencia (datos están anonimizados)

# Configuración de Anonimización
ANONYMIZE_NAMES = True  # Anonimizar nombres de personas
ANONYMIZE_IDS = True  # Anonimizar números de cédula/documento
ANONYMIZE_CASE_NUMBERS = True  # Anonimizar números de radicado
ANONYMIZE_COURTS = False  # Mantener nombres de juzgados (menos sensible)

# Modelos disponibles:
# - "gpt-3.5-turbo": Más económico (~$0.002/audiencia)  
# - "gpt-4o-mini": Más preciso (~$0.0008/audiencia) - RECOMENDADO
# - "gpt-4": Máxima precisión pero más costoso

# Para obtener tu API key:
# 1. Ve a https://platform.openai.com/api-keys
# 2. Crea una cuenta o inicia sesión
# 3. Crea una nueva API key
# 4. Agrega crédito ($5 USD = varios meses de uso)

# Ejemplo de configuración completa:
# OPENAI_API_KEY = "sk-proj-ABC123..."
# OPENAI_MODEL = "gpt-4o-mini"
# USE_FREE_TIER = True
# ANONYMIZE_DATA = True
