import flet as ft
from typing import List, Tuple, Optional, Callable


class DialogoCrearArchivo:
    """Diálogo para crear un nuevo archivo."""
    
    def __init__(self, page: ft.Page, callback: Callable[[str], None]):
        self.page = page
        self.callback = callback
        self.dialog = None
        self._crear_dialogo()
    
    def _crear_dialogo(self):
        """Crea el diálogo para crear archivo."""
        # Campo de entrada para el nombre
        self.campo_nombre = ft.TextField(
            label="Nombre del archivo",
            hint_text="Ej: audiencias_enero",
            width=300,
            border_radius=10,
            filled=True,
            bgcolor="#FFFFFF",
            border_color="#E5E7EB",
            focused_border_color="#1E40AF",
            text_style=ft.TextStyle(size=14, color="#1F2937"),
            label_style=ft.TextStyle(size=13, color="#6B7280"),
            content_padding=ft.Padding(12, 10, 12, 10),
            autofocus=True,
        )
        
        # Botones
        btn_crear = ft.ElevatedButton(
            text="Crear",
            on_click=self._on_crear,
            style=ft.ButtonStyle(
                bgcolor="#1E40AF",
                color="#FFFFFF",
                elevation=2,
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.Padding(20, 10, 20, 10),
            ),
        )
        
        btn_cancelar = ft.TextButton(
            text="Cancelar",
            on_click=self._on_cancelar,
            style=ft.ButtonStyle(
                color="#6B7280",
                padding=ft.Padding(20, 10, 20, 10),
            ),
        )
        
        # Contenido del diálogo
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Crear Nuevo Archivo", size=18, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Ingrese el nombre para el nuevo archivo:",
                            size=14,
                            color="#6B7280",
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
    """Diálogo para seleccionar un archivo de una lista."""
    
    def __init__(self, page: ft.Page, titulo: str, archivos: List[str], callback: Callable[[str], None]):
        self.page = page
        self.titulo = titulo
        self.archivos = archivos
        self.callback = callback
        self.dialog = None
        self._crear_dialogo()
    
    def _crear_dialogo(self):
        """Crea el diálogo de selección."""
        # Lista de archivos como botones
        lista_controles = []
        
        for archivo in self.archivos:
            btn_archivo = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.DESCRIPTION, size=20, color="#1E40AF"),
                        ft.Text(archivo, size=14, color="#1F2937", expand=True),
                        ft.Icon(ft.Icons.ARROW_FORWARD_IOS, size=16, color="#9CA3AF"),
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.START,
                ),
                bgcolor="#F9FAFB",
                border=ft.border.all(1, "#E5E7EB"),
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
            height=min(300, len(self.archivos) * 60 + 50),  # Altura dinámica
            width=400,
        )
        
        # Diálogo principal
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(self.titulo, size=18, weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            f"Seleccione uno de los {len(self.archivos)} archivos disponibles:",
                            size=14,
                            color="#6B7280",
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
    """Ventana para seleccionar un registro para editar."""

    def __init__(
        self,
        page: ft.Page,
        registros: List[Tuple[int, List]],
        callback: Callable[[int, List], None],
    ):
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
