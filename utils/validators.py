from datetime import datetime
from typing import List, Optional, Tuple

def validar_campos_obligatorios(datos: dict) -> Tuple[bool, str]:
    """Valida que los campos obligatorios estén completos."""
    campos_obligatorios = {
        'radicado': 'Radicado del proceso',
        'tipo': 'Tipo de audiencia',
        'realizada_si': 'Realizada (SI/NO)',
        'realizada_no': 'Realizada (SI/NO)',
        'juzgado': 'Juzgado'
    }
    
    # Verificar que se haya seleccionado SI o NO
    if not datos.get('realizada_si') and not datos.get('realizada_no'):
        return False, "Debe seleccionar si la audiencia se realizó o no"
    
    # Verificar otros campos obligatorios
    for campo, nombre_campo in campos_obligatorios.items():
        if campo in ['realizada_si', 'realizada_no']:
            continue  # Ya validado arriba
        if not datos.get(campo, '').strip():
            return False, f"El campo '{nombre_campo}' es obligatorio"
    
    return True, ""

def validar_fecha(fecha_str: str) -> Tuple[bool, str]:
    """Valida el formato de fecha DD/MM/AAAA."""
    try:
        fecha = datetime.strptime(fecha_str, "%d/%m/%Y")
        # Verificar que la fecha no sea muy antigua o muy futura
        año_actual = datetime.now().year
        if fecha.year < año_actual - 10 or fecha.year > año_actual + 10:
            return False, f"La fecha parece incorrecta: {fecha_str}"
        return True, ""
    except ValueError:
        return False, f"Formato de fecha inválido: {fecha_str}. Use DD/MM/AAAA"

def validar_hora(hora_str: str) -> Tuple[bool, str]:
    """Valida el formato de hora HH:MM."""
    try:
        datetime.strptime(hora_str, "%H:%M")
        return True, ""
    except ValueError:
        return False, f"Formato de hora inválido: {hora_str}. Use HH:MM"

def validar_motivos_no_realizacion(realizada: str, motivos: List[str]) -> Tuple[bool, str]:
    """Valida que si la audiencia NO se realizó, haya al menos un motivo."""
    if realizada == "NO":
        if not any(motivo.strip() for motivo in motivos):
            return False, "Debe seleccionar al menos un motivo si la audiencia NO se realizó"
    return True, ""

def validar_todos_los_datos(datos: dict) -> Tuple[bool, str]:
    """Ejecuta todas las validaciones sobre los datos del formulario."""
    # Validar campos obligatorios
    valido, mensaje = validar_campos_obligatorios(datos)
    if not valido:
        return False, mensaje
    
    # Validar fecha
    valido, mensaje = validar_fecha(datos.get('fecha', ''))
    if not valido:
        return False, mensaje
    
    # Validar hora
    valido, mensaje = validar_hora(datos.get('hora', ''))
    if not valido:
        return False, mensaje
    
    # Validar motivos si NO se realizó
    realizada = "SI" if datos.get('realizada_si') else "NO"
    valido, mensaje = validar_motivos_no_realizacion(realizada, datos.get('motivos', []))
    if not valido:
        return False, mensaje
    
    return True, "Datos válidos"

def limpiar_texto(texto: str) -> str:
    """Limpia y normaliza texto de entrada."""
    if not texto:
        return ""
    return str(texto).strip()

def normalizar_radicado(radicado: str) -> str:
    """Normaliza el formato del radicado."""
    radicado_limpio = limpiar_texto(radicado)
    # Aquí podrías agregar más lógica de normalización si es necesario
    return radicado_limpio.upper()