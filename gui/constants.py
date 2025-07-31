"""
Constantes de colores y estilos para la aplicación Gestor de Audiencias.
Centraliza todos los colores para facilitar el mantenimiento y consistencia visual.
Soporta temas claro y oscuro con toggle dinámico.
"""

import flet as ft

# ============================================
# SISTEMA DE TEMAS - CLARO Y OSCURO
# ============================================

class ThemeColors:
    """Colores para el sistema de temas"""
    
    # TEMA CLARO
    LIGHT = {
        # Colores principales
        "primary": "#1E40AF",
        "primary_light": "#DBEAFE", 
        "primary_dark": "#1E3A8A",
        
        # Superficies
        "surface_primary": "#FFFFFF",
        "surface_secondary": "#F8FAFC",
        "surface_tertiary": "#F9FAFB",
        "surface_border": "#E5E7EB",
        "surface_card": "#FFFFFF",
        
        # Texto
        "text_primary": "#1F2937",
        "text_secondary": "#6B7280", 
        "text_muted": "#9CA3AF",
        "text_on_primary": "#FFFFFF",
        
        # Estados
        "success": "#059669",
        "success_light": "#ECFDF5",
        "error": "#DC2626", 
        "error_light": "#FEF2F2",
        "warning": "#F59E0B",
        "warning_light": "#FFFBEB",
        
        # Específicos
        "motivo_bg": "#FEF2F2",
        "motivo_border": "#FECACA",
        "header_bg": "#FFFFFF",
        "form_bg": "#F8FAFC",
    }
    
    # TEMA OSCURO
    DARK = {
        # Colores principales
        "primary": "#3B82F6",
        "primary_light": "#1E40AF",
        "primary_dark": "#1D4ED8",
        
        # Superficies
        "surface_primary": "#1F2937",
        "surface_secondary": "#111827", 
        "surface_tertiary": "#374151",
        "surface_border": "#4B5563",
        "surface_card": "#374151",
        
        # Texto
        "text_primary": "#F9FAFB",
        "text_secondary": "#D1D5DB",
        "text_muted": "#9CA3AF", 
        "text_on_primary": "#FFFFFF",
        
        # Estados
        "success": "#10B981",
        "success_light": "#064E3B",
        "danger": "#F97316",       # Naranja suave para botones de peligro
        "error": "#F97316",        # Naranja suave en lugar de rojo
        "error_light": "#9A3412",  # Naranja oscuro en lugar de rojo oscuro
        "warning": "#F59E0B",
        "warning_light": "#78350F",
        
        # Específicos
        "motivo_bg": "#9A3412",    # Naranja oscuro en lugar de rojo
        "motivo_border": "#C2410C", # Naranja medio en lugar de rojo
        "header_bg": "#374151",
        "form_bg": "#111827",
    }

# Variable global para el tema actual
current_theme = "dark"  # Tema oscuro como predeterminado

def get_theme_colors():
    """Obtiene los colores del tema actual"""
    return ThemeColors.LIGHT if current_theme == "light" else ThemeColors.DARK

def toggle_theme():
    """Alterna entre tema claro y oscuro"""
    global current_theme
    current_theme = "dark" if current_theme == "light" else "light"
    return current_theme

def is_dark_theme():
    """Verifica si el tema actual es oscuro"""
    return current_theme == "dark"

# ============================================
# COMPATIBILIDAD CON CÓDIGO EXISTENTE
# ============================================

# Mantener constantes originales para compatibilidad
def _update_legacy_constants():
    """Actualiza las constantes legacy basadas en el tema actual"""
    colors = get_theme_colors()
    
    global PRIMARY_BLUE, PRIMARY_BLUE_LIGHT, PRIMARY_BLUE_DARK
    global SURFACE_WHITE, SURFACE_LIGHT_GRAY, SURFACE_GRAY, SURFACE_BORDER_GRAY
    global TEXT_PRIMARY, TEXT_SECONDARY, TEXT_MUTED
    global SUCCESS_GREEN, SUCCESS_GREEN_LIGHT, ERROR_RED, ERROR_RED_LIGHT
    global WARNING_YELLOW, WARNING_YELLOW_LIGHT, MOTIVO_BG, MOTIVO_BORDER, MOTIVO_TEXT
    
    PRIMARY_BLUE = colors["primary"]
    PRIMARY_BLUE_LIGHT = colors["primary_light"]
    PRIMARY_BLUE_DARK = colors["primary_dark"]
    
    SURFACE_WHITE = colors["surface_primary"]
    SURFACE_LIGHT_GRAY = colors["surface_secondary"]
    SURFACE_GRAY = colors["surface_tertiary"]
    SURFACE_BORDER_GRAY = colors["surface_border"]
    
    TEXT_PRIMARY = colors["text_primary"]
    TEXT_SECONDARY = colors["text_secondary"]
    TEXT_MUTED = colors["text_muted"]
    
    SUCCESS_GREEN = colors["success"]
    SUCCESS_GREEN_LIGHT = colors["success_light"]
    ERROR_RED = colors["error"]
    ERROR_RED_LIGHT = colors["error_light"]
    WARNING_YELLOW = colors["warning"]
    WARNING_YELLOW_LIGHT = colors["warning_light"]
    
    MOTIVO_BG = colors["motivo_bg"]
    MOTIVO_BORDER = colors["motivo_border"]
    MOTIVO_TEXT = colors["error"]

# Inicializar constantes
_update_legacy_constants()

# ============================================
# ESTILOS DINÁMICOS
# ============================================

def get_button_style_primary():
    """Estilo de botón primario dinámico"""
    colors = get_theme_colors()
    return ft.ButtonStyle(
        bgcolor=colors["primary"],
        color=colors["text_on_primary"],
        elevation=2,
        shape=ft.RoundedRectangleBorder(radius=8),
        padding=ft.Padding(20, 10, 20, 10),
    )

def get_button_style_secondary():
    """Estilo de botón secundario dinámico"""
    colors = get_theme_colors()
    return ft.ButtonStyle(
        bgcolor=colors["text_secondary"],
        color=colors["text_on_primary"],
        elevation=2,
        shape=ft.RoundedRectangleBorder(radius=8),
        padding=ft.Padding(20, 10, 20, 10),
    )

def get_button_style_danger():
    """Estilo de botón de peligro dinámico"""
    colors = get_theme_colors()
    return ft.ButtonStyle(
        bgcolor=colors["error"],
        color=colors["text_on_primary"],
        elevation=2,
        shape=ft.RoundedRectangleBorder(radius=8),
        padding=ft.Padding(20, 10, 20, 10),
    )

def get_field_style():
    """Estilo de campo de entrada dinámico"""
    colors = get_theme_colors()
    return {
        "border_radius": 10,
        "filled": True,
        "bgcolor": colors["surface_primary"],
        "border_color": colors["surface_border"],
        "focused_border_color": colors["primary"],
        "text_style": ft.TextStyle(size=14, color=colors["text_primary"]),
        "label_style": ft.TextStyle(size=13, color=colors["text_secondary"]),
        "content_padding": ft.Padding(12, 10, 12, 10),
    }

def get_container_style():
    """Estilo de contenedor dinámico"""
    colors = get_theme_colors()
    return {
        "bgcolor": colors["surface_card"],
        "border_radius": 12,
        "border": ft.border.all(1, colors["surface_border"]),
        "shadow": ft.BoxShadow(
            spread_radius=0,
            blur_radius=8,
            color="#00000015" if current_theme == "light" else "#00000030",
            offset=ft.Offset(0, 2),
        )
    }

# ============================================
# CONSTANTES LEGACY (Para compatibilidad)
# ============================================

# Estas se actualizan automáticamente con el tema
PRIMARY_BLUE = None
PRIMARY_BLUE_LIGHT = None 
PRIMARY_BLUE_DARK = None
SURFACE_WHITE = None
SURFACE_LIGHT_GRAY = None
SURFACE_GRAY = None
SURFACE_BORDER_GRAY = None
TEXT_PRIMARY = None
TEXT_SECONDARY = None
TEXT_MUTED = None
SUCCESS_GREEN = None
SUCCESS_GREEN_LIGHT = None
ERROR_RED = None
ERROR_RED_LIGHT = None
WARNING_YELLOW = None
WARNING_YELLOW_LIGHT = None
MOTIVO_BG = None
MOTIVO_BORDER = None
MOTIVO_TEXT = None

# Estilos legacy estáticos (se mantendrán por compatibilidad pero se recomienda usar los dinámicos)
BUTTON_STYLE_PRIMARY = {
    "bgcolor": "#1E40AF",
    "color": "#FFFFFF",
    "elevation": 2,
    "shape": {"radius": 8},
    "padding": {"horizontal": 20, "vertical": 10},
}

BUTTON_STYLE_SECONDARY = {
    "bgcolor": "#6B7280", 
    "color": "#FFFFFF",
    "elevation": 2,
    "shape": {"radius": 8},
    "padding": {"horizontal": 20, "vertical": 10},
}

BUTTON_STYLE_DANGER = {
    "bgcolor": "#DC2626",
    "color": "#FFFFFF",
    "elevation": 2,
    "shape": {"radius": 8},
    "padding": {"horizontal": 20, "vertical": 10},
}

FIELD_STYLE = {
    "border_radius": 10,
    "filled": True,
    "bgcolor": "#FFFFFF",
    "border_color": "#E5E7EB",
    "focused_border_color": "#1E40AF",
    "text_style": {"size": 14, "color": "#1F2937"},
    "label_style": {"size": 13, "color": "#6B7280"},
    "content_padding": {"all": 12},
}
