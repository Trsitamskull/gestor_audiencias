import flet as ft
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


class DialogoCrearArchivo:
    """Diálogo para crear un nuevo archivo."""

    def __init__(self, page: ft.Page, callback):
        self.page = page
        self.callback = callback
        self.dlg = None
        self.entry = None
        self._crear_dialogo()

    def _crear_dialogo(self):
        """Crea el diálogo."""
        self.entry = ft.TextField(
            label="Nombre del archivo",
            hint_text="Ej: mayo_2025",
            width=300,
            autofocus=True,
        )

        self.dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("📄 Crear Nuevo Archivo"),
            content=ft.Column(
                [ft.Text("Ingrese el nombre para la nueva copia:"), self.entry],
                tight=True,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=self._cancelar),
                ft.TextButton("Crear", on_click=self._crear),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        self.page.dialog = self.dlg
        self.dlg.open = True
        self.page.update()

    def _crear(self, e):
        """Crea el archivo."""
        nombre = self.entry.value.strip()
        if nombre:
            if not nombre.lower().endswith(".xlsx"):
                nombre += ".xlsx"
            self.callback(nombre)
        self._cerrar()

    def _cancelar(self, e):
        """Cancela la creación."""
        self._cerrar()

    def _cerrar(self):
        """Cierra el diálogo."""
        self.dlg.open = False
        self.page.update()


class VentanaSeleccionArchivo:
    """Ventana para seleccionar un archivo."""

    def __init__(self, page: ft.Page, titulo: str, archivos: list, callback):
        self.page = page
        self.titulo = titulo
        self.archivos = archivos
        self.callback = callback
        self.dlg = None
        self._crear_ventana()

    def _crear_ventana(self):
        """Crea la ventana de selección."""
        items = []
        for archivo in self.archivos:
            items.append(
                ft.ListTile(
                    leading=ft.Icon(ft.icons.DESCRIPTION),
                    title=ft.Text(archivo),
                    on_click=lambda e, archivo=archivo: self._seleccionar(archivo),
                )
            )

        self.dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"📁 {self.titulo}"),
            content=ft.Column(controls=items, height=300, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Cancelar", on_click=self._cancelar),
            ],
        )

        self.page.dialog = self.dlg
        self.dlg.open = True
        self.page.update()

    def _seleccionar(self, archivo):
        """Selecciona un archivo."""
        self.callback(archivo)
        self._cerrar()

    def _cancelar(self, e):
        """Cancela la selección."""
        self._cerrar()

    def _cerrar(self):
        """Cierra el diálogo."""
        self.dlg.open = False
        self.page.update()


class VentanaSeleccionRegistro:
    """Ventana para seleccionar un registro para editar."""

    def __init__(self, page: ft.Page, registros: list, callback):
        self.page = page
        self.registros = registros
        self.callback = callback
        self.dlg = None
        self._crear_ventana()

    def _crear_ventana(self):
        """Crea la ventana de selección."""
        items = []
        for i, (fila_num, datos) in enumerate(self.registros):
            info = f"#{i+1} - {datos[1] or 'Sin radicado'} - {datos[2] or 'Sin tipo'} - {datos[3] or 'Sin fecha'}"
            items.append(
                ft.ListTile(
                    leading=ft.Icon(ft.icons.EDIT),
                    title=ft.Text(info, size=12),
                    on_click=lambda e, fn=fila_num, d=datos: self._seleccionar(fn, d),
                )
            )

        self.dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("✏️ Seleccionar Registro para Editar"),
            content=ft.Column(controls=items, height=400, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Cancelar", on_click=self._cancelar),
            ],
        )

        self.page.dialog = self.dlg
        self.dlg.open = True
        self.page.update()

    def _seleccionar(self, fila_num, datos):
        """Selecciona un registro."""
        self.callback(fila_num, datos)
        self._cerrar()

    def _cancelar(self, e):
        """Cancela la selección."""
        self._cerrar()

    def _cerrar(self):
        """Cierra el diálogo."""
        self.dlg.open = False
        self.page.update()


class DialogoConfirmacion:
    """Diálogo de confirmación."""

    @staticmethod
    def confirmar(page: ft.Page, titulo: str, mensaje: str, callback_si):
        """Muestra un diálogo de confirmación."""

        def confirmar_accion(e):
            dlg.open = False
            page.update()
            callback_si()

        def cancelar_accion(e):
            dlg.open = False
            page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(titulo),
            content=ft.Text(mensaje),
            actions=[
                ft.TextButton("No", on_click=cancelar_accion),
                ft.TextButton("Sí", on_click=confirmar_accion),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.dialog = dlg
        dlg.open = True
        page.update()


class VentanaPrincipal:
    """Ventana principal de la aplicación con Flet - Interfaz Moderna."""

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
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20
        self.page.window_width = 1000
        self.page.window_height = 800
        self.page.window_min_width = 900
        self.page.window_min_height = 700
        self.page.window_center()

        # Tema personalizado elegante
        self.page.theme = ft.Theme(
            color_scheme_seed=ft.colors.BLUE,
            visual_density=ft.ThemeVisualDensity.COMFORTABLE,
        )

    def _crear_interfaz(self):
        """Crea toda la interfaz de usuario."""

        # === HEADER ===
        header = self._crear_header()

        # === FORMULARIO PRINCIPAL ===
        formulario = self._crear_formulario()

        # === BOTONES DE ACCIÓN ===
        botones_accion = self._crear_botones_accion()

        # === GESTIÓN DE ARCHIVOS ===
        gestion_archivos = self._crear_gestion_archivos()

        # === INFO DE ESTADO ===
        info_estado = self._crear_info_estado()

        # === FOOTER ===
        footer = self._crear_footer()

        # Agregar todo a la página en un ListView scrollable
        contenido = ft.ListView(
            controls=[
                header,
                formulario,
                botones_accion,
                gestion_archivos,
                info_estado,
                footer,
            ],
            expand=True,
            spacing=20,
            padding=ft.padding.symmetric(vertical=10),
        )

        self.page.add(contenido)

    def _crear_header(self):
        """Crea el header profesional."""
        self.contador_registros = ft.Text(
            "Registros: 0", size=14, weight=ft.FontWeight.BOLD
        )

        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Text(
                        "⚖️ GESTOR DE AUDIENCIAS JUDICIALES",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.BLUE_900,
                    ),
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(ft.icons.ANALYTICS, size=20),
                                self.contador_registros,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=8,
                        ),
                        bgcolor=ft.colors.BLUE_50,
                        border_radius=10,
                        padding=ft.padding.symmetric(horizontal=15, vertical=10),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            bgcolor=ft.colors.WHITE,
            border_radius=15,
            padding=25,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.colors.with_opacity(0.1, ft.colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
        )

    def _crear_formulario(self):
        """Crea el formulario principal."""

        # Título del formulario
        titulo_form = ft.Text(
            "📝 INFORMACIÓN DE LA AUDIENCIA",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.BLUE_800,
        )

        # Campos del formulario
        campos = [
            titulo_form,
            ft.Divider(height=20, color=ft.colors.BLUE_200),
            self._crear_campo_radicado(),
            self._crear_campo_tipo_audiencia(),
            self._crear_campo_fecha(),
            self._crear_campo_hora(),
            self._crear_campo_juzgado(),
            self._crear_campo_realizada(),
            self._crear_campo_motivos(),
            self._crear_campo_observaciones(),
        ]

        return ft.Container(
            content=ft.Column(controls=campos, spacing=15, scroll=ft.ScrollMode.AUTO),
            bgcolor=ft.colors.WHITE,
            border_radius=15,
            padding=30,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.colors.with_opacity(0.1, ft.colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
        )

    def _crear_campo_radicado(self):
        """Campo de radicado."""
        self.entrada_radicado = ft.TextField(
            label="📋 Radicado del proceso",
            border_radius=10,
            filled=True,
            bgcolor=ft.colors.BLUE_50,
            prefix_icon=ft.icons.FOLDER_OUTLINED,
        )
        return self.entrada_radicado

    def _crear_campo_tipo_audiencia(self):
        """Campo de tipo de audiencia."""
        self.combo_tipo = ft.Dropdown(
            label="⚖️ Tipo de audiencia",
            options=[ft.dropdown.Option(tipo) for tipo in self.tipos_audiencia],
            border_radius=10,
            filled=True,
            bgcolor=ft.colors.BLUE_50,
            on_change=self._on_tipo_change,
        )

        self.entrada_tipo_otra = ft.TextField(
            label="Especificar otro tipo...",
            border_radius=10,
            filled=True,
            bgcolor=ft.colors.ORANGE_50,
            visible=False,
        )

        return ft.Column(controls=[self.combo_tipo, self.entrada_tipo_otra], spacing=10)

    def _crear_campo_fecha(self):
        """Campo de fecha."""
        dias = [f"{i:02d}" for i in range(1, 32)]
        meses = [f"{i:02d}" for i in range(1, 13)]
        anios = [str(a) for a in range(datetime.now().year, datetime.now().year + 6)]

        self.combo_dia = ft.Dropdown(
            label="Día",
            options=[ft.dropdown.Option(dia) for dia in dias],
            width=100,
            border_radius=10,
            filled=True,
            bgcolor=ft.colors.BLUE_50,
        )

        self.combo_mes = ft.Dropdown(
            label="Mes",
            options=[ft.dropdown.Option(mes) for mes in meses],
            width=100,
            border_radius=10,
            filled=True,
            bgcolor=ft.colors.BLUE_50,
        )

        self.combo_anio = ft.Dropdown(
            label="Año",
            options=[ft.dropdown.Option(anio) for anio in anios],
            width=120,
            border_radius=10,
            filled=True,
            bgcolor=ft.colors.BLUE_50,
        )

        return ft.Column(
            controls=[
                ft.Text("📅 Fecha (DD/MM/AAAA)", size=16, weight=ft.FontWeight.BOLD),
                ft.Row(
                    controls=[self.combo_dia, self.combo_mes, self.combo_anio],
                    spacing=15,
                ),
            ],
            spacing=10,
        )

    def _crear_campo_hora(self):
        """Campo de hora."""
        self.entrada_hora = ft.TextField(
            label="Hora",
            hint_text="00",
            width=80,
            border_radius=10,
            filled=True,
            bgcolor=ft.colors.BLUE_50,
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=2,
        )

        self.entrada_minuto = ft.TextField(
            label="Min",
            hint_text="00",
            width=80,
            border_radius=10,
            filled=True,
            bgcolor=ft.colors.BLUE_50,
            input_filter=ft.NumbersOnlyInputFilter(),
            max_length=2,
        )

        return ft.Column(
            controls=[
                ft.Text("🕐 Hora (24h)", size=16, weight=ft.FontWeight.BOLD),
                ft.Row(
                    controls=[
                        self.entrada_hora,
                        ft.Text(":", size=20, weight=ft.FontWeight.BOLD),
                        self.entrada_minuto,
                    ],
                    spacing=10,
                ),
            ],
            spacing=10,
        )

    def _crear_campo_juzgado(self):
        """Campo de juzgado."""
        self.entrada_juzgado = ft.TextField(
            label="🏛️ Juzgado",
            border_radius=10,
            filled=True,
            bgcolor=ft.colors.BLUE_50,
            prefix_icon=ft.icons.ACCOUNT_BALANCE,
        )
        return self.entrada_juzgado

    def _crear_campo_realizada(self):
        """Campo ¿Se realizó?"""
        self.combo_realizada = ft.Dropdown(
            label="✅ ¿Se realizó?",
            options=[ft.dropdown.Option("SI"), ft.dropdown.Option("NO")],
            width=150,
            border_radius=10,
            filled=True,
            bgcolor=ft.colors.BLUE_50,
            on_change=self._on_realizada_change,
        )
        return self.combo_realizada

    def _crear_campo_motivos(self):
        """Campo de motivos."""
        motivos_labels = [
            "Juez",
            "Fiscalía",
            "Usuario",
            "INPEC",
            "Víctima",
            "ICBF",
            "Defensor Confianza",
            "Defensor Público",
        ]

        self.checkboxes_motivos = []

        checkboxes_row1 = []
        checkboxes_row2 = []

        for i, motivo in enumerate(motivos_labels):
            checkbox = ft.Checkbox(
                label=motivo, disabled=True, fill_color=ft.colors.RED_400
            )
            self.checkboxes_motivos.append(checkbox)

            if i < 4:
                checkboxes_row1.append(checkbox)
            else:
                checkboxes_row2.append(checkbox)

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "❌ MOTIVOS (si NO se realizó)",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.RED_700,
                    ),
                    ft.Row(controls=checkboxes_row1, wrap=True),
                    ft.Row(controls=checkboxes_row2, wrap=True),
                ],
                spacing=15,
            ),
            bgcolor=ft.colors.RED_50,
            border_radius=15,
            border=ft.border.all(2, ft.colors.RED_200),
            padding=20,
        )

    def _crear_campo_observaciones(self):
        """Campo de observaciones."""
        self.entrada_observaciones = ft.TextField(
            label="📝 Observaciones",
            multiline=True,
            min_lines=4,
            max_lines=6,
            border_radius=10,
            filled=True,
            bgcolor=ft.colors.BLUE_50,
        )
        return self.entrada_observaciones

    def _crear_botones_accion(self):
        """Crea los botones de acción."""
        self.btn_guardar = ft.ElevatedButton(
            text="💾 GUARDAR AUDIENCIA",
            icon=ft.icons.SAVE,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor=ft.colors.BLUE_700,
                text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD),
                padding=ft.padding.symmetric(horizontal=30, vertical=15),
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            on_click=self._on_guardar,
            expand=True,
        )

        self.btn_actualizar = ft.ElevatedButton(
            text="✏️ ACTUALIZAR REGISTRO",
            icon=ft.icons.EDIT,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor=ft.colors.GREEN_700,
                text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD),
                padding=ft.padding.symmetric(horizontal=30, vertical=15),
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            on_click=self._on_actualizar,
            expand=True,
            visible=False,
        )

        self.btn_cancelar_edicion = ft.ElevatedButton(
            text="❌ CANCELAR EDICIÓN",
            icon=ft.icons.CANCEL,
            style=ft.ButtonStyle(
                color=ft.colors.WHITE,
                bgcolor=ft.colors.RED_700,
                text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD),
                padding=ft.padding.symmetric(horizontal=30, vertical=15),
                shape=ft.RoundedRectangleBorder(radius=10),
            ),
            on_click=self._on_cancelar_edicion,
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
            bgcolor=ft.colors.WHITE,
            border_radius=15,
            padding=20,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.colors.with_opacity(0.1, ft.colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
        )

    def _crear_gestion_archivos(self):
        """Crea la sección de gestión de archivos."""
        botones = [
            ("📄 Crear", ft.colors.PURPLE_700, self._on_crear_archivo),
            ("🔍 Seleccionar", ft.colors.BLUE_700, self._on_seleccionar_archivo),
            ("✏️ Editar", ft.colors.ORANGE_700, self._on_editar_registro),
            ("🗑️ Eliminar", ft.colors.RED_700, self._on_eliminar_archivo),
            ("💾 Descargar", ft.colors.GREEN_700, self._on_descargar_archivo),
        ]

        botones_controles = []
        for texto, color, callback in botones:
            btn = ft.ElevatedButton(
                text=texto,
                style=ft.ButtonStyle(
                    color=ft.colors.WHITE,
                    bgcolor=color,
                    text_style=ft.TextStyle(size=12, weight=ft.FontWeight.BOLD),
                    padding=ft.padding.symmetric(horizontal=15, vertical=10),
                    shape=ft.RoundedRectangleBorder(radius=8),
                ),
                on_click=callback,
                expand=True,
            )
            botones_controles.append(btn)

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "🗂️ GESTIÓN DE ARCHIVOS",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.colors.BLUE_800,
                    ),
                    ft.Row(controls=botones_controles, spacing=10),
                ],
                spacing=15,
            ),
            bgcolor=ft.colors.WHITE,
            border_radius=15,
            padding=20,
            shadow=ft.BoxShadow(
                spread_radius=1,
                blur_radius=10,
                color=ft.colors.with_opacity(0.1, ft.colors.BLACK),
                offset=ft.Offset(0, 2),
            ),
        )

    def _crear_info_estado(self):
        """Crea la información de estado."""
        self.archivo_actual_text = ft.Text(
            "📁 Ningún archivo seleccionado",
            size=14,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.BLUE_700,
        )

        return ft.Container(
            content=self.archivo_actual_text,
            bgcolor=ft.colors.BLUE_50,
            border_radius=10,
            padding=15,
            alignment=ft.alignment.center,
        )

    def _crear_footer(self):
        """Crea el footer."""
        return ft.Container(
            content=ft.Text(
                "© 2025 - Desarrollado por Jose David Bustamante Sánchez",
                size=12,
                color=ft.colors.GREY_600,
                text_align=ft.TextAlign.CENTER,
            ),
            alignment=ft.alignment.center,
            padding=10,
        )

    # === EVENTOS ===

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

        # Establecer fecha actual
        hoy = datetime.now()
        self.combo_dia.value = f"{hoy.day:02d}"
        self.combo_mes.value = f"{hoj.month:02d}"
        self.combo_anio.value = str(hoy.year)

        # Establecer hora por defecto
        self.entrada_hora.value = "00"
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
        if self.combo_dia:
            self.combo_dia.value = None
        if self.combo_mes:
            self.combo_mes.value = None
        if self.combo_anio:
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

        fecha = f"{self.combo_dia.value or '01'}/{self.combo_mes.value or '01'}/{self.combo_anio.value or '2025'}"

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
        if not self.archivo_excel or not self.excel_manager:
            self._mostrar_snackbar(
                "❌ Primero debe seleccionar un archivo", ft.colors.RED
            )
            return

        datos = self.obtener_datos_formulario()
        valido, mensaje = validar_todos_los_datos(datos)

        if not valido:
            self._mostrar_snackbar(f"❌ {mensaje}", ft.colors.RED)
            return

        try:
            audiencia = Audiencia.from_form_data(datos)
            self.excel_manager.guardar_audiencia(audiencia)
            self.excel_manager.reordenar_y_guardar()

            self._mostrar_snackbar(
                "✅ Registro guardado correctamente", ft.colors.GREEN
            )
            self.limpiar_campos()
            self._inicializar()
            self.actualizar_contador_registros()

        except Exception as e:
            self._mostrar_snackbar(f"❌ Error al guardar: {e}", ft.colors.RED)

    def actualizar_registro(self):
        """Actualiza un registro existente."""
        if not self.fila_editando:
            return

        if not self.archivo_excel or not self.excel_manager:
            self._mostrar_snackbar("❌ No hay archivo seleccionado", ft.colors.RED)
            return

        datos = self.obtener_datos_formulario()
        valido, mensaje = validar_todos_los_datos(datos)

        if not valido:
            self._mostrar_snackbar(f"❌ {mensaje}", ft.colors.RED)
            return

        try:
            audiencia = Audiencia.from_form_data(datos)
            self.excel_manager.actualizar_audiencia(self.fila_editando, audiencia)
            self.excel_manager.reordenar_y_guardar()

            self._mostrar_snackbar(
                "✅ Registro actualizado correctamente", ft.colors.GREEN
            )

            self.desactivar_modo_edicion()
            self.actualizar_contador_registros()

        except Exception as e:
            self._mostrar_snackbar(f"❌ Error al actualizar: {e}", ft.colors.RED)

    def cancelar_edicion(self):
        """Cancela la edición."""
        self.desactivar_modo_edicion()

    def activar_modo_edicion(self):
        """Activa el modo edición."""
        self.modo_edicion = True
        self.btn_guardar.visible = False
        self.btn_actualizar.visible = True
        self.btn_cancelar_edicion.visible = True
        self.page.title = "🏛️ Gestor de Audiencias - EDITANDO"
        self.page.update()

    def desactivar_modo_edicion(self):
        """Desactiva el modo edición."""
        self.modo_edicion = False
        self.fila_editando = None
        self.btn_guardar.visible = True
        self.btn_actualizar.visible = False
        self.btn_cancelar_edicion.visible = False
        self.page.title = "🏛️ Gestor de Audiencias Judiciales"
        self.limpiar_campos()
        self._inicializar()

    def crear_nueva_copia(self):
        """Crea una nueva copia."""

        def callback_crear(nombre):
            try:
                crear_copia_plantilla(nombre)
                self._mostrar_snackbar(
                    f"✅ Archivo '{nombre}' creado.", ft.colors.GREEN
                )
            except FileExistsError:
                self._mostrar_snackbar(
                    "❌ Ya existe un archivo con ese nombre.", ft.colors.RED
                )
            except Exception as e:
                self._mostrar_snackbar(
                    f"❌ No se pudo crear el archivo: {e}", ft.colors.RED
                )

        DialogoCrearArchivo(self.page, callback_crear)

    def seleccionar_archivo_trabajo(self):
        """Selecciona archivo de trabajo."""
        archivos = listar_archivos_creados()
        if not archivos:
            self._mostrar_snackbar(
                "ℹ️ No hay archivos de plantilla creados.", ft.colors.ORANGE
            )
            return

        def callback_seleccionar(nombre_archivo):
            try:
                self.archivo_excel = seleccionar_archivo(nombre_archivo)
                self.excel_manager = ExcelManager(self.archivo_excel)
                self.archivo_actual_text.value = f"📁 Trabajando con: {nombre_archivo}"
                self.actualizar_contador_registros()
                self._mostrar_snackbar(
                    f"✅ Ahora trabajando con: {nombre_archivo}", ft.colors.GREEN
                )
            except Exception as e:
                self._mostrar_snackbar(
                    f"❌ No se pudo seleccionar el archivo: {e}", ft.colors.RED
                )

        VentanaSeleccionArchivo(
            self.page,
            "Seleccionar Archivo de Trabajo",
            archivos,
            callback_seleccionar,
        )

    def seleccionar_registro_para_editar(self):
        """Selecciona registro para editar."""
        if not self.archivo_excel or not self.excel_manager:
            self._mostrar_snackbar(
                "❌ Primero debe seleccionar un archivo", ft.colors.RED
            )
            return

        try:
            registros = self.excel_manager.leer_registros()

            if not registros:
                self._mostrar_snackbar(
                    "ℹ️ No hay registros para editar en el archivo.", ft.colors.ORANGE
                )
                return

            def callback_editar(fila_num, datos_completos):
                self.fila_editando = fila_num
                self.cargar_datos_para_edicion(datos_completos)
                self.activar_modo_edicion()

            VentanaSeleccionRegistro(self.page, registros, callback_editar)

        except Exception as e:
            self._mostrar_snackbar(
                f"❌ Error al leer los registros: {e}", ft.colors.RED
            )

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

        # Fecha
        if len(fila_datos) > 3 and fila_datos[3] and "/" in str(fila_datos[3]):
            try:
                dia, mes, anio = str(fila_datos[3]).split("/")
                self.combo_dia.value = dia
                self.combo_mes.value = mes
                self.combo_anio.value = anio
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
            self._mostrar_snackbar("ℹ️ No hay archivos para eliminar.", ft.colors.ORANGE)
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
            self._mostrar_snackbar(
                f"✅ Archivo '{nombre_archivo}' eliminado.", ft.colors.GREEN
            )

            # Si era el archivo actual, limpiar la selección
            if self.archivo_excel and self.archivo_excel.endswith(nombre_archivo):
                self.archivo_excel = None
                self.excel_manager = None
                self.archivo_actual_text.value = "📁 Ningún archivo seleccionado"
                self.actualizar_contador_registros()

        except Exception as e:
            self._mostrar_snackbar(
                f"❌ No se pudo eliminar el archivo: {e}", ft.colors.RED
            )

    def descargar_archivo_trabajo(self):
        """Descarga archivo de trabajo."""
        archivos = listar_archivos_creados()
        if not archivos:
            self._mostrar_snackbar(
                "ℹ️ No hay archivos para descargar.", ft.colors.ORANGE
            )
            return

        def callback_seleccionar(nombre_archivo):
            try:
                destino = descargar_archivo(nombre_archivo)
                if destino:
                    self._mostrar_snackbar(
                        f"✅ Archivo guardado en: {destino}", ft.colors.GREEN
                    )
            except Exception as e:
                self._mostrar_snackbar(
                    f"❌ No se pudo descargar el archivo: {e}", ft.colors.RED
                )

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

    def _mostrar_snackbar(self, mensaje: str, color: str):
        """Muestra un mensaje tipo snackbar."""
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text(mensaje, color=ft.colors.WHITE), bgcolor=color
        )
        self.page.snack_bar.open = True
        self.page.update()


def crear_app(page: ft.Page):
    """Función principal para crear la app de Flet."""
    app = VentanaPrincipal(page)


def ejecutar_app():
    """Ejecuta la aplicación Flet."""
    # Forzar modo web si hay problemas con ventana
    try:
        ft.app(target=crear_app)
    except Exception as e:
        print("🌐 Abriendo en modo web...")
        ft.app(target=crear_app, view=ft.AppView.WEB_BROWSER, port=8080)
