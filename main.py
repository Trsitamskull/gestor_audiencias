#!/usr/bin/env python3
"""
Gestor de Audiencias - Aplicación para gestionar y ordenar audiencias judiciales.

Este es el punto de entrada principal de la aplicación refactorizada.
Autor: Jose David Bustamante Sánchez
Año: 2025
"""

import sys
import os
from pathlib import Path

# Agregar el directorio raíz del proyecto al path de Python
proyecto_root = Path(__file__).parent
sys.path.insert(0, str(proyecto_root))

def main():
    """Función principal que inicia la aplicación."""
    try:
        # Importar la ventana principal
        from gui.main_window import VentanaPrincipal
        
        # Crear y ejecutar la aplicación
        print("Iniciando Gestor de Audiencias...")
        app = VentanaPrincipal()
        app.ejecutar()
        
    except ImportError as e:
        print(f"Error de importación: {e}")
        print("Asegúrese de que todas las dependencias estén instaladas.")
        print("Ejecute: pip install openpyxl ttkbootstrap")
        sys.exit(1)
    except Exception as e:
        print(f"Error inesperado: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()