"""
Constantes de colores y estilos para la aplicación Gestor de Audiencias.
Centraliza todos los colores para facilitar el mantenimiento y consistencia visual.
"""

# Colores principales
PRIMARY_BLUE = "#1E40AF"
PRIMARY_BLUE_LIGHT = "#DBEAFE"
PRIMARY_BLUE_DARK = "#1E3A8A"

# Colores de superficie
SURFACE_WHITE = "#FFFFFF"
SURFACE_LIGHT_GRAY = "#F8FAFC"
SURFACE_GRAY = "#F9FAFB"
SURFACE_BORDER_GRAY = "#E5E7EB"

# Colores de texto
TEXT_PRIMARY = "#1F2937"
TEXT_SECONDARY = "#6B7280"
TEXT_MUTED = "#9CA3AF"

# Colores de estado
SUCCESS_GREEN = "#059669"
SUCCESS_GREEN_LIGHT = "#ECFDF5"
ERROR_RED = "#DC2626"
ERROR_RED_LIGHT = "#FEF2F2"
WARNING_YELLOW = "#F59E0B"
WARNING_YELLOW_LIGHT = "#FFFBEB"

# Colores específicos para motivos de no realización
MOTIVO_BG = "#FEF2F2"
MOTIVO_BORDER = "#FECACA"
MOTIVO_TEXT = "#DC2626"

# Estilos de botón reutilizables
BUTTON_STYLE_PRIMARY = {
    "bgcolor": PRIMARY_BLUE,
    "color": SURFACE_WHITE,
    "elevation": 2,
    "shape": {"radius": 8},
    "padding": {"horizontal": 20, "vertical": 10},
}

BUTTON_STYLE_SECONDARY = {
    "bgcolor": TEXT_SECONDARY,
    "color": SURFACE_WHITE,
    "elevation": 2,
    "shape": {"radius": 8},
    "padding": {"horizontal": 20, "vertical": 10},
}

BUTTON_STYLE_DANGER = {
    "bgcolor": ERROR_RED,
    "color": SURFACE_WHITE,
    "elevation": 2,
    "shape": {"radius": 8},
    "padding": {"horizontal": 20, "vertical": 10},
}

# Estilos de campo de entrada
FIELD_STYLE = {
    "border_radius": 10,
    "filled": True,
    "bgcolor": SURFACE_WHITE,
    "border_color": SURFACE_BORDER_GRAY,
    "focused_border_color": PRIMARY_BLUE,
    "text_style": {"size": 14, "color": TEXT_PRIMARY},
    "label_style": {"size": 13, "color": TEXT_SECONDARY},
    "content_padding": {"all": 12},
}
