import os
import sys
import shutil

def obtener_directorio_real():
    """Devuelve la carpeta donde realmente se encuentra el .exe o .py"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

# Directorio base del proyecto
BASE_DIR = obtener_directorio_real()

# Rutas organizadas
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
ARCHIVOS_CREADOS_DIR = os.path.join(BASE_DIR, "archivos_creados")
CONFIG_DIR = os.path.join(BASE_DIR, "config")
DOCS_DIR = os.path.join(BASE_DIR, "docs")

# Archivo de plantilla
PLANTILLA_EXCEL = os.path.join(TEMPLATES_DIR, "plantilla_audiencias.xlsx")

# Crear directorios si no existen
os.makedirs(ARCHIVOS_CREADOS_DIR, exist_ok=True)
os.makedirs(TEMPLATES_DIR, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

def crear_carpeta_si_no_existe():
    """Crea la carpeta de archivos creados si no existe"""
    if not os.path.exists(ARCHIVOS_CREADOS_DIR):
        os.makedirs(ARCHIVOS_CREADOS_DIR)

def crear_copia_plantilla(nombre_archivo):
    """Crea una copia de la plantilla con el nombre especificado"""
    crear_carpeta_si_no_existe()
    destino = os.path.join(ARCHIVOS_CREADOS_DIR, nombre_archivo)
    if os.path.exists(destino):
        raise FileExistsError("Ya existe un archivo con ese nombre.")
    shutil.copy2(PLANTILLA_EXCEL, destino)
    return destino

def listar_archivos_creados():
    """Retorna una lista de archivos Excel en la carpeta de archivos creados"""
    crear_carpeta_si_no_existe()
    return [f for f in os.listdir(ARCHIVOS_CREADOS_DIR) if f.endswith(".xlsx")]

def seleccionar_archivo(nombre_archivo):
    """Retorna la ruta completa del archivo seleccionado"""
    ruta = os.path.join(ARCHIVOS_CREADOS_DIR, nombre_archivo)
    if not os.path.exists(ruta):
        raise FileNotFoundError("Archivo no encontrado.")
    return ruta

def eliminar_archivo(nombre_archivo):
    """Elimina un archivo de la carpeta de archivos creados"""
    ruta = os.path.join(ARCHIVOS_CREADOS_DIR, nombre_archivo)
    if os.path.exists(ruta):
        os.remove(ruta)
        return True
    return False

def descargar_archivo(nombre_archivo):
    """Copia el archivo a la carpeta de Descargas del usuario."""
    ruta = os.path.join(ARCHIVOS_CREADOS_DIR, nombre_archivo)
    if not os.path.exists(ruta):
        raise FileNotFoundError("Archivo no encontrado.")
    
    # Usar la carpeta de Descargas del usuario
    carpeta_descargas = os.path.join(os.path.expanduser("~"), "Downloads")
    destino = os.path.join(carpeta_descargas, nombre_archivo)
    
    # Si ya existe, añadir un número
    contador = 1
    base_nombre, extension = os.path.splitext(nombre_archivo)
    while os.path.exists(destino):
        nuevo_nombre = f"{base_nombre}_{contador}{extension}"
        destino = os.path.join(carpeta_descargas, nuevo_nombre)
        contador += 1
    
    shutil.copy2(ruta, destino)
    return destino

def obtener_ruta_plantilla():
    """Retorna la ruta de la plantilla Excel"""
    return PLANTILLA_EXCEL

def obtener_ruta_config():
    """Retorna la ruta del directorio de configuración"""
    return CONFIG_DIR
