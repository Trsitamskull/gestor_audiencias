import flet as ft
import traceback
from typing import Optional
from datetime import datetime

from models.audiencia import Audiencia
from models.excel_manager import ExcelManager
from utils.validators import validar_todos_los_datos
from gestor_archivos import (
    crear_copia_plantilla,
    listar_archivos_creados,
    seleccionar_archivo,
    eliminar_archivo,
    descargar_archivo,
)
from gui.constants import (
    get_theme_colors, 
    toggle_theme, 
    is_dark_theme,
    _update_legacy_constants,
    get_button_style_primary,
    get_button_style_secondary,
    get_button_style_danger,
    get_field_style,
    get_container_style,
)


class DialogoCrearArchivo:
    """Diálogo para crear un nuevo archivo con Flet."""
    
    def __init__(self, page: ft.Page, callback):
        self.page = page
        self.callback = callback
        self.dialog = None
        self._crear_dialogo()
    
    def _crear_dialogo(self):
        """Crea el diálogo para crear archivo con colores dinámicos."""
        colors = get_theme_colors()
        
        # Campo de entrada para el nombre
        self.campo_nombre = ft.TextField(
            label="Nombre del archivo",
            hint_text="Ej: audiencias_enero",
            width=300,
            border_radius=10,
            filled=True,
            bgcolor=colors["surface_primary"],
            border_color=colors["surface_border"],
            focused_border_color=colors["primary"],
            text_style=ft.TextStyle(size=14, color=colors["text_primary"]),
            label_style=ft.TextStyle(size=13, color=colors["text_secondary"]),
            content_padding=ft.Padding(12, 10, 12, 10),
            autofocus=True,
        )
        
        # Botones
        btn_crear = ft.ElevatedButton(
            text="Crear",
            on_click=self._on_crear,
            style=ft.ButtonStyle(
                bgcolor=colors["primary"],
                color=colors["text_on_primary"],
                elevation=2,
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.Padding(20, 10, 20, 10),
            ),
        )
        
        btn_cancelar = ft.TextButton(
            text="Cancelar",
            on_click=self._on_cancelar,
            style=ft.ButtonStyle(
                color=colors["text_secondary"],
                padding=ft.Padding(20, 10, 20, 10),
            ),
        )
        
        # Contenido del diálogo
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Crear Nuevo Archivo", size=18, weight=ft.FontWeight.BOLD, color=colors["text_primary"]),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Ingrese el nombre para el nuevo archivo:",
                            size=14,
                            color=colors["text_secondary"],
                        ),
                        ft.Container(height=10),
                        self.campo_nombre,
                    ],
                    tight=True,
                    spacing=5,
                ),
                width=350,
                height=120,
            ),
            actions=[
                btn_cancelar,
                btn_crear,
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=colors["surface_card"],
        )
        
        # Mostrar el diálogo
        self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()
    
    def _on_crear(self, e):
        """Maneja el click en crear."""
        nombre = self.campo_nombre.value.strip() if self.campo_nombre.value else ""
        
        if not nombre:
            # Mostrar error si no hay nombre
            self.campo_nombre.error_text = "El nombre es obligatorio"
            self.page.update()
            return
        
        # Cerrar diálogo y ejecutar callback
        self.dialog.open = False
        self.page.update()
        self.callback(nombre)
    
    def _on_cancelar(self, e):
        """Maneja el click en cancelar."""
        self.dialog.open = False
        self.page.update()


class VentanaSeleccionArchivo:
    """Diálogo para seleccionar un archivo de una lista con Flet."""
    
    def __init__(self, page: ft.Page, titulo: str, archivos, callback):
        self.page = page
        self.titulo = titulo
        self.archivos = archivos
        self.callback = callback
        self.dialog = None
        self._crear_dialogo()
    
    def _crear_dialogo(self):
        """Crea el diálogo de selección con colores dinámicos."""
        colors = get_theme_colors()
        
        # Lista de archivos como botones
        lista_controles = []
        
        for archivo in self.archivos:
            btn_archivo = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.DESCRIPTION, size=20, color=colors["primary"]),
                        ft.Text(archivo, size=14, color=colors["text_primary"], expand=True),
                        ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=16, color=colors["text_muted"]),
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.START,
                ),
                bgcolor=colors["surface_tertiary"],
                border=ft.border.all(1, colors["surface_border"]),
                border_radius=8,
                padding=ft.Padding(15, 12, 15, 12),
                on_click=lambda e, arch=archivo: self._on_seleccionar(arch),
                ink=True,
            )
            lista_controles.append(btn_archivo)
        
        # Botón cancelar
        btn_cancelar = ft.TextButton(
            text="Cancelar",
            on_click=self._on_cancelar,
            style=ft.ButtonStyle(
                color=colors["text_secondary"],
                padding=ft.Padding(20, 10, 20, 10),
            ),
        )
        
        # Contenido scrollable
        contenido_scroll = ft.Column(
            controls=lista_controles,
            spacing=8,
            scroll=ft.ScrollMode.AUTO,
        )
        
        # Contenedor con altura fija para scroll
        contenedor_lista = ft.Container(
            content=contenido_scroll,
            height=min(300, len(self.archivos) * 60 + 50),  # Altura dinámica
            width=400,
        )
        
        # Diálogo principal
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(self.titulo, size=18, weight=ft.FontWeight.BOLD, color=colors["text_primary"]),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            f"Seleccione uno de los {len(self.archivos)} archivos disponibles:",
                            size=14,
                            color=colors["text_secondary"],
                        ),
                        ft.Container(height=15),
                        contenedor_lista,
                    ],
                    tight=True,
                    spacing=5,
                ),
                width=450,
            ),
            actions=[btn_cancelar],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=colors["surface_card"],
        )
        
        # Mostrar el diálogo
        self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()
    
    def _on_seleccionar(self, archivo: str):
        """Maneja la selección de un archivo."""
        self.dialog.open = False
        self.page.update()
        self.callback(archivo)
    
    def _on_cancelar(self, e):
        """Maneja el click en cancelar."""
        self.dialog.open = False
        self.page.update()


class VentanaSeleccionRegistro:
    """Ventana para seleccionar un registro para editar con Flet."""

    def __init__(self, page: ft.Page, registros, callback):
        self.page = page
        self.registros = registros
        self.callback = callback
        self.dialog = None
        self._crear_dialogo()
    
    def _crear_dialogo(self):
        """Crea el diálogo de selección de registro."""
        # Lista de registros como botones
        lista_controles = []
        
        for i, (fila_num, datos) in enumerate(self.registros):
            # Información del registro
            info_text = f"#{datos[0] or i+1} - {datos[1]} - {datos[2]} - {datos[3]} - {datos[4]}"
            
            btn_registro = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.EDIT_DOCUMENT, size=20, color="#059669"),
                        ft.Text(info_text, size=13, color="#1F2937", expand=True),
                        ft.ElevatedButton(
                            text="Editar",
                            on_click=lambda e, fn=fila_num, d=datos: self._on_editar_item(fn, d),
                            style=ft.ButtonStyle(
                                bgcolor="#059669",
                                color="#FFFFFF",
                                shape=ft.RoundedRectangleBorder(radius=6),
                                padding=ft.Padding(12, 8, 12, 8),
                                text_style=ft.TextStyle(size=12),
                            ),
                        ),
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.START,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor="#F9FAFB",
                border=ft.border.all(1, "#E5E7EB"),
                border_radius=8,
                padding=ft.Padding(15, 12, 15, 12),
            )
            lista_controles.append(btn_registro)
        
        # Botón cancelar
        btn_cancelar = ft.TextButton(
            text="Cancelar",
            on_click=self._on_cancelar,
            style=ft.ButtonStyle(
                color="#6B7280",
                padding=ft.Padding(20, 10, 20, 10),
            ),
        )
        
        # Contenido scrollable
        contenido_scroll = ft.Column(
            controls=lista_controles,
            spacing=8,
            scroll=ft.ScrollMode.AUTO,
        )
        
        # Contenedor con altura fija para scroll
        contenedor_lista = ft.Container(
            content=contenido_scroll,
            height=min(400, len(self.registros) * 70 + 50),  # Altura dinámica
            width=600,
        )
        
        # Diálogo principal
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Seleccionar Registro para Editar", size=18, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            f"Seleccione uno de los {len(self.registros)} registros disponibles para editar:",
                            size=14,
                            color="#6B7280",
                        ),
                        ft.Container(height=15),
                        contenedor_lista,
                    ],
                    tight=True,
                    spacing=5,
                ),
                width=650,
            ),
            actions=[btn_cancelar],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        # Mostrar el diálogo
        self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()
    
    def _on_editar_item(self, fila_num, datos_completos):
        """Maneja la selección de un registro para editar."""
        self.dialog.open = False
        self.page.update()
        self.callback(fila_num, datos_completos)
    
    def _on_cancelar(self, e):
        """Cancela la selección."""
        self.dialog.open = False
        self.page.update()


class DialogoConfirmacion:
    """Diálogo de confirmación con Flet."""
    
    @staticmethod
    def confirmar(page: ft.Page, titulo: str, mensaje: str, callback_si):
        """Muestra un diálogo de confirmación con colores dinámicos."""
        colors = get_theme_colors()
        
        def confirmar_accion(e):
            dlg.open = False
            page.update()
            callback_si()
        
        def cancelar_accion(e):
            dlg.open = False
            page.update()
        
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(titulo, size=18, weight=ft.FontWeight.BOLD, color=colors["text_primary"]),
            content=ft.Text(mensaje, size=14, color=colors["text_secondary"]),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=cancelar_accion,
                    style=ft.ButtonStyle(
                        color=colors["text_secondary"],
                        padding=ft.Padding(20, 10, 20, 10),
                    ),
                ),
                ft.ElevatedButton(
                    "Confirmar",
                    on_click=confirmar_accion,
                    style=ft.ButtonStyle(
                        bgcolor=colors["danger"],
                        color=colors["surface_primary"],
                        elevation=2,
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=ft.Padding(20, 10, 20, 10),
                    ),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            bgcolor=colors["surface_card"],
        )
        
        page.overlay.append(dlg)
        dlg.open = True
        page.update()


class VentanaPrincipal:
    """Ventana principal de la aplicación con Flet - Versión Simple."""

    def __init__(self, page: ft.Page):
        self.page = page
        self.archivo_excel: Optional[str] = None
        self.excel_manager: Optional[ExcelManager] = None
        self.modo_edicion = False
        self.fila_editando: Optional[int] = None

        # Referencias a los controles
        self.entrada_radicado = None
        self.combo_tipo = None
        self.entrada_tipo_otra = None
        self.combo_dia = None
        self.combo_mes = None
        self.combo_anio = None
        self.entrada_hora = None
        self.entrada_minuto = None
        self.entrada_juzgado = None
        self.combo_realizada = None
        self.checkboxes_motivos = []
        self.entrada_observaciones = None
        self.contador_registros = None
        self.archivo_actual_text = None
        self.btn_guardar = None
        self.btn_actualizar = None
        self.btn_cancelar_edicion = None

        # Lista de tipos de audiencia
        self.tipos_audiencia = [
            "Alegatos de conclusión",
            "Audiencia concentrada",
            "Audiencia de acusación",
            "Audiencia de juicio oral",
            "Audiencia de preclusion",
            "Audiencia preliminar",
            "Audiencia preparatoria",
            "Otra",
        ]

        self._configurar_pagina()
        self._crear_interfaz()
        self._inicializar()

    def _configurar_pagina(self):
        """Configura las propiedades de la página."""
        self.page.title = "🏛️ Gestor de Audiencias Judiciales"
        self.page.padding = 0  # Sin padding para usar toda la pantalla
        self.page.scroll = ft.ScrollMode.AUTO
        
        # Aplicar colores del tema actual
        colors = get_theme_colors()
        self.page.bgcolor = colors["surface_secondary"]
        
        # Configurar ventana
        try:
            if hasattr(self.page, 'window'):
                self.page.window.width = 1400
                self.page.window.height = 900
                self.page.window.min_width = 1000
                self.page.window.min_height = 700
        except:
            pass

        # Configurar tema basado en el tema actual
        self.page.theme_mode = ft.ThemeMode.DARK if is_dark_theme() else ft.ThemeMode.LIGHT
        self.page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=colors["primary"],
                on_primary=colors["text_on_primary"],
                surface=colors["surface_primary"],
                on_surface=colors["text_primary"],
            )
        )

    def _toggle_theme(self, e):
        """Alternar entre tema claro y oscuro"""
        # Cambiar el tema
        new_theme = toggle_theme()
        
        # Actualizar constantes legacy
        _update_legacy_constants()
        
        # Reconfigurar la página
        self._configurar_pagina()
        
        # Recrear la interfaz con los nuevos colores
        self.page.clean()
        self._crear_interfaz()
        
        # Reinicializar
        self._inicializar()
        
        # Mostrar mensaje de confirmación
        tema_nombre = "Tema Oscuro" if new_theme == "dark" else "Tema Claro"
        # Usamos un snack bar simple en lugar del método que aún no definimos
        snack = ft.SnackBar(
            ft.Text(f"✅ {tema_nombre} activado", color="#FFFFFF"),
            bgcolor=get_theme_colors()["success"],
        )
        self.page.overlay.append(snack)
        snack.open = True
        self.page.update()

    def _crear_interfaz(self):
        """Crea toda la interfaz de usuario con diseño profesional."""

        # Contenedor principal con padding
        colors = get_theme_colors()
        contenido_principal = ft.Container(
            content=ft.Column(
                controls=[
                    self._crear_header(),
                    ft.Container(height=15),  # Espaciado reducido
                    self._crear_formulario(),  # Ahora incluye los botones integrados
                    ft.Container(height=15),
                    self._crear_gestion_archivos(),
                    ft.Container(height=20),  # Espaciado final
                ],
                expand=True,
                spacing=0,
                scroll=ft.ScrollMode.HIDDEN,  # Sin scroll
            ),
            padding=ft.padding.all(25),  # Padding reducido
            bgcolor=colors["surface_secondary"],
            expand=True,
        )

        # Agregar a la página
        self.page.add(contenido_principal)

    def _crear_header(self):
        """Crea el header profesional moderno con toggle de tema."""
        colors = get_theme_colors()
        
        self.contador_registros = ft.Text(
            "Registros: 0", 
            size=14, 
            weight=ft.FontWeight.W_600,
            color=colors["text_primary"]
        )

        self.archivo_actual_text = ft.Text(
            "Ningún archivo seleccionado",
            size=14,
            weight=ft.FontWeight.W_500,
            color=colors["text_secondary"]
        )

        # Botón de toggle de tema
        theme_icon = ft.Icons.DARK_MODE if not is_dark_theme() else ft.Icons.LIGHT_MODE
        theme_tooltip = "Activar tema oscuro" if not is_dark_theme() else "Activar tema claro"
        
        btn_theme_toggle = ft.IconButton(
            icon=theme_icon,
            tooltip=theme_tooltip,
            on_click=self._toggle_theme,
            icon_color=colors["primary"],
            icon_size=22,
            style=ft.ButtonStyle(
                bgcolor=colors["surface_tertiary"],
                shape=ft.CircleBorder(),
                padding=ft.Padding(8, 8, 8, 8),
            ),
        )

        return ft.Container(
            content=ft.Row(
                controls=[
                    # Logo y título principal
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.GAVEL, 
                                    size=40, 
                                    color=colors["text_on_primary"]
                                ),
                                width=60,
                                height=60,
                                bgcolor=colors["primary"],
                                border_radius=15,
                                alignment=ft.alignment.center,
                            ),
                            ft.Column(
                                controls=[
                                    ft.Text(
                                        "GESTOR DE AUDIENCIAS", 
                                        size=24, 
                                        weight=ft.FontWeight.BOLD, 
                                        color=colors["text_primary"]
                                    ),
                                    ft.Text(
                                        "Sistema Judicial Profesional", 
                                        size=14, 
                                        color=colors["text_secondary"],
                                        italic=True
                                    ),
                                ],
                                spacing=2,
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ],
                        spacing=15,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    
                    # Información del archivo (centrado)
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.FOLDER_OUTLINED, size=18, color=colors["primary"]),
                                self.archivo_actual_text,
                            ],
                            spacing=8,
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        bgcolor=colors["surface_tertiary"],
                        border_radius=20,
                        padding=ft.padding.symmetric(horizontal=20, vertical=12),
                        border=ft.border.all(1, colors["surface_border"]),
                    ),
                    
                    # Contador de registros y toggle de tema
                    ft.Row(
                        controls=[
                            ft.Container(
                                content=ft.Row(
                                    controls=[
                                        ft.Icon(ft.Icons.ANALYTICS_OUTLINED, size=18, color=colors["primary"]),
                                        self.contador_registros,
                                    ],
                                    spacing=8,
                                    alignment=ft.MainAxisAlignment.CENTER,
                                ),
                                bgcolor=colors["primary_light"] if not is_dark_theme() else colors["surface_tertiary"],
                                border_radius=20,
                                padding=ft.padding.symmetric(horizontal=20, vertical=12),
                                border=ft.border.all(1, colors["surface_border"]),
                            ),
                            btn_theme_toggle,
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.END,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=colors["header_bg"],
            border_radius=20,
            padding=30,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=10,
                color="#00000010" if not is_dark_theme() else "#00000030",
                offset=ft.Offset(0, 2),
            ),
            border=ft.border.all(1, colors["surface_border"]),
        )

    def _crear_formulario(self):
        """Crea el formulario principal con diseño de dos columnas sin scroll."""
        colors = get_theme_colors()
        
        # Título principal del formulario (compacto)
        titulo_principal = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.EDIT_NOTE_OUTLINED, size=24, color=colors["primary"]),
                    ft.Text(
                        "INFORMACIÓN DE LA AUDIENCIA", 
                        size=18, 
                        weight=ft.FontWeight.BOLD, 
                        color=colors["primary"]
                    ),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(vertical=10),
        )

        # === COLUMNA IZQUIERDA ===
        columna_izquierda = ft.Column(
            controls=[
                # SECCIÓN 1: IDENTIFICACIÓN DEL PROCESO
                ft.Container(
                    content=ft.Column(
                        controls=[
                            # Encabezado de sección (compacto)
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.FOLDER_OUTLINED, size=18, color=colors["text_primary"]),
                                    ft.Text(
                                        "IDENTIFICACIÓN DEL PROCESO",
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                        color=colors["text_primary"]
                                    ),
                                ],
                                spacing=8,
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            ft.Container(height=10),  # Espaciado reducido
                            
                            # Campos: Radicado y Juzgado (uno debajo del otro)
                            self._crear_campo_radicado(),
                            ft.Container(height=8),
                            self._crear_campo_juzgado(),
                        ],
                        spacing=3,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    bgcolor=colors["surface_tertiary"],
                    border_radius=10,
                    padding=ft.padding.all(15),
                    border=ft.border.all(1, colors["surface_border"]),
                ),
                
                ft.Container(height=15),  # Espaciado entre secciones
                
                # SECCIÓN 2: CONFIGURACIÓN DE LA AUDIENCIA
                ft.Container(
                    content=ft.Column(
                        controls=[
                            # Encabezado de sección (compacto)
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.SETTINGS_OUTLINED, size=18, color=colors["text_primary"]),
                                    ft.Text(
                                        "CONFIGURACIÓN DE LA AUDIENCIA",
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                        color=colors["text_primary"]
                                    ),
                                ],
                                spacing=8,
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            ft.Container(height=10),
                            
                            # Campos: Tipo de audiencia y ¿Se realizó?
                            self._crear_campo_tipo_audiencia(),
                            ft.Container(height=8),
                            self._crear_campo_realizada(),
                        ],
                        spacing=3,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    bgcolor=colors["surface_tertiary"],
                    border_radius=10,
                    padding=ft.padding.all(15),
                    border=ft.border.all(1, colors["surface_border"]),
                ),
            ],
            expand=True,
            spacing=0,
            alignment=ft.MainAxisAlignment.START,  # Alineación desde arriba
        )

        # === COLUMNA DERECHA ===
        columna_derecha = ft.Column(
            controls=[
                # SECCIÓN 3: PROGRAMACIÓN (FECHA Y HORA)
                ft.Container(
                    content=ft.Column(
                        controls=[
                            # Encabezado de sección (compacto)
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.SCHEDULE_OUTLINED, size=18, color=colors["text_primary"]),
                                    ft.Text(
                                        "PROGRAMACIÓN",
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                        color=colors["text_primary"]
                                    ),
                                ],
                                spacing=8,
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            ft.Container(height=10),
                            
                            # Campos: Fecha y Hora (uno debajo del otro)
                            self._crear_campo_fecha(),
                            ft.Container(height=8),
                            self._crear_campo_hora(),
                        ],
                        spacing=3,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    bgcolor=colors["surface_tertiary"],
                    border=ft.border.all(1, colors["surface_border"]),
                    border_radius=10,
                    padding=15,
                ),
                
                ft.Container(height=15),
                
                # SECCIÓN 4: MOTIVOS DE NO REALIZACIÓN
                ft.Container(
                    content=ft.Column(
                        controls=[
                            # Encabezado de sección (compacto)
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.ERROR_OUTLINE, size=18, color=colors["error"]),
                                    ft.Text(
                                        "MOTIVOS DE NO REALIZACIÓN",
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                        color=colors["error"]
                                    ),
                                ],
                                spacing=8,
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            ft.Container(height=10),
                            
                            # Campo de motivos (compacto)
                            self._crear_campo_motivos(),
                        ],
                        spacing=3,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                    bgcolor=colors["error_light"],
                    border_radius=12,
                    padding=ft.padding.all(18),
                    border=ft.border.all(1, colors["error"]),
                    shadow=ft.BoxShadow(
                        spread_radius=0,
                        blur_radius=8,
                        color=f"{colors['error']}20",
                        offset=ft.Offset(0, 2),
                    ),
                ),
            ],
            expand=True,
            spacing=0,
            alignment=ft.MainAxisAlignment.START,  # Alineación desde arriba
        )

        # === ROW PRINCIPAL CON LAS DOS COLUMNAS ===
        row_principal = ft.Row(
            controls=[
                columna_izquierda,
                ft.Container(width=20),  # Espaciado entre columnas
                columna_derecha,
            ],
            expand=True,
            spacing=0,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,  # Alineación vertical desde arriba
        )

        # === SECCIÓN DE OBSERVACIONES (ANCHO COMPLETO) ===
        seccion_observaciones = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            # Encabezado de sección (compacto)
                            ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.NOTES_OUTLINED, size=18, color=colors["text_primary"]),
                                    ft.Text(
                                        "OBSERVACIONES ADICIONALES",
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                        color=colors["text_primary"]
                                    ),
                                ],
                                spacing=8,
                            ),
                            ft.Container(height=8),
                            
                            # Campo de observaciones (reducido a 2 líneas)
                            self._crear_campo_observaciones_compacto(),
                        ],
                        spacing=3,
                    ),
                    bgcolor=colors["surface_tertiary"],
                    border=ft.border.all(1, colors["surface_border"]),
                    border_radius=10,
                    padding=15,
                    expand=1,
                ),
            ],
        )

        # === BOTONES DE ACCIÓN (ANCHO COMPLETO) ===
        seccion_botones = ft.Row(
            controls=[
                self._crear_botones_accion_compactos(),
            ],
            expand=True,
        )

        # === CONTENEDOR PRINCIPAL SIN SCROLL ===
        colors = get_theme_colors()
        return ft.Container(
            content=ft.Column(
                controls=[
                    titulo_principal,
                    ft.Divider(height=1, color=colors["surface_border"]),
                    ft.Container(height=15),  # Espaciado reducido
                    
                    row_principal,  # Las dos columnas principales
                    ft.Container(height=15),
                    
                    seccion_observaciones,  # Observaciones ancho completo
                    ft.Container(height=15),
                    
                    seccion_botones,  # Botones ancho completo
                ],
                spacing=0,
                expand=True,
                scroll=ft.ScrollMode.HIDDEN,  # Sin scroll
            ),
            bgcolor=colors["form_bg"], 
            border_radius=16,
            padding=ft.padding.all(20),  # Padding reducido
            expand=True,
        )

    def _crear_campo_radicado(self):
        """Campo de radicado con diseño mejorado y colores dinámicos."""
        colors = get_theme_colors()
        self.entrada_radicado = ft.TextField(
            label="Número de radicado",
            hint_text="Ej: 11001-60-00000-2024-00000-00",
            border_radius=12,
            filled=True,
            bgcolor=colors["surface_primary"],
            border_color=colors["surface_border"],
            focused_border_color=colors["primary"],
            prefix_icon=ft.Icons.FOLDER_OUTLINED,
            text_style=ft.TextStyle(size=14, color=colors["text_primary"]),
            label_style=ft.TextStyle(size=13, color=colors["text_secondary"]),
            content_padding=ft.Padding(12, 10, 12, 10),
        )
        return self.entrada_radicado

    def _crear_campo_tipo_audiencia(self):
        """Campo de tipo de audiencia con diseño mejorado y colores dinámicos."""
        colors = get_theme_colors()
        
        self.combo_tipo = ft.Dropdown(
            label="Tipo de audiencia",
            hint_text="Seleccione el tipo de audiencia...",
            options=[ft.dropdown.Option(tipo) for tipo in self.tipos_audiencia],
            on_change=self._on_tipo_change,
            border_radius=12,
            filled=True,
            bgcolor=colors["surface_primary"],
            border_color=colors["surface_border"],
            focused_border_color=colors["primary"],
            text_style=ft.TextStyle(size=14, color=colors["text_primary"]),
            label_style=ft.TextStyle(size=13, color=colors["text_secondary"]),
            content_padding=ft.Padding(12, 10, 12, 10),
        )

        self.entrada_tipo_otra = ft.TextField(
            label="Especificar otro tipo",
            hint_text="Escriba el tipo de audiencia...",
            border_radius=12,
            filled=True,
            bgcolor=colors["warning_light"],
            border_color=colors["warning"],
            focused_border_color=colors["warning"],
            text_style=ft.TextStyle(size=14, color=colors["text_primary"]),
            label_style=ft.TextStyle(size=13, color=colors["warning"]),
            content_padding=ft.Padding(12, 10, 12, 10),
            visible=False,
        )

        return ft.Column(
            controls=[
                self.combo_tipo,
                self.entrada_tipo_otra,
            ],
            spacing=10,
        )

    def _crear_campo_fecha(self):
        """Campo de fecha con DatePicker unificado y formateo en tiempo real."""
        colors = get_theme_colors()
        
        # DatePicker principal
        self.date_picker = ft.DatePicker(
            first_date=datetime(datetime.now().year - 1, 1, 1),
            last_date=datetime(datetime.now().year + 5, 12, 31),
            on_change=self._on_date_picker_change,
        )
        
        # Campo de texto con formateo automático en tiempo real
        self.entrada_fecha = ft.TextField(
            label="Fecha (DD/MM/AAAA)",
            hint_text="Ej: 22072025 → 22/07/2025",
            width=200,
            max_length=10,  # DD/MM/AAAA = 10 caracteres
            border_radius=10,
            filled=True,
            bgcolor=colors["surface_primary"],
            border_color=colors["surface_border"],
            focused_border_color=colors["primary"],
            text_style=ft.TextStyle(size=13, color=colors["text_primary"]),
            label_style=ft.TextStyle(size=12, color=colors["text_secondary"]),
            content_padding=ft.Padding(12, 10, 12, 10),
            on_change=self._on_fecha_change_tiempo_real,
        )
        
        # Botón del calendario alineado junto al campo
        btn_calendario = ft.IconButton(
            icon=ft.Icons.CALENDAR_TODAY_OUTLINED,
            tooltip="Abrir calendario",
            on_click=self._abrir_date_picker,
            icon_color=colors["primary"],
            icon_size=20,
            style=ft.ButtonStyle(
                bgcolor=colors["surface_tertiary"],
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.Padding(8, 8, 8, 8),
            ),
        )
        
        # Row para alinear campo y botón lado a lado
        campo_fecha_row = ft.Row(
            controls=[
                self.entrada_fecha,
                btn_calendario,
            ],
            spacing=8,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        
        # Agregar el DatePicker a la página
        self.page.overlay.append(self.date_picker)
        
        # Campos virtuales para compatibilidad con lógica existente
        self.combo_dia = ft.Dropdown(
            options=[ft.dropdown.Option(f"{i:02d}") for i in range(1, 32)],
            width=80,
            value=None,
        )
        self.combo_mes = ft.Dropdown(
            options=[ft.dropdown.Option(f"{i:02d}") for i in range(1, 13)],
            width=80,
            value=None,
        )
        self.combo_anio = ft.Dropdown(
            options=[ft.dropdown.Option(str(i)) for i in range(2020, 2031)],
            width=100,
            value=None,
        )

        return campo_fecha_row

    def _crear_campo_hora(self):
        """Campo de hora con selección automática de texto al hacer clic y colores dinámicos."""
        colors = get_theme_colors()
        
        # Estilo dinámico para campos de hora
        estilo_hora = {
            "border_radius": 10,
            "filled": True,
            "bgcolor": colors["surface_primary"],
            "border_color": colors["surface_border"],
            "focused_border_color": colors["primary"],
            "text_style": ft.TextStyle(size=13, color=colors["text_primary"]),
            "label_style": ft.TextStyle(size=12, color=colors["text_secondary"]),
            "text_align": ft.TextAlign.CENTER,
            "content_padding": ft.Padding(12, 10, 12, 10),
        }

        def _seleccionar_texto_hora(e):
            """Selecciona todo el contenido del campo hora al hacer clic."""
            if e.control.value:
                e.control.selection = ft.TextSelection(0, len(e.control.value))
                e.control.update()

        def _seleccionar_texto_minuto(e):
            """Selecciona todo el contenido del campo minuto al hacer clic."""
            if e.control.value:
                e.control.selection = ft.TextSelection(0, len(e.control.value))
                e.control.update()

        self.entrada_hora = ft.TextField(
            label="Hora",
            hint_text="00",
            width=85,
            max_length=2,
            on_click=_seleccionar_texto_hora,
            **estilo_hora
        )

        self.entrada_minuto = ft.TextField(
            label="Min",
            hint_text="00",
            width=85,
            max_length=2,
            on_click=_seleccionar_texto_minuto,
            **estilo_hora
        )

        return ft.Row(
            controls=[
                self.entrada_hora,
                ft.Container(
                    content=ft.Text(":", size=20, color=colors["text_secondary"], weight=ft.FontWeight.BOLD),
                    margin=ft.Margin(0, 15, 0, 0),  # Ajustar la posición vertical del separador
                ),
                self.entrada_minuto,
            ],
            spacing=8,
            alignment=ft.MainAxisAlignment.START,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

    def _crear_campo_juzgado(self):
        """Campo de juzgado con diseño mejorado y colores dinámicos."""
        colors = get_theme_colors()
        self.entrada_juzgado = ft.TextField(
            label="Juzgado o entidad",
            hint_text="Nombre del juzgado o entidad judicial",
            border_radius=12,
            filled=True,
            bgcolor=colors["surface_primary"],
            border_color=colors["surface_border"],
            focused_border_color=colors["primary"],
            prefix_icon=ft.Icons.ACCOUNT_BALANCE_OUTLINED,
            text_style=ft.TextStyle(size=14, color=colors["text_primary"]),
            label_style=ft.TextStyle(size=13, color=colors["text_secondary"]),
            content_padding=ft.Padding(12, 10, 12, 10),
        )
        return self.entrada_juzgado

    def _crear_campo_realizada(self):
        """Campo ¿Se realizó? con diseño mejorado y colores dinámicos."""
        colors = get_theme_colors()
        self.combo_realizada = ft.Dropdown(
            label="¿Se realizó?",
            hint_text="Seleccione SI o NO",
            options=[ft.dropdown.Option("SI"), ft.dropdown.Option("NO")],
            on_change=self._on_realizada_change,
            border_radius=10,
            filled=True,
            bgcolor=colors["surface_primary"],
            border_color=colors["surface_border"],
            focused_border_color=colors["primary"],
            text_style=ft.TextStyle(size=13, color=colors["text_primary"]),
            label_style=ft.TextStyle(size=12, color=colors["text_secondary"]),
            content_padding=ft.Padding(12, 10, 12, 10),
        )
        return self.combo_realizada

    def _crear_campo_motivos(self):
        """Campo de motivos con diseño mejorado y checkboxes optimizados con colores dinámicos."""
        colors = get_theme_colors()
        
        motivos_labels = [
            "Juez", "Fiscalía", "Usuario", "INPEC",
            "Víctima", "ICBF", "Defensor Confianza", "Defensor Público",
        ]

        self.checkboxes_motivos = []
        checkboxes_row1 = []
        checkboxes_row2 = []

        # Estilo mejorado para checkboxes con colores dinámicos
        for i, motivo in enumerate(motivos_labels):
            checkbox = ft.Checkbox(
                label=motivo,
                disabled=True,
                label_style=ft.TextStyle(size=13, color=colors["text_secondary"]),
                check_color=colors["error"],
                active_color=colors["error_light"],
            )
            self.checkboxes_motivos.append(checkbox)

            if i < 4:
                checkboxes_row1.append(checkbox)
            else:
                checkboxes_row2.append(checkbox)

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=checkboxes_row1,
                        spacing=10,
                        alignment=ft.MainAxisAlignment.START,
                        wrap=False,
                    ),
                    ft.Row(
                        controls=checkboxes_row2,
                        spacing=10,
                        alignment=ft.MainAxisAlignment.START,
                        wrap=False,
                    ),
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.START,
            ),
            bgcolor=colors["error_light"],
            border_radius=10,
            padding=ft.Padding(15, 12, 15, 12),
            border=ft.border.all(1, colors["error"]),
        )

    def _crear_campo_observaciones(self):
        """Campo de observaciones con diseño mejorado y colores claros."""
        self.entrada_observaciones = ft.TextField(
            label="Observaciones",
            hint_text="Detalles adicionales de la audiencia...",
            multiline=True,
            min_lines=3,
            max_lines=5,
            border_radius=10,
            filled=True,
            bgcolor="#FFFFFF",  # Fondo blanco completamente claro
            border_color="#E5E7EB",
            focused_border_color="#1E40AF",
            text_style=ft.TextStyle(size=13, color="#1F2937"),
            label_style=ft.TextStyle(size=12, color="#6B7280"),
            content_padding=ft.Padding(12, 10, 12, 10),
        )
        return self.entrada_observaciones

    def _crear_campo_observaciones_compacto(self):
        """Campo de observaciones compacto para layout de dos columnas con colores dinámicos."""
        colors = get_theme_colors()
        self.entrada_observaciones = ft.TextField(
            label="Observaciones",
            hint_text="Detalles adicionales de la audiencia...",
            multiline=True,
            min_lines=2,
            max_lines=3,  # Reducido para que quepa en pantalla
            border_radius=10,
            filled=True,
            bgcolor=colors["surface_primary"],
            border_color=colors["surface_border"],
            focused_border_color=colors["primary"],
            text_style=ft.TextStyle(size=13, color=colors["text_primary"]),
            label_style=ft.TextStyle(size=12, color=colors["text_secondary"]),
            content_padding=ft.Padding(12, 8, 12, 8),  # Padding reducido
        )
        return self.entrada_observaciones

    def _crear_botones_accion(self):
        """Crea los botones de acción con diseño profesional."""
        self.btn_guardar = ft.ElevatedButton(
            text="💾 GUARDAR AUDIENCIA",
            on_click=self._on_guardar,
            style=ft.ButtonStyle(
                bgcolor="#1E40AF",
                color="#FFFFFF",
                elevation=3,
                shape=ft.RoundedRectangleBorder(radius=12),
                padding=ft.Padding(20, 15, 20, 15),
                text_style=ft.TextStyle(size=16, weight=ft.FontWeight.W_600),
            ),
            expand=True,
        )

        self.btn_actualizar = ft.ElevatedButton(
            text="✏️ ACTUALIZAR REGISTRO",
            on_click=self._on_actualizar,
            style=ft.ButtonStyle(
                bgcolor="#059669",
                color="#FFFFFF",
                elevation=3,
                shape=ft.RoundedRectangleBorder(radius=12),
                padding=ft.Padding(20, 15, 20, 15),
                text_style=ft.TextStyle(size=16, weight=ft.FontWeight.W_600),
            ),
            expand=True,
            visible=False,
        )

        self.btn_cancelar_edicion = ft.ElevatedButton(
            text="❌ CANCELAR EDICIÓN",
            on_click=self._on_cancelar_edicion,
            style=ft.ButtonStyle(
                bgcolor="#DC2626",
                color="#FFFFFF",
                elevation=3,
                shape=ft.RoundedRectangleBorder(radius=12),
                padding=ft.Padding(20, 15, 20, 15),
                text_style=ft.TextStyle(size=16, weight=ft.FontWeight.W_600),
            ),
            expand=True,
            visible=False,
        )

        return ft.Container(
            content=ft.Row(
                controls=[
                    self.btn_guardar,
                    self.btn_actualizar,
                    self.btn_cancelar_edicion,
                ],
                spacing=15,
            ),
            padding=ft.Padding(20, 15, 20, 20),
            bgcolor="#FFFFFF",
            border_radius=16,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color="#0000001A",
                offset=ft.Offset(0, 2),
            ),
        )

    def _crear_botones_accion_compactos(self):
        """Crea los botones de acción compactos para layout de dos columnas con colores dinámicos."""
        colors = get_theme_colors()
        
        self.btn_guardar = ft.ElevatedButton(
            text="💾 GUARDAR AUDIENCIA",
            on_click=self._on_guardar,
            style=get_button_style_primary(),
            expand=True,
        )

        self.btn_actualizar = ft.ElevatedButton(
            text="✏️ ACTUALIZAR REGISTRO",
            on_click=self._on_actualizar,
            style=ft.ButtonStyle(
                bgcolor=colors["success"],
                color=colors["text_on_primary"],
                elevation=2,
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=ft.Padding(16, 12, 16, 12),
                text_style=ft.TextStyle(size=14, weight=ft.FontWeight.W_600),
            ),
            expand=True,
            visible=False,
        )

        self.btn_cancelar_edicion = ft.ElevatedButton(
            text="❌ CANCELAR EDICIÓN",
            on_click=self._on_cancelar_edicion,
            style=get_button_style_danger(),
            expand=True,
            visible=False,
        )

        return ft.Container(
            content=ft.Row(
                controls=[
                    self.btn_guardar,
                    self.btn_actualizar,
                    self.btn_cancelar_edicion,
                ],
                spacing=10,  # Espaciado reducido
            ),
            padding=ft.Padding(15, 10, 15, 15),  # Padding reducido
            bgcolor=colors["surface_card"],
            border_radius=12,
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=4,
                color="#00000015" if not is_dark_theme() else "#00000030",
                offset=ft.Offset(0, 1),
            ),
            expand=1,
        )

    def _crear_gestion_archivos(self):
        """Crea la sección de gestión de archivos con diseño profesional y colores dinámicos."""
        colors = get_theme_colors()
        
        # Estilos para botones con colores dinámicos
        estilo_boton_primario = ft.ButtonStyle(
            bgcolor=colors["primary"],
            color=colors["text_on_primary"],
            elevation=2,
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.Padding(16, 12, 16, 12),
            text_style=ft.TextStyle(size=14, weight=ft.FontWeight.W_500),
        )
        
        estilo_boton_secundario = ft.ButtonStyle(
            bgcolor=colors["text_secondary"],
            color=colors["text_on_primary"],
            elevation=2,
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.Padding(16, 12, 16, 12),
            text_style=ft.TextStyle(size=14, weight=ft.FontWeight.W_500),
        )
        
        estilo_boton_peligro = ft.ButtonStyle(
            bgcolor=colors["error"],
            color=colors["text_on_primary"],
            elevation=2,
            shape=ft.RoundedRectangleBorder(radius=10),
            padding=ft.Padding(16, 12, 16, 12),
            text_style=ft.TextStyle(size=14, weight=ft.FontWeight.W_500),
        )

        # Primera fila de botones
        fila1 = ft.Row(
            controls=[
                ft.ElevatedButton(
                    text="📄 Crear",
                    on_click=self._on_crear_archivo,
                    style=estilo_boton_primario,
                    expand=True,
                ),
                ft.ElevatedButton(
                    text="📂 Seleccionar",
                    on_click=self._on_seleccionar_archivo,
                    style=estilo_boton_secundario,
                    expand=True,
                ),
            ],
            spacing=12,
        )
        
        # Segunda fila de botones
        fila2 = ft.Row(
            controls=[
                ft.ElevatedButton(
                    text="✏️ Editar",
                    on_click=self._on_editar_registro,
                    style=estilo_boton_secundario,
                    expand=True,
                ),
                ft.ElevatedButton(
                    text="🗑️ Eliminar",
                    on_click=self._on_eliminar_archivo,
                    style=estilo_boton_peligro,
                    expand=True,
                ),
                ft.ElevatedButton(
                    text="💾 Descargar",
                    on_click=self._on_descargar_archivo,
                    style=estilo_boton_primario,
                    expand=True,
                ),
            ],
            spacing=12,
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.FOLDER_OPEN, size=24, color=colors["primary"]),
                            ft.Text(
                                "GESTIÓN DE ARCHIVOS",
                                size=18,
                                weight=ft.FontWeight.W_700,
                                color=colors["text_primary"],
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.Container(height=15),  # Espaciado
                    fila1,
                    fila2,
                ],
                spacing=12,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=colors["surface_card"],
            border_radius=16,
            padding=ft.Padding(20, 20, 20, 20),
            shadow=ft.BoxShadow(
                spread_radius=0,
                blur_radius=8,
                color="#00000015" if not is_dark_theme() else "#00000030",
                offset=ft.Offset(0, 2),
            ),
        )

    # === EVENTOS ===

    def _abrir_date_picker(self, e):
        """Abre el DatePicker para seleccionar fecha."""
        self.date_picker.open = True
        self.page.update()

    def _on_date_picker_change(self, e):
        """Maneja el cambio de fecha en el DatePicker."""
        if e.control.value:
            fecha_seleccionada = e.control.value
            fecha_formateada = fecha_seleccionada.strftime("%d/%m/%Y")
            self.entrada_fecha.value = fecha_formateada
            self._actualizar_campos_compatibilidad(fecha_seleccionada)
            self.page.update()

    def _on_fecha_change_tiempo_real(self, e):
        """Maneja el formateo en tiempo real de la fecha mientras se escribe."""
        valor = e.control.value
        if not valor:
            return
            
        # Remover caracteres no numéricos excepto /
        valor_limpio = ''.join(c for c in valor if c.isdigit())
        
        # Inicializar fecha_formateada
        fecha_formateada = valor
        
        # Formatear automáticamente mientras se escribe
        if len(valor_limpio) <= 8:
            if len(valor_limpio) <= 2:
                # Solo día: 2 → 2, 22 → 22
                fecha_formateada = valor_limpio
            elif len(valor_limpio) <= 4:
                # Día + mes: 220 → 22/0, 2207 → 22/07
                dia = valor_limpio[:2]
                mes = valor_limpio[2:]
                fecha_formateada = f"{dia}/{mes}"
            elif len(valor_limpio) <= 8:
                # Día + mes + año: 22072 → 22/07/2, 22072025 → 22/07/2025
                dia = valor_limpio[:2]
                mes = valor_limpio[2:4]
                anio = valor_limpio[4:]
                fecha_formateada = f"{dia}/{mes}/{anio}"
            
            # Actualizar el campo si el formato cambió
            if fecha_formateada != valor:
                # Recordar la posición del cursor
                cursor_pos = len(fecha_formateada)
                e.control.value = fecha_formateada
                # Establecer el cursor al final
                e.control.selection = ft.TextSelection(cursor_pos, cursor_pos)
                e.control.update()
            
            # Si tenemos una fecha completa (8 dígitos), validar y sincronizar
            if len(valor_limpio) == 8:
                try:
                    fecha_obj = datetime.strptime(fecha_formateada, "%d/%m/%Y")
                    self._actualizar_campos_compatibilidad(fecha_obj)
                    # Sincronizar con DatePicker
                    self.date_picker.value = fecha_obj.date()
                except ValueError:
                    # Fecha inválida, limpiar campos de compatibilidad
                    self._limpiar_campos_compatibilidad()

    def _on_fecha_change(self, e):
        """Maneja cambios en el campo de fecha con formateo automático."""
        self._on_fecha_change_tiempo_real(e)

    def _actualizar_campos_compatibilidad(self, fecha_obj):
        """Actualiza los campos virtuales para mantener compatibilidad."""
        self.combo_dia.value = f"{fecha_obj.day:02d}"
        self.combo_mes.value = f"{fecha_obj.month:02d}"
        self.combo_anio.value = str(fecha_obj.year)

    def _limpiar_campos_compatibilidad(self):
        """Limpia los campos virtuales de compatibilidad."""
        self.combo_dia.value = None
        self.combo_mes.value = None
        self.combo_anio.value = None

    def _on_tipo_change(self, e):
        """Maneja el cambio en el tipo de audiencia."""
        self.entrada_tipo_otra.visible = e.control.value == "Otra"
        self.page.update()

    def _on_realizada_change(self, e):
        """Maneja el cambio en ¿Se realizó?"""
        habilitar = e.control.value == "NO"
        for checkbox in self.checkboxes_motivos:
            checkbox.disabled = not habilitar
            if not habilitar:
                checkbox.value = False
        self.page.update()

    def _on_guardar(self, e):
        """Guarda los datos."""
        self.guardar_datos()

    def _on_actualizar(self, e):
        """Actualiza el registro."""
        self.actualizar_registro()

    def _on_cancelar_edicion(self, e):
        """Cancela la edición."""
        self.cancelar_edicion()

    def _on_crear_archivo(self, e):
        """Crea un nuevo archivo."""
        self.crear_nueva_copia()

    def _on_seleccionar_archivo(self, e):
        """Selecciona un archivo."""
        self.seleccionar_archivo_trabajo()

    def _on_editar_registro(self, e):
        """Edita un registro."""
        self.seleccionar_registro_para_editar()

    def _on_eliminar_archivo(self, e):
        """Elimina un archivo."""
        self.eliminar_archivo_trabajo()

    def _on_descargar_archivo(self, e):
        """Descarga un archivo."""
        self.descargar_archivo_trabajo()

    # === MÉTODOS DE LÓGICA DE NEGOCIO ===

    def _inicializar(self):
        """Inicializa valores por defecto."""
        self.limpiar_campos()
        self.actualizar_contador_registros()

        # Establecer fecha actual en el nuevo campo
        hoy = datetime.now()
        fecha_actual = f"{hoy.day:02d}/{hoy.month:02d}/{hoy.year}"
        if hasattr(self, 'entrada_fecha') and self.entrada_fecha:
            self.entrada_fecha.value = fecha_actual
            self._actualizar_campos_compatibilidad(hoy)

        # Establecer hora por defecto
        if self.entrada_hora:
            self.entrada_hora.value = "00"
        if self.entrada_minuto:
            self.entrada_minuto.value = "00"

        self.page.update()

    def limpiar_campos(self):
        """Limpia todos los campos."""
        if self.entrada_radicado:
            self.entrada_radicado.value = ""
        if self.combo_tipo:
            self.combo_tipo.value = None
        if self.entrada_tipo_otra:
            self.entrada_tipo_otra.value = ""
            self.entrada_tipo_otra.visible = False
        # Limpiar nuevo campo de fecha
        if hasattr(self, 'entrada_fecha') and self.entrada_fecha:
            self.entrada_fecha.value = ""
        # Limpiar campos de compatibilidad
        if hasattr(self, 'combo_dia'):
            self.combo_dia.value = None
        if hasattr(self, 'combo_mes'):
            self.combo_mes.value = None
        if hasattr(self, 'combo_anio'):
            self.combo_anio.value = None
        if self.entrada_hora:
            self.entrada_hora.value = ""
        if self.entrada_minuto:
            self.entrada_minuto.value = ""
        if self.entrada_juzgado:
            self.entrada_juzgado.value = ""
        if self.combo_realizada:
            self.combo_realizada.value = None
        for checkbox in self.checkboxes_motivos:
            checkbox.value = False
            checkbox.disabled = True
        if self.entrada_observaciones:
            self.entrada_observaciones.value = ""

    def obtener_datos_formulario(self):
        """Obtiene los datos del formulario."""
        tipo_audiencia = self.combo_tipo.value
        if tipo_audiencia == "Otra":
            tipo_audiencia = self.entrada_tipo_otra.value or ""

        # Usar el nuevo campo de fecha
        fecha = self.entrada_fecha.value or f"01/01/{datetime.now().year}"

        hora_val = self.entrada_hora.value or "00"
        minuto_val = self.entrada_minuto.value or "00"
        hora = f"{hora_val.zfill(2)}:{minuto_val.zfill(2)}"

        motivos = [
            checkbox.label if checkbox.value else ""
            for checkbox in self.checkboxes_motivos
        ]

        return {
            "radicado": self.entrada_radicado.value or "",
            "tipo": tipo_audiencia or "",
            "fecha": fecha,
            "hora": hora,
            "juzgado": self.entrada_juzgado.value or "",
            "realizada_si": "SI" if self.combo_realizada.value == "SI" else "",
            "realizada_no": "NO" if self.combo_realizada.value == "NO" else "",
            "motivos": motivos,
            "observaciones": self.entrada_observaciones.value or "",
        }

    def guardar_datos(self):
        """Guarda los datos."""
        print("=== DEBUG: Iniciando guardar_datos ===")
        
        if not self.archivo_excel or not self.excel_manager:
            print("ERROR: No hay archivo seleccionado")
            self._mostrar_mensaje("Primero debe seleccionar un archivo")
            return

        print(f"Archivo seleccionado: {self.archivo_excel}")

        # AGREGAR LA LÓGICA FALTANTE:
        datos = self.obtener_datos_formulario()
        print(f"Datos obtenidos del formulario: {datos}")
        
        valido, mensaje = validar_todos_los_datos(datos)
        print(f"Validación: válido={valido}, mensaje='{mensaje}'")

        if not valido:
            self._mostrar_mensaje(f"Error: {mensaje}")
            return

        try:
            print("Creando objeto Audiencia...")
            audiencia = Audiencia.from_form_data(datos)
            print(f"Audiencia creada: {audiencia}")
            
            print("Guardando en Excel...")
            self.excel_manager.guardar_audiencia(audiencia)
            print("Guardado exitoso. Reordenando...")
            
            self.excel_manager.reordenar_y_guardar()
            print("Reordenamiento exitoso.")

            self._mostrar_mensaje("Registro guardado correctamente")
            self.limpiar_campos()
            self._inicializar()
            self.actualizar_contador_registros()
            print("=== DEBUG: guardar_datos completado exitosamente ===")

        except Exception as e:
            print(f"ERROR en guardar_datos: {e}")
            traceback.print_exc()
            self._mostrar_mensaje(f"Error al guardar: {e}")

    def actualizar_registro(self):
        """Actualiza un registro existente."""
        if not self.fila_editando:
            return

        if not self.archivo_excel or not self.excel_manager:
            self._mostrar_mensaje("No hay archivo seleccionado")
            return

        datos = self.obtener_datos_formulario()
        valido, mensaje = validar_todos_los_datos(datos)

        if not valido:
            self._mostrar_mensaje(f"Error: {mensaje}")
            return

        try:
            audiencia = Audiencia.from_form_data(datos)
            self.excel_manager.actualizar_audiencia(self.fila_editando, audiencia)
            self.excel_manager.reordenar_y_guardar()

            self._mostrar_mensaje("Registro actualizado correctamente")
            self.desactivar_modo_edicion()
            self.actualizar_contador_registros()

        except Exception as e:
            self._mostrar_mensaje(f"Error al actualizar: {e}")

    def cancelar_edicion(self):
        """Cancela la edición."""
        self.desactivar_modo_edicion()

    def activar_modo_edicion(self):
        """Activa el modo edición."""
        self.modo_edicion = True
        self.btn_guardar.visible = False
        self.btn_actualizar.visible = True
        self.btn_cancelar_edicion.visible = True
        self.page.title = "Gestor de Audiencias - EDITANDO"
        self.page.update()

    def desactivar_modo_edicion(self):
        """Desactiva el modo edición."""
        self.modo_edicion = False
        self.fila_editando = None
        self.btn_guardar.visible = True
        self.btn_actualizar.visible = False
        self.btn_cancelar_edicion.visible = False
        self.page.title = "Gestor de Audiencias Judiciales"
        self.limpiar_campos()
        self._inicializar()

    def crear_nueva_copia(self):
        """Crea una nueva copia."""
        print("=== DEBUG: Iniciando crear_nueva_copia ===")
        
        def callback_crear(nombre):
            print(f"Callback crear ejecutado con nombre: '{nombre}'")
            try:
                # Asegurar que tenga la extensión .xlsx
                if not nombre.lower().endswith('.xlsx'):
                    nombre_con_extension = f"{nombre}.xlsx"
                else:
                    nombre_con_extension = nombre
                
                print(f"Nombre final con extensión: '{nombre_con_extension}'")
                print("Llamando a crear_copia_plantilla...")
                resultado = crear_copia_plantilla(nombre_con_extension)
                print(f"Archivo creado exitosamente en: {resultado}")
                self._mostrar_mensaje(f"Archivo '{nombre_con_extension}' creado correctamente.")
            except FileExistsError:
                print(f"ERROR: Archivo ya existe: {nombre}")
                self._mostrar_mensaje("Ya existe un archivo con ese nombre.")
            except Exception as e:
                print(f"ERROR en crear_copia_plantilla: {e}")
                import traceback
                traceback.print_exc()
                self._mostrar_mensaje(f"No se pudo crear el archivo: {e}")

        print("Abriendo diálogo para crear archivo...")
        DialogoCrearArchivo(self.page, callback_crear)

    def seleccionar_archivo_trabajo(self):
        """Selecciona archivo de trabajo."""
        print("=== DEBUG: Iniciando seleccionar_archivo_trabajo ===")
        
        archivos = listar_archivos_creados()
        print(f"Archivos encontrados: {archivos}")
        
        if not archivos:
            print("ERROR: No hay archivos de plantilla creados.")
            self._mostrar_mensaje("No hay archivos de plantilla creados.")
            return

        def callback_seleccionar(nombre_archivo):
            print(f"Callback seleccionar ejecutado con archivo: '{nombre_archivo}'")
            try:
                self.archivo_excel = seleccionar_archivo(nombre_archivo)
                self.excel_manager = ExcelManager(self.archivo_excel)
                self.archivo_actual_text.value = nombre_archivo
                self._mostrar_mensaje(f"Archivo seleccionado: {nombre_archivo}")
                self.actualizar_contador_registros()
                self.page.update()
            except Exception as e:
                self._mostrar_mensaje(f"Error al seleccionar archivo: {e}")

        print("Abriendo ventana de selección...")
        VentanaSeleccionArchivo(
            self.page,
            "Seleccionar Archivo de Trabajo",
            archivos,
            callback_seleccionar,
        )

    def seleccionar_registro_para_editar(self):
        """Selecciona registro para editar."""
        if not self.archivo_excel or not self.excel_manager:
            self._mostrar_mensaje("Primero debe seleccionar un archivo")
            return

        try:
            registros = self.excel_manager.leer_registros()

            if not registros:
                self._mostrar_mensaje("No hay registros para editar en el archivo.")
                return

            def callback_editar(fila_num, datos_completos):
                self.fila_editando = fila_num
                self.cargar_datos_para_edicion(datos_completos)
                self.activar_modo_edicion()

            VentanaSeleccionRegistro(self.page, registros, callback_editar)

        except Exception as e:
            self._mostrar_mensaje(f"Error al leer los registros: {e}")

    def cargar_datos_para_edicion(self, fila_datos):
        """Carga los datos de una fila en el formulario para editarlos."""
        self.limpiar_campos()

        # Cargar datos básicos
        if len(fila_datos) > 1 and fila_datos[1]:
            self.entrada_radicado.value = str(fila_datos[1])

        # Tipo de audiencia
        if len(fila_datos) > 2 and fila_datos[2]:
            tipo = str(fila_datos[2])
            if tipo in self.tipos_audiencia:
                self.combo_tipo.value = tipo
            else:
                self.combo_tipo.value = "Otra"
                self.entrada_tipo_otra.value = tipo
                self.entrada_tipo_otra.visible = True

        # Fecha - usar el nuevo campo
        if len(fila_datos) > 3 and fila_datos[3] and "/" in str(fila_datos[3]):
            fecha_str = str(fila_datos[3])
            self.entrada_fecha.value = fecha_str
            try:
                fecha_obj = datetime.strptime(fecha_str, "%d/%m/%Y")
                self._actualizar_campos_compatibilidad(fecha_obj)
            except ValueError:
                pass

        # Hora
        if len(fila_datos) > 4 and fila_datos[4] and ":" in str(fila_datos[4]):
            try:
                hora, minuto = str(fila_datos[4]).split(":")
                self.entrada_hora.value = hora.zfill(2)
                self.entrada_minuto.value = minuto.zfill(2)
            except ValueError:
                pass

        # Juzgado
        if len(fila_datos) > 5 and fila_datos[5]:
            self.entrada_juzgado.value = str(fila_datos[5])

        # Se realizó
        if len(fila_datos) > 6 and fila_datos[6] == "SI":
            self.combo_realizada.value = "SI"
        elif len(fila_datos) > 7 and fila_datos[7] == "NO":
            self.combo_realizada.value = "NO"

        # Motivos
        for i, checkbox in enumerate(self.checkboxes_motivos):
            if len(fila_datos) > i + 8 and fila_datos[i + 8]:
                checkbox.value = True
                checkbox.disabled = False

        # Observaciones
        if len(fila_datos) > 16 and fila_datos[16]:
            self.entrada_observaciones.value = str(fila_datos[16])

        self.page.update()

    def eliminar_archivo_trabajo(self):
        """Elimina archivo de trabajo."""
        archivos = listar_archivos_creados()
        if not archivos:
            self._mostrar_mensaje("No hay archivos para eliminar.")
            return

        def callback_seleccionar(nombre_archivo):
            DialogoConfirmacion.confirmar(
                self.page,
                "Confirmar eliminación",
                f"¿Seguro que quiere eliminar '{nombre_archivo}'?",
                lambda: self._ejecutar_eliminacion(nombre_archivo),
            )

        VentanaSeleccionArchivo(
            self.page, "Eliminar Archivo", archivos, callback_seleccionar
        )

    def _ejecutar_eliminacion(self, nombre_archivo):
        """Ejecuta la eliminación del archivo."""
        try:
            eliminar_archivo(nombre_archivo)
            self._mostrar_mensaje(f"Archivo '{nombre_archivo}' eliminado.")

            # Si era el archivo actual, limpiar la selección
            if self.archivo_excel and self.archivo_excel.endswith(nombre_archivo):
                self.archivo_excel = None
                self.excel_manager = None
                self.archivo_actual_text.value = "Ningún archivo seleccionado"
                self.actualizar_contador_registros()

        except Exception as e:
            self._mostrar_mensaje(f"No se pudo eliminar el archivo: {e}")

    def descargar_archivo_trabajo(self):
        """Descarga archivo de trabajo."""
        archivos = listar_archivos_creados()
        if not archivos:
            self._mostrar_mensaje("No hay archivos para descargar.")
            return

        def callback_seleccionar(nombre_archivo):
            try:
                destino = descargar_archivo(nombre_archivo)
                if destino:
                    self._mostrar_mensaje(f"Archivo guardado en: {destino}")
            except Exception as e:
                self._mostrar_mensaje(f"No se pudo descargar el archivo: {e}")

        VentanaSeleccionArchivo(
            self.page, "Descargar Archivo", archivos, callback_seleccionar
        )

    def actualizar_contador_registros(self):
        """Actualiza el contador de registros."""
        if not self.excel_manager:
            self.contador_registros.value = "Registros: 0"
        else:
            try:
                num_registros = self.excel_manager.contar_registros()
                self.contador_registros.value = f"Registros: {num_registros}"
            except Exception:
                self.contador_registros.value = "Registros: ?"

        self.page.update()

    def _mostrar_mensaje(self, mensaje: str):
        """Muestra un mensaje usando AlertDialog."""
        print(f"=== DEBUG: Mostrando mensaje: '{mensaje}' ===")
        
        def cerrar_mensaje(e):
            dlg.open = False
            self.page.update()
        
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Información", size=18, weight=ft.FontWeight.BOLD),
            content=ft.Text(mensaje, size=14, color="#374151"),
            actions=[
                ft.ElevatedButton(
                    "OK",
                    on_click=cerrar_mensaje,
                    style=ft.ButtonStyle(
                        bgcolor="#1E40AF",
                        color="#FFFFFF",
                        elevation=2,
                        shape=ft.RoundedRectangleBorder(radius=8),
                        padding=ft.Padding(20, 10, 20, 10),
                    ),
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.overlay.append(dlg)
        dlg.open = True
        self.page.update()
        print("=== DEBUG: Mensaje mostrado ===")
    
    def _cerrar_dialogo(self, dlg):
        """Cierra un diálogo."""
        dlg.open = False
        self.page.update()


def crear_app(page: ft.Page):
    """Función principal para crear la app de Flet."""
    app = VentanaPrincipal(page)


def ejecutar_app():
    """Ejecuta la aplicación Flet."""
    try:
        ft.app(target=crear_app)
    except Exception as e:
        print("Abriendo en modo web...")
        ft.app(target=crear_app, view=ft.AppView.WEB_BROWSER, port=8080)
