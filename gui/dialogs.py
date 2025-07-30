import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Tuple, Optional, Callable

class VentanaSeleccionRegistro:
    """Ventana para seleccionar un registro para editar."""
    
    def __init__(self, parent, registros: List[Tuple[int, List]], callback: Callable[[int, List], None]):
        self.parent = parent
        self.registros = registros
        self.callback = callback
        self.ventana = None
        self._crear_ventana()
    
    def _crear_ventana(self):
        """Crea la ventana de selección."""
        self.ventana = tk.Toplevel(self.parent)
        self.ventana.title("Seleccionar Registro para Editar")
        self.ventana.geometry("800x400")
        self.ventana.grab_set()
        
        # Crear el Treeview
        cols = ("N°", "Radicado", "Tipo", "Fecha", "Hora", "Juzgado")
        self.tree = ttk.Treeview(self.ventana, columns=cols, show="headings")
        
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="w")
        
        # Llenar el Treeview con datos
        for fila_num, datos in self.registros:
            self.tree.insert(
                "",
                "end",
                values=(datos[0], datos[1], datos[2], datos[3], datos[4], datos[5]),
                tags=(str(fila_num),),
            )
        
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)
        
        # Botones
        btn_frame = tk.Frame(self.ventana)
        btn_frame.pack(pady=10)
        
        tk.Button(
            btn_frame, 
            text="Editar Seleccionado", 
            command=self._on_editar, 
            bg="#28a745", 
            fg="white"
        ).pack(side="left", padx=5)
        
        tk.Button(
            btn_frame, 
            text="Cancelar", 
            command=self._on_cancelar
        ).pack(side="left", padx=5)
    
    def _on_editar(self):
        """Maneja la selección de un registro para editar."""
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning(
                "Sin selección", "Por favor, seleccione un registro de la lista."
            )
            return
        
        fila_num_str = self.tree.item(seleccion[0])["tags"][0]
        fila_num = int(fila_num_str)
        
        # Encontrar los datos completos de la fila seleccionada
        datos_completos = next(
            (datos for num, datos in self.registros if num == fila_num), None
        )
        
        if datos_completos:
            self.callback(fila_num, datos_completos)
            if self.ventana:
                self.ventana.destroy()
    
    def _on_cancelar(self):
        """Cancela la selección."""
        if self.ventana:
            self.ventana.destroy()


class VentanaSeleccionArchivo:
    """Ventana genérica para seleccionar un archivo de una lista."""
    
    def __init__(self, parent, titulo: str, archivos: List[str], callback: Callable[[str], None]):
        self.parent = parent
        self.titulo = titulo
        self.archivos = archivos
        self.callback = callback
        self.resultado = None
        self._crear_ventana()
    
    def _crear_ventana(self):
        """Crea la ventana de selección."""
        self.ventana = tk.Toplevel(self.parent)
        self.ventana.title(self.titulo)
        self.ventana.geometry("400x200")
        self.ventana.grab_set()
        
        # Centrar la ventana
        self.ventana.transient(self.parent)
        
        # Etiqueta
        tk.Label(self.ventana, text="Seleccione un archivo:").pack(padx=20, pady=10)
        
        # Combobox
        self.combo = ttk.Combobox(
            self.ventana, 
            values=self.archivos, 
            state="readonly", 
            width=40
        )
        self.combo.pack(padx=20, pady=5)
        
        if self.archivos:
            self.combo.current(0)
        
        # Botones
        btn_frame = tk.Frame(self.ventana)
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame, 
            text="Aceptar", 
            command=self._on_aceptar,
            bg="#4a90e2",
            fg="white"
        ).pack(side="left", padx=5)
        
        tk.Button(
            btn_frame, 
            text="Cancelar", 
            command=self._on_cancelar
        ).pack(side="left", padx=5)
        
        # Hacer que Enter funcione como Aceptar
        self.ventana.bind('<Return>', lambda e: self._on_aceptar())
        self.combo.focus_set()
    
    def _on_aceptar(self):
        """Procesa la selección."""
        seleccion = self.combo.get()
        if seleccion:
            self.callback(seleccion)
        self.ventana.destroy()
    
    def _on_cancelar(self):
        """Cancela la selección."""
        self.ventana.destroy()


class DialogoCrearArchivo:
    """Diálogo para crear un nuevo archivo."""
    
    def __init__(self, parent, callback: Callable[[str], None]):
        self.parent = parent
        self.callback = callback
        self._crear_dialogo()
    
    def _crear_dialogo(self):
        """Crea el diálogo."""
        self.ventana = tk.Toplevel(self.parent)
        self.ventana.title("Crear Nuevo Archivo")
        self.ventana.geometry("400x150")
        self.ventana.grab_set()
        self.ventana.transient(self.parent)
        
        # Etiqueta
        tk.Label(
            self.ventana, 
            text="Nombre para la copia (ej: mayo_2025):"
        ).pack(padx=20, pady=10)
        
        # Entry
        self.entry = tk.Entry(self.ventana, width=40)
        self.entry.pack(padx=20, pady=5)
        self.entry.focus_set()
        
        # Botones
        btn_frame = tk.Frame(self.ventana)
        btn_frame.pack(pady=20)
        
        tk.Button(
            btn_frame, 
            text="Crear", 
            command=self._on_crear,
            bg="#28a745",
            fg="white"
        ).pack(side="left", padx=5)
        
        tk.Button(
            btn_frame, 
            text="Cancelar", 
            command=self._on_cancelar
        ).pack(side="left", padx=5)
        
        # Hacer que Enter funcione como Crear
        self.ventana.bind('<Return>', lambda e: self._on_crear())
    
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
    def confirmar(parent, titulo: str, mensaje: str, callback_si: Callable[[], None], callback_no: Optional[Callable[[], None]] = None):
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
    # Obtener dimensiones de la pantalla
    ancho_pantalla = ventana.winfo_screenwidth()
    alto_pantalla = ventana.winfo_screenheight()
    
    # Calcular posición
    x = (ancho_pantalla - ancho) // 2
    y = (alto_pantalla - alto) // 2
    
    # Aplicar geometría
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")