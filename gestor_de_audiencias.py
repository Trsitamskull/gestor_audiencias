import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from openpyxl import load_workbook
from tkcalendar import DateEntry
from gestor_archivos import (
    crear_copia_plantilla,
    listar_archivos_creados,
    seleccionar_archivo,
    eliminar_archivo,
    descargar_archivo
)

ARCHIVO_EXCEL = None  # No hay archivo seleccionado al inicio
FILA_INICIO_DATOS = 11  # Los datos empiezan desde esta fila

# === Interfaz gráfica con tkinter ===
ventana = tk.Tk()
ventana.title("Ordenador de Audiencias")
ventana.configure(bg="#f7f7fa")
ventana.resizable(True, True)

try:
    ventana.state('zoomed')
except tk.TclError:
    ventana.attributes('-fullscreen', True)

# Centrar ventana en pantalla (puedes dejarlo o quitarlo, ya no es necesario si usas zoomed)
# ventana.update_idletasks()
# w = 600
# h = 560
# x = (ventana.winfo_screenwidth() // 2) - (w // 2)
# y = (ventana.winfo_screenheight() // 2) - (h // 2)
# ventana.geometry(f"{w}x{h}+{x}+{y}")

# Configurar grid para expansión
for i in range(9):
    ventana.rowconfigure(i, weight=1)
ventana.columnconfigure(1, weight=1)

fuente = ("Segoe UI", 11)

tk.Label(ventana, text="Radicado del proceso:", bg="#f7f7fa", font=fuente).grid(row=0, column=0, sticky="e", padx=16, pady=8)
entrada_radicado = tk.Entry(ventana, width=40, font=fuente)
entrada_radicado.grid(row=0, column=1, sticky="ew", padx=16, pady=8)

# Lista de tipos de audiencia
tipos_audiencia = [
  "Alegatos de conclusión",
  "Audiencia concentrada",
  "Audiencia de acusación",
  "Audiencia de juicio oral",
  "Audiencia de preclusion",
  "Audiencia preliminar",
  "Audiencia preparatoria",
  "Otra",  # Esta opción permite ingresar un tipo personalizado
]

tk.Label(ventana, text="Tipo de audiencia:", bg="#f7f7fa", font=fuente).grid(row=1, column=0, sticky="e", padx=16, pady=8)

frame_tipo = tk.Frame(ventana, bg="#f7f7fa")
frame_tipo.grid(row=1, column=1, sticky="ew", padx=16, pady=8)
frame_tipo.columnconfigure(0, weight=1)
frame_tipo.columnconfigure(1, weight=0)

combo_tipo = ttk.Combobox(frame_tipo, values=tipos_audiencia, state="readonly", font=fuente, width=28)
combo_tipo.grid(row=0, column=0, sticky="ew")

entrada_tipo_tra = tk.Entry(frame_tipo, width=25, font=fuente)  # <-- Cambia el ancho aquí
entrada_tipo_tra.grid(row=0, column=1, sticky="w", padx=(8,0))
entrada_tipo_tra.grid_remove()  # Oculto por defecto

def mostrar_entrada_otra(event=None):
    if combo_tipo.get() == "Otra":
        entrada_tipo_tra.grid()
        entrada_tipo_tra.focus_set()
    else:
        entrada_tipo_tra.grid_remove()
        entrada_tipo_tra.delete(0, tk.END)

combo_tipo.bind("<<ComboboxSelected>>", mostrar_entrada_otra)

# Reemplaza el DateEntry por Comboboxes para la fecha
tk.Label(ventana, text="Fecha (DD/MM/AAAA):", bg="#f7f7fa", font=fuente).grid(row=2, column=0, sticky="e", padx=16, pady=8)
frame_fecha = tk.Frame(ventana, bg="#f7f7fa")
frame_fecha.grid(row=2, column=1, sticky="w", padx=16, pady=8)

dias = [f"{i:02d}" for i in range(1, 32)]
meses = [f"{i:02d}" for i in range(1, 13)]
anios = [str(a) for a in range(datetime.now().year, datetime.now().year + 6)]

combo_dia = ttk.Combobox(frame_fecha, values=dias, width=3, state="normal", font=fuente)
combo_mes = ttk.Combobox(frame_fecha, values=meses, width=3, state="normal", font=fuente)
combo_anio = ttk.Combobox(frame_fecha, values=anios, width=5, state="normal", font=fuente)

combo_dia.grid(row=0, column=0)
tk.Label(frame_fecha, text="/", bg="#f7f7fa", font=fuente).grid(row=0, column=1)
combo_mes.grid(row=0, column=2)
tk.Label(frame_fecha, text="/", bg="#f7f7fa", font=fuente).grid(row=0, column=3)
combo_anio.grid(row=0, column=4)

# Selecciona la fecha de hoy por defecto
hoy = datetime.now()
combo_dia.set(f"{hoy.day:02d}")
combo_mes.set(f"{hoy.month:02d}")
combo_anio.set(str(hoy.year))

tk.Label(ventana, text="Hora (militar):", bg="#f7f7fa", font=fuente).grid(row=3, column=0, sticky="e", padx=16, pady=8)
frame_hora = tk.Frame(ventana, bg="#f7f7fa")
frame_hora.grid(row=3, column=1, sticky="w", padx=16, pady=8)
spin_hora = ttk.Spinbox(frame_hora, from_=0, to=23, width=3, format="%02.0f", font=fuente)
spin_hora.grid(row=0, column=0)
tk.Label(frame_hora, text=":", bg="#f7f7fa", font=fuente).grid(row=0, column=1)
spin_minuto = ttk.Spinbox(frame_hora, from_=0, to=59, width=3, format="%02.0f", font=fuente)
spin_minuto.grid(row=0, column=2)

tk.Label(ventana, text="Juzgado:", bg="#f7f7fa", font=fuente).grid(row=4, column=0, sticky="e", padx=16, pady=8)
entrada_juzgado = tk.Entry(ventana, width=40, font=fuente)
entrada_juzgado.grid(row=4, column=1, sticky="ew", padx=16, pady=8)

tk.Label(ventana, text="¿Se realizó?", bg="#f7f7fa", font=fuente).grid(row=5, column=0, sticky="e", padx=16, pady=8)
combo_realizada = ttk.Combobox(ventana, values=["SI", "NO"], state="readonly", font=fuente)
combo_realizada.grid(row=5, column=1, sticky="w", padx=16, pady=8)

# Motivos de no realización
frame_motivos = tk.LabelFrame(ventana, text="Motivos (si NO se realizó)", font=fuente, bg="#f7f7fa", fg="#333")
frame_motivos.grid(row=6, column=0, columnspan=2, padx=16, pady=16, sticky="ew")
frame_motivos.columnconfigure((0,1,2,3), weight=1)

motivo_etiquetas = ["Juez", "Fiscalía", "Usuario", "INPEC", "Víctima", "ICBF", "Defensor Confianza", "Defensor Público"]
motivo_vars = [tk.StringVar() for _ in motivo_etiquetas]
checkboxes_motivos = []
for i, texto in enumerate(motivo_etiquetas):
    chk = tk.Checkbutton(frame_motivos, text=texto, variable=motivo_vars[i], onvalue=texto, offvalue="",
                         bg="#f7f7fa", font=fuente)
    chk.grid(row=i // 4, column=i % 4, sticky="w", padx=4, pady=2)
    checkboxes_motivos.append(chk)

tk.Label(ventana, text="Observaciones:", bg="#f7f7fa", font=fuente).grid(row=7, column=0, sticky="ne", padx=16, pady=8)
frame_obs = tk.Frame(ventana, bg="#f7f7fa")
frame_obs.grid(row=7, column=1, sticky="nsew", padx=16, pady=8)
frame_obs.rowconfigure(0, weight=1)
frame_obs.columnconfigure(0, weight=1)
entrada_observaciones = tk.Text(frame_obs, width=40, height=4, font=fuente)
entrada_observaciones.grid(row=0, column=0, sticky="nsew")
scroll_obs = ttk.Scrollbar(frame_obs, orient="vertical", command=entrada_observaciones.yview)
scroll_obs.grid(row=0, column=1, sticky="ns")
entrada_observaciones.config(yscrollcommand=scroll_obs.set)

btn_guardar = tk.Button(ventana, text="Guardar", bg="#4a90e2", fg="white", font=(fuente[0], 12, "bold"))
btn_guardar.grid(row=8, column=0, columnspan=2, pady=20, padx=16, sticky="ew")

# Solo números para hora y minuto (Spinbox)
def solo_hora(char):
    return char.isdigit()

vcmd_hora = (ventana.register(solo_hora), "%S")
spin_hora.config(validate="key", validatecommand=vcmd_hora)
spin_minuto.config(validate="key", validatecommand=vcmd_hora)

# === Funciones ===
def habilitar_motivos():
    estado = "normal" if combo_realizada.get() == "NO" else "disabled"
    for chk in checkboxes_motivos:
        chk.config(state=estado)
    if estado == "disabled":
        for var in motivo_vars:
            var.set("")

def limpiar_campos():
    entrada_radicado.delete(0, tk.END)
    combo_tipo.set("")
    entrada_tipo_tra.delete(0, tk.END)
    # Actualiza los combos de fecha a hoy
    hoy = datetime.now()
    combo_dia.set(f"{hoy.day:02d}")
    combo_mes.set(f"{hoy.month:02d}")
    combo_anio.set(str(hoy.year))
    spin_hora.set("00")
    spin_minuto.set("00")
    entrada_juzgado.delete(0, tk.END)
    combo_realizada.set("")
    for var in motivo_vars:
        var.set("")
    entrada_observaciones.delete("1.0", tk.END)
    habilitar_motivos()
    mostrar_entrada_otra()  # <-- Esto oculta el campo "Otra" si está visible

def guardar_datos():
    import os
    if not ARCHIVO_EXCEL or not os.path.isfile(ARCHIVO_EXCEL):
        messagebox.showwarning("Archivo no seleccionado", "Debes seleccionar un archivo válido antes de guardar.")
        return
    radicado = entrada_radicado.get()
    tipo = entrada_tipo_tra.get() if combo_tipo.get() == "Otra" else combo_tipo.get()
    fecha = f"{combo_dia.get()}/{combo_mes.get()}/{combo_anio.get()}"
    hora_val = spin_hora.get() if spin_hora.get().isdigit() else "00"
    minuto_val = spin_minuto.get() if spin_minuto.get().isdigit() else "00"
    hora = f"{int(hora_val):02d}:{int(minuto_val):02d}"
    juzgado = entrada_juzgado.get()
    realizada = combo_realizada.get()
    realizada_si = "SI" if realizada == "SI" else ""
    realizada_no = "NO" if realizada == "NO" else ""
    observaciones = entrada_observaciones.get("1.0", tk.END).strip()

    # --- Validación de motivos obligatorios si es NO ---
    if realizada == "NO":
        motivos_seleccionados = [var.get() for var in motivo_vars if var.get()]
        if not motivos_seleccionados:
            messagebox.showerror("Motivo requerido", "Debes seleccionar al menos un motivo si la audiencia NO se realizó.")
            return

    if not (radicado and tipo and fecha and hora and juzgado and realizada):
        if not messagebox.askyesno("Advertencia", "Hay campos obligatorios sin llenar.\n¿Deseas guardar de todas formas?"):
            return
    try:
        dt_fecha = datetime.strptime(fecha, "%d/%m/%Y")
    except ValueError:
        messagebox.showerror("Formato de fecha inválido", f"La fecha '{fecha}' no es válida. Usa el formato DD/MM/AAAA.")
        return
    try:
        dt_hora = datetime.strptime(hora, "%H:%M")
    except ValueError:
        messagebox.showerror("Formato de hora inválido", f"La hora '{hora}' no es válida. Usa el formato HH:MM en horario militar.")
        return

    motivos = [""] * 8
    if realizada == "NO":
        motivos = [str(var.get()) if var.get() else "" for var in motivo_vars]

    wb = load_workbook(ARCHIVO_EXCEL)
    ws = wb.active

    # Leer todos los registros existentes
    datos_tabla = []
    for row in ws.iter_rows(min_row=FILA_INICIO_DATOS, max_row=ws.max_row, values_only=True):
        if not row or row[1] is None:
            continue
        try:
            f = datetime.strptime(str(row[3]), "%d/%m/%Y")
            h = datetime.strptime(str(row[4]), "%H:%M")
        except Exception:
            continue
        datos_tabla.append((f, h, row))

    # Agregar el nuevo registro
    nuevo_registro = (
        dt_fecha,
        dt_hora,
        (
            "",  # N° (columna A, 1)
            radicado,                # B, 2
            tipo,                    # C, 3
            dt_fecha.strftime("%d/%m/%Y"),  # D, 4
            dt_hora.strftime("%H:%M"),      # E, 5
            juzgado,                 # F, 6
            realizada_si,            # G, 7
            realizada_no,            # H, 8
            *motivos,                # I-P, 9-16 (8 motivos)
            observaciones            # Q, 17
        )
    )
    datos_tabla.append(nuevo_registro)
    datos_tabla.sort(key=lambda x: (x[0], x[1]), reverse=True)

    # Limpiar todas las filas de datos
    for i in range(FILA_INICIO_DATOS, FILA_INICIO_DATOS + len(datos_tabla) + 10):
        for j in range(1, 21):
            ws.cell(row=i, column=j, value=None)

    # Escribir los registros ordenados
    for idx, (_, _, fila) in enumerate(datos_tabla, start=1):
        ws.cell(row=FILA_INICIO_DATOS + idx - 1, column=1, value=idx)  # N° en A
        for col, val in enumerate(fila[1:], start=2):  # B=2, C=3, ..., Q=17
            ws.cell(row=FILA_INICIO_DATOS + idx - 1, column=col, value=val if val is not None else "")

    try:
        wb.save(ARCHIVO_EXCEL)
        messagebox.showinfo("Éxito", "Datos guardados y ordenados correctamente.")
    except PermissionError:
        messagebox.showerror("Error", "No se pudo guardar el archivo. ¿Está abierto en otro programa?")
    sumar_motivos()
    limpiar_campos()

def sumar_motivos():
    if not ARCHIVO_EXCEL:
        return
    wb = load_workbook(ARCHIVO_EXCEL)
    ws = wb.active
    totales = [0] * 8  # Para las 8 columnas de motivos (I a P)
    total_si = 0       # Para el total de "SI" en columna G

    for fila in range(11, 111):
        # Suma "SI" en columna G (7)
        if ws.cell(row=fila, column=7).value == "SI":
            total_si += 1
        # Suma motivos en columnas I (9) a P (16)
        for col in range(9, 17):
            if ws.cell(row=fila, column=col).value not in (None, ""):
                totales[col - 9] += 1

    # Escribir los totales de motivos en la fila 111
    for i, total in enumerate(totales):
        ws.cell(row=111, column=9 + i, value=total)
    # Escribir el total de "SI" en la fila 111, columna G (7)
    ws.cell(row=111, column=7, value=total_si)

    wb.save(ARCHIVO_EXCEL)

combo_realizada.bind("<<ComboboxSelected>>", lambda _: habilitar_motivos())
btn_guardar.config(command=guardar_datos)
habilitar_motivos()

# === Gestión de archivos de plantilla ===

def crear_nueva_copia():
    nombre = tk.simpledialog.askstring("Nuevo archivo", "Nombre para la nueva copia (ej: abril_2025):")
    if nombre:
        if not nombre.lower().endswith(".xlsx"):
            nombre += ".xlsx"
        try:
            crear_copia_plantilla(nombre)
            messagebox.showinfo("Éxito", f"Archivo '{nombre}' creado.")
        except FileExistsError:
            messagebox.showerror("Error", "Ya existe un archivo con ese nombre.")

archivo_actual_var = tk.StringVar(value="Ningún archivo seleccionado")
label_archivo_actual = tk.Label(ventana, textvariable=archivo_actual_var, bg="#f7f7fa", font=("Segoe UI", 9, "italic"), fg="#555")
label_archivo_actual.grid(row=10, column=0, columnspan=2, sticky="ew", padx=16, pady=(0,12))

def seleccionar_archivo_trabajo():
    archivos = listar_archivos_creados()
    if not archivos:
        messagebox.showinfo("Sin archivos", "No hay archivos creados.")
        return
    seleccion = seleccionar_de_lista("Seleccionar archivo", archivos)
    if seleccion is None:
        return  # El usuario canceló
    global ARCHIVO_EXCEL
    ARCHIVO_EXCEL = seleccionar_archivo(seleccion)
    archivo_actual_var.set(f"Trabajando con: {seleccion}")
    messagebox.showinfo("Archivo seleccionado", f"Ahora trabajando con: {seleccion}")

def eliminar_archivo_trabajo():
    global ARCHIVO_EXCEL
    archivos = listar_archivos_creados()
    if not archivos:
        messagebox.showinfo("Sin archivos", "No hay archivos creados.")
        return
    seleccion = seleccionar_de_lista("Eliminar archivo", archivos)
    if seleccion is None:
        return
    if messagebox.askyesno("Confirmar", f"¿Eliminar '{seleccion}'?"):
        eliminar_archivo(seleccion)
        messagebox.showinfo("Eliminado", f"Archivo '{seleccion}' eliminado.")
        # Si el archivo eliminado era el seleccionado, actualiza el label
        import os
        if ARCHIVO_EXCEL and os.path.basename(ARCHIVO_EXCEL) == seleccion:
            archivo_actual_var.set("Ningún archivo seleccionado")
            ARCHIVO_EXCEL = None

def descargar_archivo_trabajo():
    archivos = listar_archivos_creados()
    if not archivos:
        messagebox.showinfo("Sin archivos", "No hay archivos creados.")
        return
    seleccion = seleccionar_de_lista("Descargar archivo", archivos)
    if seleccion is None:
        return
    destino = descargar_archivo(seleccion)
    if destino:
        messagebox.showinfo("Descargado", f"Archivo guardado en:\n{destino}")

def seleccionar_de_lista(titulo, archivos):
    seleccion = None

    def confirmar():
        nonlocal seleccion
        seleccion = combo.get()
        win.destroy()

    win = tk.Toplevel(ventana)
    win.title(titulo)
    win.grab_set()
    tk.Label(win, text="Selecciona un archivo:").pack(padx=10, pady=8)
    combo = ttk.Combobox(win, values=archivos, state="readonly", width=40)
    combo.pack(padx=10, pady=8)
    combo.current(0)
    tk.Button(win, text="Aceptar", command=confirmar).pack(pady=8)
    win.wait_window()
    return seleccion

# Botones para gestión de archivos
frame_archivos = tk.Frame(ventana, bg="#f7f7fa")
frame_archivos.grid(row=9, column=0, columnspan=2, pady=12, padx=16, sticky="ew")
tk.Button(frame_archivos, text="Crear copia plantilla", command=crear_nueva_copia).pack(side="left", padx=4)
tk.Button(frame_archivos, text="Seleccionar archivo", command=seleccionar_archivo_trabajo).pack(side="left", padx=4)
tk.Button(frame_archivos, text="Eliminar archivo", command=eliminar_archivo_trabajo).pack(side="left", padx=4)
tk.Button(frame_archivos, text="Descargar archivo", command=descargar_archivo_trabajo).pack(side="left", padx=4)

def agregar_menu_contextual(widget):
    menu = tk.Menu(widget, tearoff=0)
    menu.add_command(label="Cortar", command=lambda: widget.event_generate("<<Cut>>"))
    menu.add_command(label="Copiar", command=lambda: widget.event_generate("<<Copy>>"))
    menu.add_command(label="Pegar", command=lambda: widget.event_generate("<<Paste>>"))

    def mostrar_menu(event):
        menu.tk_popup(event.x_root, event.y_root)
    widget.bind("<Button-3>", mostrar_menu)  # Click derecho

# Aplica el menú contextual a los campos de entrada
agregar_menu_contextual(entrada_radicado)
agregar_menu_contextual(entrada_tipo_tra)
agregar_menu_contextual(entrada_juzgado)
agregar_menu_contextual(entrada_observaciones)

# Etiqueta de crédito
ventana.update_idletasks()  # Asegura que la ventana esté completamente cargada
label_credito = tk.Label(
    ventana,
    text="© 2025 - Hecho por Jose David Bustamante Sánchez",
    bg="#f7f7fa",
    fg="#777",
    font=("Segoe UI", 9, "italic")
)
label_credito.grid(row=11, column=0, columnspan=2, pady=(0, 16))

ventana.mainloop()