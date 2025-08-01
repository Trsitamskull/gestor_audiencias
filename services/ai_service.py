"""
Servicio de IA para autocompletar formularios de audiencias.
Utiliza OpenAI GPT para extraer información de texto libre con máxima precisión.
"""

import json
import re
from typing import Dict, Optional, Any
from datetime import datetime

try:
    import openai
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("❌ Error: OpenAI no está instalado. Ejecuta: pip install openai")

try:
    from config.config import (
        OPENAI_API_KEY, OPENAI_MODEL, 
        ANONYMIZE_DATA, USE_FREE_TIER, SHOW_PRIVACY_WARNING
    )
    HAS_CONFIG = True
except ImportError:
    print("❌ Error: config.py no encontrado. Crea el archivo config/config.py con tu API key.")
    OPENAI_API_KEY = ""
    OPENAI_MODEL = "gpt-4o-mini"
    ANONYMIZE_DATA = False
    USE_FREE_TIER = False
    SHOW_PRIVACY_WARNING = True
    HAS_CONFIG = False

try:
    from utils.anonimizador import anonimizar_para_ia, restaurar_datos_ia
    HAS_ANONYMIZER = True
except ImportError:
    print("⚠️ Advertencia: Anonimizador no disponible")
    HAS_ANONYMIZER = False


class AIFormFiller:
    """Servicio para autocompletar formularios usando OpenAI exclusivamente."""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or OPENAI_API_KEY
        
        if not OPENAI_AVAILABLE:
            raise Exception("OpenAI no está disponible. Instala con: pip install openai")
        
        if not self.api_key:
            raise Exception("API Key de OpenAI requerida. Configura config.py")
        
        # Inicializar cliente OpenAI
        self.client = OpenAI(api_key=self.api_key)
        self.model = OPENAI_MODEL
        print(f"� OpenAI configurado correctamente - Modelo: {self.model}")
    
    def extract_audiencia_info(self, texto: str) -> Dict[str, Any]:
        """
        Extrae información de audiencias usando OpenAI GPT con anonimización opcional.
        
        Args:
            texto (str): Texto libre con información de la audiencia
            
        Returns:
            Dict con los campos extraídos para el formulario
        """
        
        try:
            texto_para_ia = texto
            mapeo_reverso = {}
            
            # Aplicar anonimización si está habilitada
            if ANONYMIZE_DATA and HAS_ANONYMIZER:
                print("🔒 Anonimizando datos sensibles...")
                texto_para_ia, mapeo_reverso = anonimizar_para_ia(texto)
                print("✅ Datos anonimizados para procesamiento seguro")
            
            # Procesar con OpenAI
            resultado = self._extract_with_openai(texto_para_ia)
            
            # Restaurar datos reales si se anonimizó
            if ANONYMIZE_DATA and HAS_ANONYMIZER and mapeo_reverso:
                print("🔓 Restaurando datos reales...")
                resultado = restaurar_datos_ia(resultado, mapeo_reverso)
                print("✅ Datos reales restaurados")
            
            print("🤖 Procesado con OpenAI" + (" (con anonimización)" if ANONYMIZE_DATA else ""))
            return resultado
            
        except Exception as e:
            print(f"❌ Error OpenAI: {e}")
            # Devolver estructura vacía en caso de error
            return {
                "radicado": "",
                "tipo_audiencia": "",
                "fecha": "",
                "hora": "",
                "minuto": "",
                "juzgado": "",
                "se_realizo": "",
                "motivos": "",
                "observaciones": f"Error al procesar: {str(e)}",
                "demandante": "",
                "demandado": ""
            }
    
    def _extract_with_openai(self, texto: str) -> Dict[str, Any]:
        """
        Extracción usando OpenAI GPT - Modo de alta precisión.
        """
        
        prompt = f"""
Eres un asistente especializado en extraer información de textos judiciales colombianos.

IMPORTANTE: Responde SOLO con un objeto JSON válido, sin texto adicional.

Extrae la siguiente información del texto:

TEXTO A ANALIZAR:
"{texto}"

ESTRUCTURA JSON REQUERIDA:
{{
    "radicado": "número de radicado COMPLETO (incluye TODOS los números y guiones)",
    "tipo_audiencia": "tipo específico de audiencia",
    "fecha": "DD/MM/YYYY",
    "hora": "HH",
    "minuto": "MM", 
    "juzgado": "nombre completo del juzgado o tribunal",
    "se_realizo": "SI" o "NO",
    "motivos": "un_solo_motivo_principal",
    "observaciones": "información adicional relevante y TODOS los motivos si hay múltiples",
    "demandante": "nombre del demandante/actor/solicitante",
    "demandado": "nombre del demandado/accionado"
}}

REGLAS CRÍTICAS PARA RADICADO:
1. BUSCA números largos tipo: "2024-00145-001", "25754315800420240012300", "2023-001234-00"
2. BUSCA también nombres de personas en el documento
3. COMBINA nombre + radicado en UNA SOLA línea separados por " - "
4. Ejemplo: "MARÍA GONZÁLEZ PÉREZ - 2024-00145-001"
5. Si solo encuentras radicado sin nombre: solo pon el número
6. Si solo encuentras nombre sin radicado: solo pon el nombre
7. FORMATO PREFERIDO: "NOMBRE COMPLETO - NÚMERO_RADICADO_COMPLETO"

OTRAS REGLAS:
- Para fechas en texto, conviértelas a formato DD/MM/YYYY
- Para horas AM/PM, convierte a formato 24h (ej: 2:30 PM = hora: "14", minuto: "30")
- Si no encuentras algún dato, usa cadena vacía "" o array vacío []
- El campo "se_realizo" debe ser "SI" si la audiencia se realizó, "NO" si no
- Para "motivos": Si la audiencia NO se realizó, identifica SOLO EL PRIMER motivo principal:
  * "juez" - si faltó el juez, por el juez, inasistencia del juez
  * "fiscalía" - si faltó la fiscalía, por fiscalía, inasistencia fiscalía  
  * "usuario" - si faltó el usuario, demandante, actor, solicitante
  * "inpec" - si faltó INPEC, instituto penitenciario
  * "víctima" - si faltó la víctima, por la víctima
  * "icbf" - si faltó ICBF, instituto bienestar familiar
  * "defensor confianza" - si faltó defensor de confianza, abogado privado
  * "defensor público" - si faltó defensor público, defensoría
  IMPORTANTE: Solo selecciona UN motivo (el más importante). Si hay múltiples motivos, menciónalos todos en "observaciones".
- Para "observaciones": Incluye detalles adicionales y TODOS los motivos de no realización si hay múltiples.
- Identifica tipos específicos: Audiencia De Conciliación, Audiencia Concentrada, etc.
- Para juzgados, incluye la designación completa
- Extrae nombres completos de demandante y demandado si están presentes
"""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "Eres un experto en procesamiento de documentos judiciales colombianos. Responde solo con JSON válido."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.1  # Baja temperatura para mayor precisión
            )
            
            resultado_texto = response.choices[0].message.content
            if resultado_texto:
                resultado_texto = resultado_texto.strip()
            else:
                raise Exception("Respuesta vacía de OpenAI")
            
            # Limpiar posibles caracteres markdown
            if resultado_texto.startswith("```json"):
                resultado_texto = resultado_texto[7:]
            if resultado_texto.endswith("```"):
                resultado_texto = resultado_texto[:-3]
            
            resultado = json.loads(resultado_texto)
            
            # Validar y normalizar resultado
            campos_requeridos = ["radicado", "tipo_audiencia", "fecha", "hora", "minuto", 
                               "juzgado", "se_realizo", "motivos", "observaciones", 
                               "demandante", "demandado"]
            
            for campo in campos_requeridos:
                if campo not in resultado:
                    resultado[campo] = ""
            
            return resultado
            
        except json.JSONDecodeError as e:
            print(f"❌ Error parsing JSON de OpenAI: {e}")
            raise Exception(f"Error en formato JSON: {e}")
        except Exception as e:
            print(f"❌ Error OpenAI: {e}")
            raise Exception(f"Error de OpenAI: {e}")


# Instancia global del servicio
ai_service = AIFormFiller()
