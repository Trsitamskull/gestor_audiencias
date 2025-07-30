import customtkinter as ctk
from tkinter import messagebox
from typing import List, Tuple, Optional, Callable


class VentanaSeleccionRegistro:
    """Ventana para seleccionar un registro para editar."""

    def __init__(
        self,
        parent,
        registros: List[Tuple[int, List]],
        callback: Callable[[int, List], None],
    ):
        self.parent = parent
        self.registros = registros
        self.callback = callback
        self.ventana = None
        # Usar after para crear la ventana después de que el parent sea visible
        parent.after(10, self._crear_ventana)

    def _crear_ventana(self):
        """Crea la ventana de selección."""
        self.ventana = ctk.CTkToplevel(self.parent)
        self.ventana.title("Seleccionar Registro para Editar")
        self.ventana.geometry("900x500")
        self.ventana.resizable(True, True)

        # Centrar ventana
        self.ventana.transient(self.parent)
        self.ventana.after(100, self._centrar_ventana)

        # Crear el frame principal
        main_frame = ctk.CTkFrame(self.ventana)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        titulo = ctk.CTkLabel(
            main_frame,
            text="Seleccionar Registro para Editar",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
        )
        titulo.pack(pady=(0, 20))

        # Frame para el scrollable frame
        lista_frame = ctk.CTkScrollableFrame(main_frame, height=300)
        lista_frame.pack(fill="both", expand=True, pady=(0, 20))

        # Crear elementos de la lista
        for i, (fila_num, datos) in enumerate(self.registros):
            item_frame = ctk.CTkFrame(lista_frame)
            item_frame.pack(fill="x", pady=5, padx=10)

            # Información del registro
            info_text = f"#{datos[0] or i+1} - {datos[1]} - {datos[2]} - {datos[3]} - {datos[4]}"

            ctk.CTkLabel(
                item_frame, text=info_text, font=ctk.CTkFont(family="Segoe UI", size=12)
            ).pack(side="left", padx=15, pady=10)

            # Botón editar
            btn_editar = ctk.CTkButton(
                item_frame,
                text="Editar",
                width=80,
                height=30,
                command=lambda fn=fila_num, d=datos: self._on_editar_item(fn, d),
            )
            btn_editar.pack(side="right", padx=15, pady=5)

        # Botón cancelar
        ctk.CTkButton(
            main_frame, text="Cancelar", command=self._on_cancelar, width=100
        ).pack(pady=10)

    def _centrar_ventana(self):
        """Centra la ventana modal."""
        if self.ventana:
            self.ventana.update_idletasks()
            x = (
                self.parent.winfo_x()
                + (self.parent.winfo_width() // 2)
                - (self.ventana.winfo_width() // 2)
            )
            y = (
                self.parent.winfo_y()
                + (self.parent.winfo_height() // 2)
                - (self.ventana.winfo_height() // 2)
            )
            self.ventana.geometry(f"+{x}+{y}")

            # Hacer modal después de centrar
            self.ventana.grab_set()
            self.ventana.focus()

    def _on_editar_item(self, fila_num, datos_completos):
        """Maneja la selección de un registro para editar."""
        self.callback(fila_num, datos_completos)
        if self.ventana:
            self.ventana.destroy()

    def _on_cancelar(self):
        """Cancela la selección."""
        if self.ventana:
            self.ventana.destroy()


class VentanaSeleccionArchivo:
    """Ventana genérica para seleccionar un archivo de una lista."""

    def __init__(
        self, parent, titulo: str, archivos: List[str], callback: Callable[[str], None]
    ):
        self.parent = parent
        self.titulo = titulo
        self.archivos = archivos
        self.callback = callback
        # Usar after para crear la ventana después de que el parent sea visible
        parent.after(10, self._crear_ventana)

    def _crear_ventana(self):
        """Crea la ventana de selección."""
        self.ventana = ctk.CTkToplevel(self.parent)
        self.ventana.title(self.titulo)
        self.ventana.geometry("500x400")
        self.ventana.resizable(False, False)

        # Centrar ventana
        self.ventana.transient(self.parent)
        self.ventana.after(100, self._centrar_ventana)

        # Frame principal
        main_frame = ctk.CTkFrame(self.ventana)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        titulo_label = ctk.CTkLabel(
            main_frame,
            text="Seleccione un archivo:",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
        )
        titulo_label.pack(pady=(20, 30))

        # Lista de archivos
        lista_frame = ctk.CTkScrollableFrame(main_frame, height=200)
        lista_frame.pack(fill="both", expand=True, pady=(0, 20))

        for archivo in self.archivos:
            item_frame = ctk.CTkFrame(lista_frame)
            item_frame.pack(fill="x", pady=5, padx=10)

            ctk.CTkLabel(
                item_frame,
                text=f"📄 {archivo}",
                font=ctk.CTkFont(family="Segoe UI", size=12),
            ).pack(side="left", padx=15, pady=10)

            ctk.CTkButton(
                item_frame,
                text="Seleccionar",
                width=100,
                height=30,
                command=lambda a=archivo: self._on_seleccionar(a),
            ).pack(side="right", padx=15, pady=5)

        # Botón cancelar
        ctk.CTkButton(
            main_frame, text="Cancelar", command=self._on_cancelar, width=100
        ).pack(pady=10)

    def _centrar_ventana(self):
        """Centra la ventana modal."""
        self.ventana.update_idletasks()
        x = (
            self.parent.winfo_x()
            + (self.parent.winfo_width() // 2)
            - (self.ventana.winfo_width() // 2)
        )
        y = (
            self.parent.winfo_y()
            + (self.parent.winfo_height() // 2)
            - (self.ventana.winfo_height() // 2)
        )
        self.ventana.geometry(f"+{x}+{y}")

        # Hacer modal después de centrar
        self.ventana.grab_set()
        self.ventana.focus()

    def _on_seleccionar(self, archivo):
        """Procesa la selección."""
        self.callback(archivo)
        self.ventana.destroy()

    def _on_cancelar(self):
        """Cancela la selección."""
        self.ventana.destroy()


class DialogoCrearArchivo:
    """Diálogo para crear un nuevo archivo."""

    def __init__(self, parent, callback: Callable[[str], None]):
        self.parent = parent
        self.callback = callback
        # Usar after para crear la ventana después de que el parent sea visible
        parent.after(10, self._crear_dialogo)

    def _crear_dialogo(self):
        """Crea el diálogo."""
        self.ventana = ctk.CTkToplevel(self.parent)
        self.ventana.title("Crear Nuevo Archivo")
        self.ventana.geometry("450x200")
        self.ventana.resizable(False, False)

        # Centrar ventana
        self.ventana.transient(self.parent)
        self.ventana.after(100, self._centrar_ventana)

        # Frame principal
        main_frame = ctk.CTkFrame(self.ventana)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Título
        titulo = ctk.CTkLabel(
            main_frame,
            text="Crear Nuevo Archivo",
            font=ctk.CTkFont(family="Segoe UI", size=18, weight="bold"),
        )
        titulo.pack(pady=(20, 10))

        # Instrucción
        instruccion = ctk.CTkLabel(
            main_frame,
            text="Nombre para la copia (ej: mayo_2025):",
            font=ctk.CTkFont(family="Segoe UI", size=12),
        )
        instruccion.pack(pady=(0, 15))

        # Entry
        self.entry = ctk.CTkEntry(
            main_frame,
            width=300,
            height=35,
            font=ctk.CTkFont(family="Segoe UI", size=12),
            placeholder_text="Escriba el nombre del archivo...",
        )
        self.entry.pack(pady=(0, 20))

        # Frame para botones
        btn_frame = ctk.CTkFrame(main_frame)
        btn_frame.pack(pady=10)

        ctk.CTkButton(
            btn_frame,
            text="Crear",
            command=self._on_crear,
            width=100,
            fg_color=("#059669", "#10b981"),
            hover_color=("#047857", "#059669"),
        ).pack(side="left", padx=(20, 10), pady=15)

        ctk.CTkButton(
            btn_frame,
            text="Cancelar",
            command=self._on_cancelar,
            width=100,
            fg_color=("#dc2626", "#ef4444"),
            hover_color=("#b91c1c", "#dc2626"),
        ).pack(side="right", padx=(10, 20), pady=15)
        # Hacer que Enter funcione como Crear
        self.ventana.bind("<Return>", lambda _: self._on_crear())
        self.ventana.bind("<Return>", lambda e: self._on_crear())

    def _centrar_ventana(self):
        """Centra la ventana modal."""
        if self.ventana:
            self.ventana.update_idletasks()
            x = (
                self.parent.winfo_x()
                + (self.parent.winfo_width() // 2)
                - (self.ventana.winfo_width() // 2)
            )
            y = (
                self.parent.winfo_y()
                + (self.parent.winfo_height() // 2)
                - (self.ventana.winfo_height() // 2)
            )
            self.ventana.geometry(f"+{x}+{y}")

            # Hacer modal y dar focus
            self.ventana.grab_set()
            self.entry.focus()
        self.entry.focus()

    def _on_crear(self):
        """Procesa la creación del archivo."""
        nombre = self.entry.get().strip()
        if nombre:
            if not nombre.lower().endswith(".xlsx"):
                nombre += ".xlsx"
            self.callback(nombre)
        self.ventana.destroy()

    def _on_cancelar(self):
        """Cancela la creación."""
        self.ventana.destroy()


class DialogoConfirmacion:
    """Diálogo de confirmación genérico."""

    @staticmethod
    def confirmar(
        parent,
        titulo: str,
        mensaje: str,
        callback_si: Callable[[], None],
        callback_no: Optional[Callable[[], None]] = None,
    ):
        """Muestra un diálogo de confirmación."""
        resultado = messagebox.askyesno(titulo, mensaje, parent=parent)
        if resultado and callback_si:
            callback_si()
        elif not resultado and callback_no:
            callback_no()
        return resultado

    @staticmethod
    def mostrar_info(parent, titulo: str, mensaje: str):
        """Muestra un diálogo informativo."""
        messagebox.showinfo(titulo, mensaje, parent=parent)

    @staticmethod
    def mostrar_error(parent, titulo: str, mensaje: str):
        """Muestra un diálogo de error."""
        messagebox.showerror(titulo, mensaje, parent=parent)

    @staticmethod
    def mostrar_advertencia(parent, titulo: str, mensaje: str):
        """Muestra un diálogo de advertencia."""
        messagebox.showwarning(titulo, mensaje, parent=parent)


def centrar_ventana(ventana, ancho: int, alto: int):
    """Centra una ventana en la pantalla."""
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()

    x = (ancho_pantalla - ancho) // 2
    y = (alto_pantalla - alto) // 2

    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")
