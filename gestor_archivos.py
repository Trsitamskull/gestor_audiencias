import os
import sys
import shutil

def obtener_directorio_real():
    """Devuelve la carpeta donde realmente se encuentra el .exe o .py"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = obtener_directorio_real()
plantilla_excel = os.path.join(BASE_DIR, "plantilla_audiencias.xlsx")
CARPETA_ARCHIVOS = os.path.join(BASE_DIR, "archivos_creados")

os.makedirs(CARPETA_ARCHIVOS, exist_ok=True)

def crear_carpeta_si_no_existe():
    if not os.path.exists(CARPETA_ARCHIVOS):
        os.makedirs(CARPETA_ARCHIVOS)

def crear_copia_plantilla(nombre_archivo):
    crear_carpeta_si_no_existe()
    destino = os.path.join(CARPETA_ARCHIVOS, nombre_archivo)
    if os.path.exists(destino):
        raise FileExistsError("Ya existe un archivo con ese nombre.")
    shutil.copy2(plantilla_excel, destino)
    return destino

def listar_archivos_creados():
    crear_carpeta_si_no_existe()
    return [f for f in os.listdir(CARPETA_ARCHIVOS) if f.endswith(".xlsx")]

def seleccionar_archivo(nombre_archivo):
    ruta = os.path.join(CARPETA_ARCHIVOS, nombre_archivo)
    if not os.path.exists(ruta):
        raise FileNotFoundError("Archivo no encontrado.")
    return ruta

def eliminar_archivo(nombre_archivo):
    ruta = os.path.join(CARPETA_ARCHIVOS, nombre_archivo)
    if os.path.exists(ruta):
        os.remove(ruta)
        return True
    return False

def descargar_archivo(nombre_archivo):
    """Copia el archivo a la carpeta de Descargas del usuario."""
    ruta = os.path.join(CARPETA_ARCHIVOS, nombre_archivo)
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