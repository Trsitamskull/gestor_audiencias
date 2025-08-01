#!/usr/bin/env python3
"""
Script para generar ejecutable (.exe) del Gestor de Audiencias
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

def mostrar_banner():
    """Muestra el banner de construcción"""
    print("🏗️" + "="*50)
    print("   GESTOR DE AUDIENCIAS - GENERADOR EXE")
    print("   Creando ejecutable independiente")
    print("="*52)
    print()

def verificar_dependencias():
    """Verifica que PyInstaller esté instalado"""
    try:
        import PyInstaller
        print("✅ PyInstaller encontrado")
        return True
    except ImportError:
        print("❌ PyInstaller no encontrado")
        print("📦 Instalando PyInstaller...")
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
            print("✅ PyInstaller instalado")
            return True
        except subprocess.CalledProcessError:
            print("❌ Error al instalar PyInstaller")
            return False

def limpiar_directorios():
    """Limpia directorios de construcciones anteriores"""
    print("\n🧹 LIMPIANDO ARCHIVOS TEMPORALES...")
    print("-" * 35)
    
    directorios_a_limpiar = ["build", "dist", "__pycache__"]
    archivos_a_limpiar = ["*.spec"]
    
    for directorio in directorios_a_limpiar:
        if os.path.exists(directorio):
            shutil.rmtree(directorio)
            print(f"🗑️  Eliminado: {directorio}/")
    
    # Limpiar archivos .spec
    for spec_file in Path(".").glob("*.spec"):
        spec_file.unlink()
        print(f"🗑️  Eliminado: {spec_file}")
    
    print("✅ Limpieza completada")

def crear_spec_file():
    """Crea el archivo de configuración .spec personalizado"""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

import os
from pathlib import Path

# Obtener rutas del proyecto
project_dir = Path(os.getcwd())
templates_dir = project_dir / "templates"
config_dir = project_dir / "config"

block_cipher = None

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        # Incluir plantilla Excel
        (str(templates_dir / "plantilla_audiencias.xlsx"), "templates"),
        # Incluir template de configuración
        (str(config_dir / "config_template.py"), "config"),
    ],
    hiddenimports=[
        'flet',
        'flet.core',
        'openpyxl',
        'openai',
        'gui.main_window',
        'gui.dialogs',
        'gui.widgets',
        'gui.constants',
        'models.audiencia',
        'models.excel_manager',
        'services.ai_service',
        'utils.validators',
        'utils.file_manager',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='GestorAudiencias',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # Sin ventana de consola
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Aquí puedes agregar un icono .ico
    version_file=None,
)
'''
    
    with open("gestor_audiencias.spec", "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    print("✅ Archivo .spec creado")

def generar_ejecutable():
    """Genera el ejecutable usando PyInstaller"""
    print("\n🔨 GENERANDO EJECUTABLE...")
    print("-" * 26)
    
    try:
        # Comando para generar el ejecutable
        cmd = [
            "pyinstaller",
            "--clean",
            "--noconfirm",
            "gestor_audiencias.spec"
        ]
        
        print(f"🔧 Ejecutando: {' '.join(cmd)}")
        print("⏳ Esto puede tomar varios minutos...")
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Ejecutable generado exitosamente")
            return True
        else:
            print("❌ Error al generar ejecutable:")
            print(result.stderr)
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def crear_distribuible():
    """Crea la estructura final distribuible"""
    print("\n📦 CREANDO DISTRIBUCIÓN FINAL...")
    print("-" * 32)
    
    dist_dir = Path("dist")
    exe_file = dist_dir / "GestorAudiencias.exe"
    
    if not exe_file.exists():
        print("❌ Ejecutable no encontrado")
        return False
    
    # Crear directorio de distribución
    final_dir = Path("GestorAudiencias_v2.0")
    if final_dir.exists():
        shutil.rmtree(final_dir)
    
    final_dir.mkdir()
    
    # Copiar ejecutable
    shutil.copy2(exe_file, final_dir / "GestorAudiencias.exe")
    print("✅ Ejecutable copiado")
    
    # Crear README para distribución
    readme_dist = f"""# 🏛️ Gestor de Audiencias v2.0

## 🚀 INSTALACIÓN RÁPIDA

### ✅ **Opción 1: Solo Ejecutable**
1. Ejecuta: `GestorAudiencias.exe`
2. ¡Listo! El sistema funcionará sin configuración adicional

### 🤖 **Opción 2: Con Inteligencia Artificial** 
1. Ejecuta: `GestorAudiencias.exe`
2. Ve a la carpeta `config/` que se creará automáticamente
3. Edita `config_template.py` con tu API key de OpenAI
4. Renómbralo a `config.py`
5. ¡Disfruta de la IA integrada!

## 💰 **Costo de la IA**
- **$5 USD** = 6,000-8,000 audiencias procesadas
- **Duración**: 6-12 meses de uso normal
- **Modelo**: GPT-4o-mini (máxima precisión)

## 🔑 **Para obtener API Key de OpenAI:**
1. Ve a: https://platform.openai.com/api-keys
2. Crea cuenta e inicia sesión
3. Crea nueva API key
4. Agrega $5 USD de crédito
5. ¡Listo!

## 📝 **Uso Básico**
1. **Crear archivo**: Botón "Nuevo Archivo"
2. **Autocompletar**: Presiona **Ctrl+I** y pega cualquier texto
3. **Guardar**: Los datos se guardan automáticamente
4. **Ordenar**: Sistema automático por fecha/hora

## 🎯 **Características**
- ✅ **Sin instalaciones**: Ejecutable independiente
- ✅ **IA Integrada**: Reconoce cualquier formato de audiencia
- ✅ **Excel Automático**: Genera archivos organizados
- ✅ **Interfaz Moderna**: Tema claro/oscuro
- ✅ **Validaciones**: Sistema robusto de verificaciones

---
**Desarrollado por Jose David Bustamante Sánchez - 2025**
"""
    
    with open(final_dir / "README.txt", "w", encoding="utf-8") as f:
        f.write(readme_dist)
    
    print("✅ README de distribución creado")
    
    # Crear script de configuración rápida
    config_script = """@echo off
echo.
echo ===============================================
echo   🤖 CONFIGURADOR RÁPIDO DE IA
echo   Gestor de Audiencias v2.0
echo ===============================================
echo.

if not exist "config" mkdir config

if not exist "config\\config.py" (
    echo 🔧 Configurando OpenAI...
    echo.
    set /p api_key="Pega tu API key de OpenAI (sk-proj-...): "
    
    echo # Configuración de OpenAI > config\\config.py
    echo OPENAI_API_KEY = "%api_key%" >> config\\config.py
    echo OPENAI_MODEL = "gpt-4o-mini" >> config\\config.py
    
    echo.
    echo ✅ IA configurada correctamente
    echo 💰 Costo: ~$0.0008 por audiencia compleja
    echo.
) else (
    echo ✅ OpenAI ya está configurado
    echo.
)

echo 🚀 Iniciando Gestor de Audiencias...
GestorAudiencias.exe

pause
"""
    
    with open(final_dir / "configurar_ia.bat", "w", encoding="utf-8") as f:
        f.write(config_script)
    
    print("✅ Script de configuración creado")
    
    return True

def mostrar_resumen(success=True):
    """Muestra el resumen final"""
    if success:
        print("\n🎉 EJECUTABLE GENERADO EXITOSAMENTE")
        print("="*35)
        print()
        print("📁 ARCHIVOS GENERADOS:")
        print("├── 📂 GestorAudiencias_v2.0/")
        print("│   ├── 🚀 GestorAudiencias.exe")
        print("│   ├── 📖 README.txt")
        print("│   └── ⚙️ configurar_ia.bat")
        print()
        print("🎯 DISTRIBUCIÓN LISTA:")
        print("• Comparte la carpeta 'GestorAudiencias_v2.0'")
        print("• Los usuarios solo necesitan ejecutar el .exe")
        print("• IA opcional con configuración guiada")
        print()
        print("💡 PRUEBA LOCAL:")
        print("1. Ve a: GestorAudiencias_v2.0/")
        print("2. Ejecuta: GestorAudiencias.exe")
        print("3. Para IA: configurar_ia.bat")
    else:
        print("\n❌ ERROR AL GENERAR EJECUTABLE")
        print("="*30)
        print("🔧 Posibles soluciones:")
        print("• Verifica que todas las dependencias estén instaladas")
        print("• Ejecuta: pip install -r requirements.txt")
        print("• Revisa los mensajes de error anteriores")

def main():
    """Función principal"""
    mostrar_banner()
    
    # Verificar dependencias
    if not verificar_dependencias():
        mostrar_resumen(False)
        sys.exit(1)
    
    # Limpiar directorios anteriores
    limpiar_directorios()
    
    # Crear archivo spec
    crear_spec_file()
    
    # Generar ejecutable
    if not generar_ejecutable():
        mostrar_resumen(False)
        sys.exit(1)
    
    # Crear distribución final
    if not crear_distribuible():
        mostrar_resumen(False)
        sys.exit(1)
    
    # Mostrar resumen exitoso
    mostrar_resumen(True)

if __name__ == "__main__":
    main()
