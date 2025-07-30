import tkinter as tk
from tkinter import ttk
from datetime import datetime
from typing import List, Callable, Optional

class FormularioAudiencia:
    """Widget compuesto que contiene todos los campos del formulario."""
    
    def __init__(self, parent, fuente=("Segoe UI", 11)):
        self.parent = parent
        self.fuente = fuente
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
        self.motivo_etiquetas = [
            "Juez", "Fiscalía", "Usuario", "INPEC",
            "Víctima", "ICBF", "Defensor Confianza", "Defensor Público",
        ]
        
        # Variables para los checkboxes
        self.motivo_vars = [tk.StringVar() for _ in self.motivo_etiquetas]
        self.checkboxes_motivos = []
        
        # Referencias a widgets importantes
        self.widgets = {}
        
        self._crear_widgets()
        self._configurar_eventos()
    
    def _crear_widgets(self):
        """Crea todos los widgets del formulario."""
        # Campo: Radicado del proceso
        tk.Label(self.parent, text="Radicado del proceso:", bg="#f7f7fa", font=self.fuente).grid(
            row=1, column=0, sticky="e", padx=16, pady=8
        )
        self.widgets['entrada_radicado'] = tk.Entry(self.parent, width=40, font=self.fuente)
        self.widgets['entrada_radicado'].grid(row=1, column=1, sticky="ew", padx=16, pady=8)

        # Campo: Tipo de audiencia
        tk.Label(self.parent, text="Tipo de audiencia:", bg="#f7f7fa", font=self.fuente).grid(
            row=2, column=0, sticky="e", padx=16, pady=8
        )
        frame_tipo = tk.Frame(self.parent, bg="#f7f7fa")
        frame_tipo.grid(row=2, column=1, sticky="ew", padx=16, pady=8)
        frame_tipo.columnconfigure(0, weight=1)
        
        self.widgets['combo_tipo'] = ttk.Combobox(
            frame_tipo, values=self.tipos_audiencia, state="readonly", font=self.fuente, width=28
        )
        self.widgets['combo_tipo'].grid(row=0, column=0, sticky="ew")
        
        self.widgets['entrada_tipo_tra'] = tk.Entry(frame_tipo, width=25, font=self.fuente)
        self.widgets['entrada_tipo_tra'].grid(row=0, column=1, sticky="w", padx=(8, 0))
        self.widgets['entrada_tipo_tra'].grid_remove()  # Oculto por defecto

        # Campo: Fecha
        tk.Label(self.parent, text="Fecha (DD/MM/AAAA):", bg="#f7f7fa", font=self.fuente).grid(
            row=3, column=0, sticky="e", padx=16, pady=8
        )
        frame_fecha = tk.Frame(self.parent, bg="#f7f7fa")
        frame_fecha.grid(row=3, column=1, sticky="w", padx=16, pady=8)
        
        dias = [f"{i:02d}" for i in range(1, 32)]
        meses = [f"{i:02d}" for i in range(1, 13)]
        anios = [str(a) for a in range(datetime.now().year, datetime.now().year + 6)]
        
        self.widgets['combo_dia'] = ttk.Combobox(frame_fecha, values=dias, width=3, font=self.fuente)
        self.widgets['combo_mes'] = ttk.Combobox(frame_fecha, values=meses, width=3, font=self.fuente)
        self.widgets['combo_anio'] = ttk.Combobox(frame_fecha, values=anios, width=5, font=self.fuente)
        
        self.widgets['combo_dia'].grid(row=0, column=0)
        tk.Label(frame_fecha, text="/", bg="#f7f7fa", font=self.fuente).grid(row=0, column=1)
        self.widgets['combo_mes'].grid(row=0, column=2)
        tk.Label(frame_fecha, text="/", bg="#f7f7fa", font=self.fuente).grid(row=0, column=3)
        self.widgets['combo_anio'].grid(row=0, column=4)

        # Campo: Hora
        tk.Label(self.parent, text="Hora (militar):", bg="#f7f7fa", font=self.fuente).grid(
            row=4, column=0, sticky="e", padx=16, pady=8
        )
        frame_hora = tk.Frame(self.parent, bg="#f7f7fa")
        frame_hora.grid(row=4, column=1, sticky="w", padx=16, pady=8)
        
        self.widgets['spin_hora'] = ttk.Spinbox(
            frame_hora, from_=0, to=23, width=3, format="%02.0f", font=self.fuente
        )
        self.widgets['spin_hora'].grid(row=0, column=0)
        tk.Label(frame_hora, text=":", bg="#f7f7fa", font=self.fuente).grid(row=0, column=1)
        self.widgets['spin_minuto'] = ttk.Spinbox(
            frame_hora, from_=0, to=59, width=3, format="%02.0f", font=self.fuente
        )
        self.widgets['spin_minuto'].grid(row=0, column=2)

        # Campo: Juzgado
        tk.Label(self.parent, text="Juzgado:", bg="#f7f7fa", font=self.fuente).grid(
            row=5, column=0, sticky="e", padx=16, pady=8
        )
        self.widgets['entrada_juzgado'] = tk.Entry(self.parent, width=40, font=self.fuente)
        self.widgets['entrada_juzgado'].grid(row=5, column=1, sticky="ew", padx=16, pady=8)

        # Campo: ¿Se realizó?
        tk.Label(self.parent, text="¿Se realizó?", bg="#f7f7fa", font=self.fuente).grid(
            row=6, column=0, sticky="e", padx=16, pady=8
        )
        self.widgets['combo_realizada'] = ttk.Combobox(
            self.parent, values=["SI", "NO"], state="readonly", font=self.fuente
        )
        self.widgets['combo_realizada'].grid(row=6, column=1, sticky="w", padx=16, pady=8)

        # Campo: Motivos de no realización
        frame_motivos = tk.LabelFrame(
            self.parent, text="Motivos (si NO se realizó)", font=self.fuente, bg="#f7f7fa"
        )
        frame_motivos.grid(row=7, column=0, columnspan=2, padx=16, pady=16, sticky="ew")
        frame_motivos.columnconfigure((0, 1, 2, 3), weight=1)
        
        for i, texto in enumerate(self.motivo_etiquetas):
            chk = tk.Checkbutton(
                frame_motivos,
                text=texto,
                variable=self.motivo_vars[i],
                onvalue=texto,
                offvalue="",
                bg="#f7f7fa",
                font=self.fuente,
            )
            chk.grid(row=i // 4, column=i % 4, sticky="w", padx=4, pady=2)
            self.checkboxes_motivos.append(chk)

        # Campo: Observaciones
        tk.Label(self.parent, text="Observaciones:", bg="#f7f7fa", font=self.fuente).grid(
            row=8, column=0, sticky="ne", padx=16, pady=8
        )
        frame_obs = tk.Frame(self.parent, bg="#f7f7fa")
        frame_obs.grid(row=8, column=1, sticky="nsew", padx=16, pady=8)
        frame_obs.rowconfigure(0, weight=1)
        frame_obs.columnconfigure(0, weight=1)
        
        self.widgets['entrada_observaciones'] = tk.Text(frame_obs, width=40, height=4, font=self.fuente)
        self.widgets['entrada_observaciones'].grid(row=0, column=0, sticky="nsew")
        
        scroll_obs = ttk.Scrollbar(
            frame_obs, orient="vertical", command=self.widgets['entrada_observaciones'].yview
        )
        scroll_obs.grid(row=0, column=1, sticky="ns")
        self.widgets['entrada_observaciones'].config(yscrollcommand=scroll_obs.set)
    
    def _configurar_eventos(self):
        """Configura los eventos de los widgets."""
        self.widgets['combo_tipo'].bind("<<ComboboxSelected>>", self._mostrar_entrada_otra)
        self.widgets['combo_realizada'].bind("<<ComboboxSelected>>", self._habilitar_motivos)
        
        # Validación para spinboxes de hora
        vcmd_hora = (self.parent.register(lambda char: char.isdigit()), "%S")
        self.widgets['spin_hora'].config(validate="key", validatecommand=vcmd_hora)
        self.widgets['spin_minuto'].config(validate="key", validatecommand=vcmd_hora)
    
    def _mostrar_entrada_otra(self, event=None):
        """Muestra u oculta el campo de texto para 'Otra' audiencia."""
        if self.widgets['combo_tipo'].get() == "Otra":
            self.widgets['entrada_tipo_tra'].grid()
            self.widgets['entrada_tipo_tra'].focus_set()
        else:
            self.widgets['entrada_tipo_tra'].grid_remove()
            self.widgets['entrada_tipo_tra'].delete(0, tk.END)
    
    def _habilitar_motivos(self, event=None):
        """Habilita o deshabilita los checkboxes de motivos."""
        estado = "normal" if self.widgets['combo_realizada'].get() == "NO" else "disabled"
        for chk in self.checkboxes_motivos:
            chk.config(state=estado)
        if estado == "disabled":
            for var in self.motivo_vars:
                var.set("")
    
    def limpiar_campos(self):
        """Limpia todos los campos del formulario."""
        self.widgets['entrada_radicado'].delete(0, tk.END)
        self.widgets['combo_tipo'].set("")
        self.widgets['entrada_tipo_tra'].delete(0, tk.END)
        
        hoy = datetime.now()
        self.widgets['combo_dia'].set(f"{hoy.day:02d}")
        self.widgets['combo_mes'].set(f"{hoy.month:02d}")
        self.widgets['combo_anio'].set(str(hoy.year))
        
        self.widgets['spin_hora'].set("00")
        self.widgets['spin_minuto'].set("00")
        self.widgets['entrada_juzgado'].delete(0, tk.END)
        self.widgets['combo_realizada'].set("")
        
        for var in self.motivo_vars:
            var.set("")
        
        self.widgets['entrada_observaciones'].delete("1.0", tk.END)
        self._habilitar_motivos()
        self._mostrar_entrada_otra()
        self.widgets['entrada_radicado'].focus_set()
    
    def obtener_datos_formulario(self) -> dict:
        """Recoge los datos del formulario y los devuelve como diccionario."""
        tipo = (
            self.widgets['entrada_tipo_tra'].get().strip()
            if self.widgets['combo_tipo'].get() == "Otra"
            else self.widgets['combo_tipo'].get()
        )
        
        fecha_str = f"{self.widgets['combo_dia'].get()}/{self.widgets['combo_mes'].get()}/{self.widgets['combo_anio'].get()}"
        hora_str = f"{int(self.widgets['spin_hora'].get()):02d}:{int(self.widgets['spin_minuto'].get()):02d}"
        realizada = self.widgets['combo_realizada'].get()
        
        return {
            "radicado": self.widgets['entrada_radicado'].get().strip(),
            "tipo": tipo,
            "fecha": fecha_str,
            "hora": hora_str,
            "juzgado": self.widgets['entrada_juzgado'].get().strip(),
            "realizada_si": "SI" if realizada == "SI" else "",
            "realizada_no": "NO" if realizada == "NO" else "",
            "motivos": [var.get() or "" for var in self.motivo_vars],
            "observaciones": self.widgets['entrada_observaciones'].get("1.0", tk.END).strip(),
        }
    
    def cargar_datos_para_edicion(self, fila_datos):
        """Carga los datos de una fila en el formulario para editarlos."""
        self.limpiar_campos()

        # Radicado (índice 1), Tipo (2), Fecha (3), Hora (4), Juzgado (5), etc.
        self.widgets['entrada_radicado'].insert(0, str(fila_datos[1] or ""))

        tipo = str(fila_datos[2] or "")
        if tipo in self.tipos_audiencia:
            self.widgets['combo_tipo'].set(tipo)
        else:
            self.widgets['combo_tipo'].set("Otra")
            self.widgets['entrada_tipo_tra'].insert(0, tipo)
            self._mostrar_entrada_otra()

        if fila_datos[3] and isinstance(fila_datos[3], str) and "/" in fila_datos[3]:
            dia, mes, anio = fila_datos[3].split("/")
            self.widgets['combo_dia'].set(dia)
            self.widgets['combo_mes'].set(mes)
            self.widgets['combo_anio'].set(anio)

        if fila_datos[4] and isinstance(fila_datos[4], str) and ":" in fila_datos[4]:
            hora, minuto = fila_datos[4].split(":")
            self.widgets['spin_hora'].set(f"{int(hora):02d}")
            self.widgets['spin_minuto'].set(f"{int(minuto):02d}")

        self.widgets['entrada_juzgado'].insert(0, str(fila_datos[5] or ""))

        if fila_datos[6] == "SI":
            self.widgets['combo_realizada'].set("SI")
        elif fila_datos[7] == "NO":
            self.widgets['combo_realizada'].set("NO")

        for i, var in enumerate(self.motivo_vars):
            if len(fila_datos) > i + 8 and fila_datos[i + 8]:
                var.set(str(fila_datos[i + 8]))

        if len(fila_datos) > 16 and fila_datos[16]:
            self.widgets['entrada_observaciones'].insert("1.0", str(fila_datos[16]))

        self._habilitar_motivos()
    
    def agregar_menu_contextual(self):
        """Agrega menú contextual a los widgets de texto."""
        def crear_menu(widget):
            menu = tk.Menu(widget, tearoff=0)
            menu.add_command(label="Cortar", command=lambda: widget.event_generate("<<Cut>>"))
            menu.add_command(label="Copiar", command=lambda: widget.event_generate("<<Copy>>"))
            menu.add_command(label="Pegar", command=lambda: widget.event_generate("<<Paste>>"))
            widget.bind("<Button-3>", lambda e: menu.tk_popup(e.x_root, e.y_root))

        for widget_name in ['entrada_radicado', 'entrada_tipo_tra', 'entrada_juzgado', 'entrada_observaciones']:
            if widget_name in self.widgets:
                crear_menu(self.widgets[widget_name])


class BotonesAccion:
    """Widget que maneja los botones de acción (Guardar, Actualizar, Cancelar)."""
    
    def __init__(self, parent, fuente=("Segoe UI", 11)):
        self.parent = parent
        self.fuente = fuente
        self.frame = tk.Frame(parent, bg="#f7f7fa")
        self.frame.columnconfigure((0, 1, 2), weight=1)
        
        self._crear_botones()
    
    def _crear_botones(self):
        """Crea los botones de acción."""
        self.btn_guardar = tk.Button(
            self.frame,
            text="Guardar",
            bg="#4a90e2",
            fg="white",
            font=(self.fuente[0], 12, "bold"),
        )
        self.btn_guardar.grid(row=0, column=0, columnspan=3, sticky="ew", padx=2)

        self.btn_actualizar = tk.Button(
            self.frame,
            text="Actualizar",
            bg="#28a745",
            fg="white",
            font=(self.fuente[0], 12, "bold"),
        )
        self.btn_actualizar.grid(row=0, column=0, sticky="ew", padx=2)
        self.btn_actualizar.grid_remove()  # Oculto por defecto

        self.btn_cancelar_edicion = tk.Button(
            self.frame,
            text="Cancelar",
            bg="#dc3545",
            fg="white",
            font=(self.fuente[0], 12, "bold"),
        )
        self.btn_cancelar_edicion.grid(row=0, column=1, sticky="ew", padx=2)
        self.btn_cancelar_edicion.grid_remove()  # Oculto por defecto
    
    def grid(self, **kwargs):
        """Posiciona el frame en la ventana."""
        self.frame.grid(**kwargs)
    
    def activar_modo_edicion(self):
        """Cambia los botones al modo de edición."""
        self.btn_guardar.grid_remove()
        self.btn_actualizar.grid()
        self.btn_cancelar_edicion.grid()
    
    def desactivar_modo_edicion(self):
        """Vuelve los botones al modo normal."""
        self.btn_actualizar.grid_remove()
        self.btn_cancelar_edicion.grid_remove()
        self.btn_guardar.grid()
    
    def configurar_comandos(self, cmd_guardar, cmd_actualizar, cmd_cancelar):
        """Configura los comandos de los botones."""
        self.btn_guardar.config(command=cmd_guardar)
        self.btn_actualizar.config(command=cmd_actualizar)
        self.btn_cancelar_edicion.config(command=cmd_cancelar)


class BotonesGestionArchivos:
    """Widget que maneja los botones de gestión de archivos."""
    
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent, bg="#f7f7fa")
        self._crear_botones()
    
    def _crear_botones(self):
        """Crea los botones de gestión de archivos."""
        self.btn_crear_copia = tk.Button(self.frame, text="Crear Copia")
        self.btn_crear_copia.pack(side="left", padx=4, expand=True, fill="x")
        
        self.btn_seleccionar_archivo = tk.Button(self.frame, text="Seleccionar Archivo")
        self.btn_seleccionar_archivo.pack(side="left", padx=4, expand=True, fill="x")
        
        self.btn_editar_registro = tk.Button(
            self.frame, text="Editar Registro", bg="#ffc107", fg="black"
        )
        self.btn_editar_registro.pack(side="left", padx=4, expand=True, fill="x")
        
        self.btn_eliminar_archivo = tk.Button(self.frame, text="Eliminar Archivo")
        self.btn_eliminar_archivo.pack(side="left", padx=4, expand=True, fill="x")
        
        self.btn_descargar_copia = tk.Button(self.frame, text="Descargar Copia")
        self.btn_descargar_copia.pack(side="left", padx=4, expand=True, fill="x")
    
    def grid(self, **kwargs):
        """Posiciona el frame en la ventana."""
        self.frame.grid(**kwargs)
    
    def configurar_comandos(self, crear, seleccionar, editar, eliminar, descargar):
        """Configura los comandos de los botones."""
        self.btn_crear_copia.config(command=crear)
        self.btn_seleccionar_archivo.config(command=seleccionar)
        self.btn_editar_registro.config(command=editar)
        self.btn_eliminar_archivo.config(command=eliminar)
        self.btn_descargar_copia.config(command=descargar)