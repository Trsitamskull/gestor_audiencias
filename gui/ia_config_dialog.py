"""
Diálogo de configuración de IA integrado en la aplicación.
Permite configurar OpenAI directamente desde la interfaz.
"""

import flet as ft
import os
from typing import Optional, Callable
from gui.constants import get_theme_colors


class DialogoConfiguracionIA:
    """Diálogo para configurar OpenAI directamente desde la aplicación."""
    
    def __init__(self, page: ft.Page, callback: Optional[Callable] = None):
        self.page = page
        self.callback = callback
        self.dialog = None
        self.campo_api_key = None
        self._crear_dialogo()
    
    def _crear_dialogo(self):
        """Crea el diálogo de configuración con diseño atractivo."""
        colors = get_theme_colors()
        
        # Campo para API Key
        self.campo_api_key = ft.TextField(
            label="API Key de OpenAI",
            hint_text="sk-...",
            width=400,
            password=True,
            can_reveal_password=True,
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
        btn_guardar = ft.ElevatedButton(
            text="Guardar y Activar IA",
            icon=ft.icons.SMART_TOY,
            on_click=self._on_guardar,
            style=ft.ButtonStyle(
                bgcolor=colors["success"],
                color="#FFFFFF",
                elevation=2,
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.Padding(20, 12, 20, 12),
            ),
        )
        
        btn_mas_tarde = ft.TextButton(
            text="Configurar después",
            on_click=self._on_cancelar,
            style=ft.ButtonStyle(
                color=colors["text_secondary"],
                padding=ft.Padding(20, 10, 20, 10),
            ),
        )
        
        btn_obtener_key = ft.TextButton(
            text="¿Cómo obtener API Key?",
            icon=ft.icons.HELP_OUTLINE,
            on_click=self._mostrar_ayuda,
            style=ft.ButtonStyle(
                color=colors["primary"],
                padding=ft.Padding(10, 5, 10, 5),
            ),
        )
        
        # Estado actual
        estado_actual = self._obtener_estado_ia()
        
        # Contenido del diálogo
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                controls=[
                    ft.Icon(ft.icons.SMART_TOY, color=colors["primary"], size=24),
                    ft.Text(
                        "Configuración de Inteligencia Artificial", 
                        size=18, 
                        weight=ft.FontWeight.BOLD, 
                        color=colors["text_primary"]
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        # Estado actual
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.icons.CIRCLE,
                                        color=colors["success"] if estado_actual["configurado"] else colors["warning"],
                                        size=12,
                                    ),
                                    ft.Text(
                                        estado_actual["mensaje"],
                                        size=13,
                                        color=colors["text_secondary"],
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            bgcolor=colors["surface_secondary"],
                            padding=ft.Padding(12, 8, 12, 8),
                            border_radius=8,
                            margin=ft.Margin(0, 0, 0, 16),
                        ),
                        
                        # Explicación
                        ft.Text(
                            "🤖 La IA puede analizar textos y completar automáticamente los formularios",
                            size=14,
                            color=colors["text_primary"],
                            weight=ft.FontWeight.W_500,
                        ),
                        
                        ft.Text(
                            "• Extrae información de documentos judiciales\n"
                            "• Identifica automáticamente datos relevantes\n"
                            "• Acelera significativamente el proceso",
                            size=13,
                            color=colors["text_secondary"],
                        ),
                        
                        ft.Container(height=16),
                        
                        # Campo API Key
                        ft.Text(
                            "Ingrese su API Key de OpenAI:",
                            size=14,
                            color=colors["text_primary"],
                            weight=ft.FontWeight.W_500,
                        ),
                        
                        self.campo_api_key,
                        
                        # Ayuda
                        ft.Container(
                            content=btn_obtener_key,
                            alignment=ft.alignment.center_left,
                            margin=ft.Margin(0, 8, 0, 0),
                        ),
                        
                        ft.Container(height=8),
                        
                        # Nota de seguridad
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.icons.SECURITY, color=colors["text_secondary"], size=16),
                                    ft.Text(
                                        "Tu API Key se guarda localmente y de forma segura",
                                        size=12,
                                        color=colors["text_secondary"],
                                        italic=True,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.START,
                            ),
                            margin=ft.Margin(0, 8, 0, 0),
                        ),
                    ],
                    tight=True,
                    spacing=8,
                ),
                width=450,
                padding=ft.Padding(8, 0, 8, 0),
            ),
            actions=[
                ft.Row(
                    controls=[
                        btn_mas_tarde,
                        btn_guardar,
                    ],
                    alignment=ft.MainAxisAlignment.END,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
    
    def _obtener_estado_ia(self) -> dict:
        """Obtiene el estado actual de configuración de IA."""
        try:
            # Verificar si existe el archivo de configuración
            config_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.py")
            
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                    
                if 'OPENAI_API_KEY = ""' in contenido:
                    return {
                        "configurado": False,
                        "mensaje": "IA no configurada - Sin API Key"
                    }
                elif 'OPENAI_API_KEY = "sk-' in contenido:
                    return {
                        "configurado": True,
                        "mensaje": "IA configurada y lista para usar"
                    }
                else:
                    return {
                        "configurado": False,
                        "mensaje": "Configuración incompleta"
                    }
            else:
                return {
                    "configurado": False,
                    "mensaje": "Archivo de configuración no encontrado"
                }
        except Exception:
            return {
                "configurado": False,
                "mensaje": "Error al verificar configuración"
            }
    
    def _mostrar_ayuda(self, e):
        """Muestra diálogo de ayuda para obtener API Key."""
        colors = get_theme_colors()
        
        ayuda_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("¿Cómo obtener tu API Key de OpenAI?", weight=ft.FontWeight.BOLD),
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Sigue estos pasos:", weight=ft.FontWeight.W_500),
                        
                        ft.Text("1. Ve a: https://platform.openai.com/api-keys"),
                        ft.Text("2. Inicia sesión en tu cuenta de OpenAI"),
                        ft.Text("3. Haz clic en 'Create new secret key'"),
                        ft.Text("4. Copia la clave que empieza con 'sk-'"),
                        ft.Text("5. Pégala en el campo de arriba"),
                        
                        ft.Container(height=16),
                        
                        ft.Container(
                            content=ft.Text(
                                "💡 Nota: Necesitas una cuenta de OpenAI con créditos disponibles",
                                size=12,
                                color=colors["text_secondary"],
                                italic=True,
                            ),
                            bgcolor=colors["surface_secondary"],
                            padding=ft.Padding(12, 8, 12, 8),
                            border_radius=8,
                        ),
                    ],
                    tight=True,
                    spacing=8,
                ),
                width=400,
            ),
            actions=[
                ft.TextButton(
                    text="Entendido",
                    on_click=lambda e: self.page.close(ayuda_dialog),
                ),
            ],
        )
        
        self.page.open(ayuda_dialog)
    
    def _on_guardar(self, e):
        """Guarda la configuración de IA."""
        api_key = self.campo_api_key.value.strip()
        
        if not api_key:
            self._mostrar_error("Por favor, ingresa tu API Key")
            return
        
        if not api_key.startswith("sk-"):
            self._mostrar_error("La API Key debe empezar con 'sk-'")
            return
        
        try:
            # Guardar en el archivo de configuración
            config_path = os.path.join(os.path.dirname(__file__), "..", "config", "config.py")
            
            # Leer archivo actual
            with open(config_path, 'r', encoding='utf-8') as f:
                contenido = f.read()
            
            # Reemplazar la API Key
            nuevo_contenido = contenido.replace(
                'OPENAI_API_KEY = ""',
                f'OPENAI_API_KEY = "{api_key}"'
            )
            
            # Escribir archivo actualizado
            with open(config_path, 'w', encoding='utf-8') as f:
                f.write(nuevo_contenido)
            
            # Mostrar éxito
            self._mostrar_exito()
            
        except Exception as ex:
            self._mostrar_error(f"Error al guardar: {str(ex)}")
    
    def _mostrar_error(self, mensaje: str):
        """Muestra un mensaje de error."""
        colors = get_theme_colors()
        error_snack = ft.SnackBar(
            content=ft.Text(f"❌ {mensaje}", color="#FFFFFF"),
            bgcolor=colors["error"],
            duration=3000,
        )
        self.page.overlay.append(error_snack)
        error_snack.open = True
        self.page.update()
    
    def _mostrar_exito(self):
        """Muestra mensaje de éxito y cierra el diálogo."""
        colors = get_theme_colors()
        
        # SnackBar de éxito
        success_snack = ft.SnackBar(
            content=ft.Text("✅ IA configurada correctamente. ¡Ya puedes usarla!", color="#FFFFFF"),
            bgcolor=colors["success"],
            duration=4000,
        )
        self.page.overlay.append(success_snack)
        success_snack.open = True
        
        # Cerrar diálogo
        self._on_cancelar(None)
        
        # Callback si existe
        if self.callback:
            self.callback()
        
        self.page.update()
    
    def _on_cancelar(self, e):
        """Cancela y cierra el diálogo."""
        self.page.close(self.dialog)
    
    def mostrar(self):
        """Muestra el diálogo."""
        self.page.open(self.dialog)


def mostrar_dialogo_configuracion_ia(page: ft.Page, callback: Optional[Callable] = None):
    """Función helper para mostrar el diálogo de configuración de IA."""
    dialogo = DialogoConfiguracionIA(page, callback)
    dialogo.mostrar()
