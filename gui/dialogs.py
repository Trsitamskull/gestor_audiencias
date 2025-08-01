import flet as ft
from typing import List, Tuple, Optional, Callable
from gui.constants import get_theme_colors, is_dark_theme
import threading
import time

# Importar reconocimiento de voz
try:
    import speech_recognition as sr
    import pyaudio
    SPEECH_RECOGNITION_AVAILABLE = True
    PYAUDIO_AVAILABLE = True
except ImportError as e:
    SPEECH_RECOGNITION_AVAILABLE = False
    PYAUDIO_AVAILABLE = False
    print(f"⚠️ Advertencia: Reconocimiento de voz no disponible - {e}")

# Importar configuración de privacidad
try:
    from config.config import ANONYMIZE_DATA, USE_FREE_TIER, SHOW_PRIVACY_WARNING
except ImportError:
    ANONYMIZE_DATA = False
    USE_FREE_TIER = False
    SHOW_PRIVACY_WARNING = True


class DialogoAutocompletarIA:
    """Diálogo para autocompletar formulario usando IA con soporte para tema oscuro."""
    
    def __init__(self, page: ft.Page, callback: Callable[[dict], None]):
        self.page = page
        self.callback = callback
        self.dialog = None
        self.btn_procesar = None
        self.btn_cancelar = None
        self.btn_voz = None
        self.indicador_carga = None
        self.indicador_grabacion = None
        self.indicador_nivel_audio = None  # Nuevo: indicador de nivel de audio
        self.grabando = False
        self.pausa_detectada = False  # Nuevo: para detección de pausas
        self.tiempo_ultima_voz = 0  # Nuevo: timestamp de última detección de voz
        
        # Configuración optimizada de reconocimiento
        if SPEECH_RECOGNITION_AVAILABLE:
            self.recognizer = sr.Recognizer()
            # Configuración más conservadora y estable
            self.recognizer.energy_threshold = 300   # Menos sensible para evitar ruido
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 1.0    # Pausa más larga para mejor precisión
            self.recognizer.phrase_threshold = 0.3   # Mejor detección de inicio de frase
            self.recognizer.non_speaking_duration = 0.8  # Tiempo sin habla antes de procesar
        
        self._crear_dialogo()
    
    def _crear_dialogo(self):
        """Crea el diálogo para pegar texto y autocompletar con tema dinámico."""
        colors = get_theme_colors()
        
        # Campo de texto para pegar información con colores dinámicos
        self.campo_texto = ft.TextField(
            label="Pega aquí la información de la audiencia",
            hint_text="Ej: Audiencia de conciliación del proceso 11001-60-12345-2024-00567-00 programada para el 15 de agosto de 2025 a las 10:30 AM...",
            multiline=True,
            min_lines=4,
            max_lines=8,
            width=500,
            border_radius=10,
            filled=True,
            bgcolor=colors["surface_primary"],
            border_color=colors["surface_border"],
            focused_border_color=colors["primary"],
            text_style=ft.TextStyle(size=14, color=colors["text_primary"]),
            label_style=ft.TextStyle(size=13, color=colors["text_secondary"]),
            hint_style=ft.TextStyle(size=12, color=colors["text_secondary"]),
            content_padding=ft.Padding(12, 10, 12, 10),
            autofocus=True,
        )
        
        # Botón procesar
        self.btn_procesar = ft.ElevatedButton(
            text="🤖 Procesar con IA",
            on_click=self._on_procesar,
            style=ft.ButtonStyle(
                bgcolor=colors["success"],
                color=colors["text_on_primary"],
                elevation=2,
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.Padding(20, 10, 20, 10),
            ),
        )
        
        # Botón cancelar
        self.btn_cancelar = ft.TextButton(
            text="Cancelar",
            on_click=self._on_cancelar,
            style=ft.ButtonStyle(
                color=colors["text_secondary"],
                padding=ft.Padding(20, 10, 20, 10),
            ),
        )
        
        # Botón de reconocimiento de voz mejorado
        self.btn_voz = ft.Container(
            content=ft.Icon(
                ft.Icons.MIC if SPEECH_RECOGNITION_AVAILABLE else ft.Icons.MIC_OFF,
                color=colors["primary"] if SPEECH_RECOGNITION_AVAILABLE else colors["text_secondary"],
                size=24,
            ),
            tooltip="🎤 Dictado por voz (Ctrl+M)" if SPEECH_RECOGNITION_AVAILABLE else "Reconocimiento de voz no disponible",
            on_click=self._on_iniciar_grabacion if SPEECH_RECOGNITION_AVAILABLE else None,
            bgcolor=colors["surface_primary"],
            border=ft.border.all(2, colors["primary"] if SPEECH_RECOGNITION_AVAILABLE else colors["surface_border"]),
            border_radius=25,
            width=50,
            height=50,
            alignment=ft.alignment.center,
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            animate_scale=ft.Animation(100, ft.AnimationCurve.BOUNCE_OUT),
            disabled=not SPEECH_RECOGNITION_AVAILABLE,
        )
        
        # Indicador de grabación mejorado con animación
        self.indicador_grabacion = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        ft.Icons.MIC,
                        color=colors["error"],
                        size=20,
                    ),
                    ft.Text(
                        "🎤 Escuchando... (presiona para parar)",
                        size=12,
                        color=colors["error"],
                        weight=ft.FontWeight.W_500,
                    ),
                    # Indicador de nivel de audio (nuevo)
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Container(width=3, height=15, bgcolor=colors["error"], border_radius=1),
                                ft.Container(width=3, height=10, bgcolor=colors["error_light"], border_radius=1),
                                ft.Container(width=3, height=20, bgcolor=colors["error"], border_radius=1),
                                ft.Container(width=3, height=8, bgcolor=colors["error_light"], border_radius=1),
                                ft.Container(width=3, height=16, bgcolor=colors["error"], border_radius=1),
                            ],
                            spacing=2,
                        ),
                        animate=ft.Animation(1000, ft.AnimationCurve.EASE_IN_OUT),
                    ),
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            visible=False,
            padding=ft.Padding(10, 8, 10, 8),
            bgcolor=colors["error_light"],
            border_radius=12,
            border=ft.border.all(2, colors["error"]),
            animate_opacity=300,
        )
        
        # Indicador de carga (inicialmente oculto)
        self.indicador_carga = ft.Container(
            content=ft.Row(
                controls=[
                    ft.ProgressRing(
                        width=20,
                        height=20,
                        stroke_width=2,
                        color=colors["primary"],
                    ),
                    ft.Text(
                        "🤖 Procesando con IA...",
                        size=14,
                        color=colors["primary"],
                        weight=ft.FontWeight.W_500,
                    ),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            visible=False,
            padding=ft.Padding(0, 10, 0, 10),
        )
        
        # Contenido del diálogo con colores dinámicos y atajos de teclado
        self.dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text(
                "🤖 Autocompletar con IA", 
                size=18, 
                weight=ft.FontWeight.BOLD,
                color=colors["text_primary"]
            ),
            bgcolor=colors["surface_secondary"],
            content=ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Pega o escribe la información de la audiencia y la IA completará el formulario automáticamente:",
                            size=14,
                            color=colors["text_secondary"],
                        ),
                        # Información de atajos de teclado
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(ft.Icons.KEYBOARD, size=16, color=colors["text_secondary"]),
                                    ft.Text(
                                        "Atajos: Ctrl+M (Micrófono), Ctrl+Enter (Procesar), Esc (Cancelar)",
                                        size=11,
                                        color=colors["text_secondary"],
                                        italic=True,
                                    ),
                                ],
                                spacing=5,
                            ),
                            margin=ft.Margin(0, 5, 0, 10),
                        ),
                        ft.Container(height=5),
                        # Campo de texto con botón de voz
                        ft.Row(
                            controls=[
                                ft.Container(
                                    content=self.campo_texto,
                                    expand=True,
                                ),
                                self.btn_voz,
                            ],
                            spacing=10,
                            alignment=ft.MainAxisAlignment.START,
                        ),
                        # Indicador de grabación
                        self.indicador_grabacion,
                        ft.Container(height=10),
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.LIGHTBULB_OUTLINE, size=16, color=colors["warning"]),
                                ft.Text(
                                    "Tip: Incluye radicado, tipo de audiencia, fecha, hora y juzgado",
                                    size=12,
                                    color=colors["warning"],
                                    italic=True,
                                ),
                            ],
                            spacing=5,
                        ),
                        # Información mejorada sobre protección de datos si está activa
                        self._crear_info_proteccion_completa(colors) if ANONYMIZE_DATA else ft.Container(height=0),
                        self.indicador_carga,  # Añadir el indicador de carga
                    ],
                    tight=True,
                    spacing=5,
                ),
                width=580,  # Ancho aumentado para mostrar atajos
                height=320,  # Altura aumentada
            ),
            actions=[
                self.btn_cancelar,
                self.btn_procesar,
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=self._on_cancelar,  # Manejar Esc para cerrar
        )
        
        # Configurar eventos de teclado
        self.page.on_keyboard_event = self._on_keyboard_event
        
        # Mostrar el diálogo
        self.page.overlay.append(self.dialog)
        self.dialog.open = True
        self.page.update()
    
    def _on_keyboard_event(self, e):
        """Maneja los eventos de teclado para atajos."""
        if not self.dialog or not self.dialog.open:
            return
            
        # Ctrl+M para activar/desactivar micrófono
        if e.key == "M" and e.ctrl and SPEECH_RECOGNITION_AVAILABLE:
            self._on_iniciar_grabacion(None)
        
        # Ctrl+Enter para procesar
        elif e.key == "Enter" and e.ctrl:
            self._on_procesar(None)
        
        # Esc para cancelar
        elif e.key == "Escape":
            self._on_cancelar(None)
    
    def _mostrar_carga(self, mostrar: bool = True):
        """Muestra u oculta el indicador de carga."""
        if self.indicador_carga:
            self.indicador_carga.visible = mostrar
            
        if self.btn_procesar:
            self.btn_procesar.disabled = mostrar
            if mostrar:
                self.btn_procesar.text = "🔄 Procesando..."
            else:
                self.btn_procesar.text = "🤖 Procesar con IA"
                
        if self.btn_cancelar:
            self.btn_cancelar.disabled = mostrar
            
        self.page.update()
    
    def _on_procesar(self, e):
        """Procesa el texto con IA y devuelve los datos extraídos."""
        texto = self.campo_texto.value.strip() if self.campo_texto.value else ""
        
        if not texto:
            self.campo_texto.error_text = "Ingresa información para procesar"
            self.page.update()
            return
        
        # Limpiar errores previos
        self.campo_texto.error_text = None
        
        # Mostrar indicador de carga
        self._mostrar_carga(True)
        
        # Procesar con IA en hilo separado para no bloquear la UI
        def procesar_ia():
            try:
                from services.ai_service import ai_service
                datos_extraidos = ai_service.extract_audiencia_info(texto)
                
                # Ocultar indicador de carga
                self._mostrar_carga(False)
                
                # Cerrar diálogo y enviar datos
                self.dialog.open = False
                self.page.update()
                self.callback(datos_extraidos)
                
            except ImportError:
                # Ocultar indicador de carga
                self._mostrar_carga(False)
                # Mostrar error si no está el servicio
                self.campo_texto.error_text = "❌ Servicio de IA no disponible"
                self.page.update()
            except Exception as ex:
                # Ocultar indicador de carga
                self._mostrar_carga(False)
                # Mostrar error general
                self.campo_texto.error_text = f"❌ Error: {str(ex)}"
                self.page.update()
        
        # Ejecutar procesamiento
        import threading
        threading.Thread(target=procesar_ia, daemon=True).start()
    
    def _on_cancelar(self, e):
        """Cancela el procesamiento."""
        self.dialog.open = False
        self.page.update()
    
    def _on_iniciar_grabacion(self, e):
        """Inicia o detiene el reconocimiento de voz."""
        if not SPEECH_RECOGNITION_AVAILABLE:
            return
        
        if self.grabando:
            # Detener grabación
            self.grabando = False
            self._mostrar_grabacion(False)
        else:
            # Iniciar grabación
            self.grabando = True
            self._mostrar_grabacion(True)
            # Ejecutar reconocimiento en hilo separado
            threading.Thread(target=self._procesar_voz, daemon=True).start()
    
    def _mostrar_grabacion(self, mostrar: bool = True):
        """Muestra u oculta el indicador de grabación con mejores efectos visuales."""
        if not self.indicador_grabacion or not self.btn_voz:
            return
            
        colors = get_theme_colors()
        
        # Actualizar indicador de grabación
        self.indicador_grabacion.visible = mostrar
        
        # Recrear el icono del botón con el estado correcto
        if mostrar:
            # Estado de grabación activa
            self.btn_voz.content = ft.Icon(
                ft.Icons.STOP,
                color=colors["error"],
                size=24,
            )
            self.btn_voz.bgcolor = colors["error_light"]
            self.btn_voz.border = ft.border.all(2, colors["error"])
            self.btn_voz.tooltip = "🛑 Detener grabación"
            self.btn_voz.scale = 1.1  # Efecto de escala
        else:
            # Estado normal
            self.btn_voz.content = ft.Icon(
                ft.Icons.MIC if SPEECH_RECOGNITION_AVAILABLE else ft.Icons.MIC_OFF,
                color=colors["primary"] if SPEECH_RECOGNITION_AVAILABLE else colors["text_secondary"],
                size=24,
            )
            self.btn_voz.bgcolor = colors["surface_primary"]
            self.btn_voz.border = ft.border.all(2, colors["primary"] if SPEECH_RECOGNITION_AVAILABLE else colors["surface_border"])
            self.btn_voz.tooltip = "🎤 Dictado por voz (Ctrl+M)" if SPEECH_RECOGNITION_AVAILABLE else "Reconocimiento de voz no disponible"
            self.btn_voz.scale = 1.0
            
        self.page.update()
    
    def _procesar_voz(self):
        """Procesa el reconocimiento de voz con configuración optimizada para mejor precisión."""
        if not SPEECH_RECOGNITION_AVAILABLE:
            return
            
        try:
            with sr.Microphone() as source:
                # Calibración inicial más cuidadosa
                print("🎤 Calibrando micrófono...")
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
                print(f"🎤 Nivel de energía: {self.recognizer.energy_threshold}")
                
                # Variables para control de duplicados
                ultimo_texto = ""
                tiempo_ultimo_reconocimiento = 0
                contador_duplicados = 0
                
                print("🎤 ¡Listo! Habla claramente...")
                
                # Bucle de reconocimiento optimizado
                while self.grabando:
                    try:
                        # Escuchar con configuración optimizada
                        audio = self.recognizer.listen(
                            source, 
                            timeout=2,           # Timeout más largo para mejor calidad
                            phrase_time_limit=6  # Frases de duración media
                        )
                        
                        # Intentar reconocimiento con el mejor idioma
                        texto_reconocido = self._reconocer_con_mejor_precision(audio)
                        tiempo_actual = time.time()
                        
                        if texto_reconocido:
                            # Filtrar duplicados
                            if (texto_reconocido == ultimo_texto and 
                                tiempo_actual - tiempo_ultimo_reconocimiento < 3):
                                contador_duplicados += 1
                                if contador_duplicados < 2:  # Permitir máximo 1 duplicado
                                    print(f"🎤 Duplicado filtrado: {texto_reconocido}")
                                    continue
                            else:
                                contador_duplicados = 0
                            
                            print(f"🎤 ✅ Reconocido: {texto_reconocido}")
                            
                            # Agregar texto al campo
                            self._agregar_texto_inteligente(texto_reconocido)
                            
                            # Actualizar variables de control
                            ultimo_texto = texto_reconocido
                            tiempo_ultimo_reconocimiento = tiempo_actual
                            self.tiempo_ultima_voz = tiempo_actual
                        
                    except sr.WaitTimeoutError:
                        # Manejar timeout con indicador visual
                        print("🎤 Esperando voz...")
                        self._actualizar_indicador_esperando()
                        continue
                        
                    except sr.UnknownValueError:
                        print("🎤 No se pudo entender el audio, intenta hablar más claro")
                        continue
                        
                    except sr.RequestError as e:
                        print(f"❌ Error del servicio: {e}")
                        break
                        
        except Exception as e:
            print(f"❌ Error en reconocimiento de voz: {e}")
        finally:
            self.grabando = False
            self._mostrar_grabacion(False)
            print("🎤 Grabación terminada")
    
    def _reconocer_con_mejor_precision(self, audio) -> str:
        """Intenta reconocer con configuración optimizada para precisión."""
        # Orden de idiomas optimizado para Colombia
        configuraciones = [
            ('es-CO', 'Español Colombia'),
            ('es-ES', 'Español España'), 
            ('es-MX', 'Español México'),
            ('es-AR', 'Español Argentina'),
            ('en-US', 'Inglés')
        ]
        
        for idioma, nombre in configuraciones:
            try:
                resultado = self.recognizer.recognize_google(
                    audio, 
                    language=idioma,
                    show_all=False  # Solo el mejor resultado
                )
                if resultado and len(resultado.strip()) > 2:  # Filtrar resultados muy cortos
                    print(f"🎤 Reconocido en {nombre}: {resultado}")
                    return resultado.strip()
            except sr.UnknownValueError:
                continue
            except sr.RequestError:
                continue
        
        return ""
    
    def _agregar_texto_inteligente(self, nuevo_texto: str):
        """Agrega texto al campo con formateo inteligente y sin duplicados."""
        if not self.campo_texto or not nuevo_texto:
            return
            
        texto_actual = self.campo_texto.value or ""
        nuevo_texto = nuevo_texto.strip()
        
        if not nuevo_texto:
            return
        
        # Verificar si el texto ya existe para evitar duplicados
        if nuevo_texto.lower() in texto_actual.lower():
            print(f"🎤 Texto ya existe, omitiendo: {nuevo_texto}")
            return
        
        # Limpiar texto reconocido (remover palabras muy cortas o raras)
        palabras = nuevo_texto.split()
        palabras_filtradas = []
        
        for palabra in palabras:
            # Filtrar palabras muy cortas o con caracteres extraños
            if len(palabra) >= 2 and palabra.isalpha():
                palabras_filtradas.append(palabra)
        
        if not palabras_filtradas:
            return
            
        nuevo_texto_filtrado = " ".join(palabras_filtradas)
        
        # Formatear texto inteligentemente
        if len(nuevo_texto_filtrado) > 10:  # Solo agregar punto si es una frase larga
            if not nuevo_texto_filtrado.endswith(('.', '!', '?', ':', ',')):
                nuevo_texto_filtrado += '.'
        
        # Combinar con texto existente
        if texto_actual:
            if not texto_actual.endswith(' '):
                texto_actual += ' '
            # Capitalizar si empieza una nueva oración
            if texto_actual.endswith('. '):
                nuevo_texto_filtrado = nuevo_texto_filtrado.capitalize()
        else:
            # Primera oración, capitalizar
            nuevo_texto_filtrado = nuevo_texto_filtrado.capitalize()
        
        # Actualizar campo
        texto_final = texto_actual + nuevo_texto_filtrado
        self.campo_texto.value = texto_final
        
        # Scroll al final del texto
        self.campo_texto.selection = ft.TextSelection(
            base_offset=len(texto_final),
            extent_offset=len(texto_final)
        )
        
        self.page.update()
        print(f"🎤 ✅ Texto agregado: '{nuevo_texto_filtrado}'")
    
    def _actualizar_indicador_esperando(self):
        """Actualiza el indicador cuando está esperando voz."""
        if self.indicador_grabacion and self.indicador_grabacion.visible:
            # Cambiar texto del indicador
            for control in self.indicador_grabacion.content.controls:
                if isinstance(control, ft.Text):
                    control.value = "🎤 Esperando... (habla o presiona para parar)"
                    break
            self.page.update()
    
    def _crear_advertencia_privacidad(self, colors) -> ft.Container:
        """Crea la advertencia sobre privacidad y uso de datos."""
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.INFO_OUTLINE, size=14, color=colors["warning"]),
                    ft.Text(
                        "🔒 Privacidad: Usando tier gratuito (datos anonimizados antes del envío)",
                        size=11,
                        color=colors["warning"],
                        italic=True,
                        weight=ft.FontWeight.W_500,
                    ),
                ],
                spacing=5,
            ),
            bgcolor=colors["warning_light"] if not is_dark_theme() else colors["surface_tertiary"],
            border=ft.border.all(1, colors["warning"]),
            border_radius=6,
            padding=ft.Padding(8, 6, 8, 6),
            margin=ft.Margin(0, 5, 0, 0),
        )
    
    def _crear_info_proteccion_completa(self, colors) -> ft.Container:
        """Crea la información completa sobre protección de datos sensibles."""
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.SHIELD, size=16, color=colors["success"]),
                            ft.Text(
                                "🛡️ Sus datos están completamente protegidos",
                                size=12,
                                color=colors["success"],
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                        spacing=8,
                    ),
                    ft.Container(height=4),
                    ft.Text(
                        "• Nombres de personas • Números de cédula • Radicados • Teléfonos • Emails",
                        size=10,
                        color=colors["text_secondary"],
                        italic=True,
                    ),
                ],
                tight=True,
                spacing=2,
            ),
            bgcolor=colors["success_light"] if not is_dark_theme() else colors["surface_tertiary"],
            border=ft.border.all(1, colors["success"]),
            border_radius=8,
            padding=ft.Padding(12, 10, 12, 10),
            margin=ft.Margin(0, 8, 0, 0),
        )

    def _crear_info_anonimizacion(self, colors) -> ft.Container:
        """Crea la información sobre protección de datos sensibles."""
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(ft.Icons.SHIELD, size=16, color=colors["success"]),
                    ft.Text(
                        "🛡️ Sus datos están protegidos: La información sensible se anonimiza automáticamente",
                        size=12,
                        color=colors["success"],
                        weight=ft.FontWeight.W_500,
                    ),
                ],
                spacing=8,
            ),
            bgcolor=colors["success_light"] if not is_dark_theme() else colors["surface_tertiary"],
            border=ft.border.all(1, colors["success"]),
            border_radius=8,
            padding=ft.Padding(12, 8, 12, 8),
            margin=ft.Margin(0, 8, 0, 0),
        )


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
