import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
from typing import Optional, Callable
from datetime import datetime

from .widgets import FormularioAudiencia, BotonesAccion, BotonesGestionArchivos
from .dialogs import (
    VentanaSeleccionRegistro, 
    VentanaSeleccionArchivo, 
    DialogoCrearArchivo,
    DialogoConfirmacion,
    centrar_ventana
)
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


class VentanaPrincipal:
    """Ventana principal de la aplicación."""
    
    def __init__(self):
        self.archivo_excel: Optional[str] = None
        self.excel_manager: Optional[ExcelManager] = None
        self.modo_edicion = False
        self.fila_editando: Optional[int] = None
        
        # Crear la ventana principal
        self.ventana = tb.Window(themename="flatly")
        self._configurar_ventana()
        self._crear_widgets()
        self._configurar_eventos()
        self._inicializar()
    
    def _configurar_ventana(self):
        """Configura las propiedades básicas de la ventana."""
        self.ventana.title("Ordenador de Audiencias")
        self.ventana.geometry("600x600")
        self.ventana.minsize(600, 600)
        self.ventana.maxsize(1200, 1080)
        self.ventana.resizable(True, True)
        
        # Intentar maximizar la ventana
        try:
            self.ventana.state("zoomed")
        except tk.TclError:
            self.ventana.attributes("-fullscreen", True)
        
        # Configurar grid
        for i in range(13):
            self.ventana.rowconfigure(i, weight=1)
        self.ventana.columnconfigure(1, weight=1)
        
        # Color de fondo
        self.ventana.configure(bg="#f7f7fa")
    
    def _crear_widgets(self):
        """Crea todos los widgets de la interfaz."""
        fuente = ("Segoe UI", 11)
        
        # Contador de registros
        self.contador_registros_label = ttk.Label(
            self.ventana, text="Registros: 0", font=("Segoe UI", 10, "bold")
        )
        self.contador_registros_label.grid(row=0, column=1, sticky="ne", padx=20, pady=5)
        
        # Formulario de audiencia
        self.formulario = FormularioAudiencia(self.ventana, fuente)
        
        # Botones de acción
        self.botones_accion = BotonesAccion(self.ventana, fuente)
        self.botones_accion.grid(row=9, column=0, columnspan=2, pady=20, padx=16, sticky="ew")
        
        # Botones de gestión de archivos
        self.botones_gestion = BotonesGestionArchivos(self.ventana)
        self.botones_gestion.grid(row=10, column=0, columnspan=2, pady=12, padx=16, sticky="ew")
        
        # Etiqueta de archivo actual
        self.archivo_actual_var = tk.StringVar(value="Ningún archivo seleccionado")
        self.label_archivo_actual = tk.Label(
            self.ventana,
            textvariable=self.archivo_actual_var,
            bg="#f7f7fa",
            font=("Segoe UI", 9, "italic"),
            fg="#555",
        )
        self.label_archivo_actual.grid(
            row=11, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12)
        )
        
        # Etiqueta de crédito
        label_credito = tk.Label(
            self.ventana,
            text="© 2025 - Hecho por Jose David Bustamante Sánchez",
            bg="#f7f7fa",
            font=("Segoe UI", 9, "italic"),
        )
        label_credito.grid(row=12, column=0, columnspan=2, pady=(0, 16))
    
    def _configurar_eventos(self):
        """Configura los eventos y comandos de los widgets."""
        # Configurar comandos de botones de acción
        self.botones_accion.configurar_comandos(
            self.guardar_datos,
            self.actualizar_registro,
            self.cancelar_edicion
        )
        
        # Configurar comandos de botones de gestión
        self.botones_gestion.configurar_comandos(
            self.crear_nueva_copia,
            self.seleccionar_archivo_trabajo,
            self.seleccionar_registro_para_editar,
            self.eliminar_archivo_trabajo,
            self.descargar_archivo_trabajo
        )
        
        # Configurar menú contextual
        self.formulario.agregar_menu_contextual()
    
    def _inicializar(self):
        """Inicialización final de la aplicación."""
        self.formulario.limpiar_campos()
        self.actualizar_contador_registros()
    
    # === Métodos de gestión de modo de edición ===
    
    def activar_modo_edicion(self):
        """Cambia la interfaz al modo de edición."""
        self.modo_edicion = True
        self.botones_accion.activar_modo_edicion()
        self.ventana.title("Ordenador de Audiencias - EDITANDO REGISTRO")
    
    def desactivar_modo_edicion(self):
        """Vuelve la interfaz al modo normal."""
        self.modo_edicion = False
        self.fila_editando = None
        self.botones_accion.desactivar_modo_edicion()
        self.ventana.title("Ordenador de Audiencias")
        self.formulario.limpiar_campos()
    
    # === Métodos de gestión de datos ===
    
    def guardar_datos(self):
        """Guarda un nuevo registro en el archivo Excel."""
        if not self.archivo_excel or not self.excel_manager:
            DialogoConfirmacion.mostrar_advertencia(
                self.ventana,
                "Sin Archivo", 
                "Por favor, seleccione un archivo de trabajo."
            )
            return
        
        datos = self.formulario.obtener_datos_formulario()
        valido, mensaje = validar_todos_los_datos(datos)
        
        if not valido:
            DialogoConfirmacion.mostrar_error(self.ventana, "Error de Validación", mensaje)
            return
        
        try:
            audiencia = Audiencia.from_form_data(datos)
            self.excel_manager.guardar_audiencia(audiencia)
            
            # Reordenar y actualizar
            num_registros, total_si, totales_motivos = self.excel_manager.reordenar_y_guardar()
            
            DialogoConfirmacion.mostrar_info(
                self.ventana,
                "Éxito", 
                "Registro guardado y ordenado correctamente."
            )
            
            self.formulario.limpiar_campos()
            self.actualizar_contador_registros()
            
        except Exception as e:
            DialogoConfirmacion.mostrar_error(
                self.ventana,
                "Error al Guardar", 
                f"No se pudo guardar el registro: {e}"
            )
    
    def actualizar_registro(self):
        """Actualiza una fila existente en el archivo Excel."""
        if not self.fila_editando:
            return
        
        if not self.archivo_excel or not self.excel_manager:
            DialogoConfirmacion.mostrar_error(
                self.ventana,
                "Error", 
                "No hay archivo seleccionado"
            )
            return
        
        datos = self.formulario.obtener_datos_formulario()
        valido, mensaje = validar_todos_los_datos(datos)
        
        if not valido:
            DialogoConfirmacion.mostrar_error(self.ventana, "Error de Validación", mensaje)
            return
        
        try:
            audiencia = Audiencia.from_form_data(datos)
            self.excel_manager.actualizar_audiencia(self.fila_editando, audiencia)
            
            # Reordenar y actualizar
            num_registros, total_si, totales_motivos = self.excel_manager.reordenar_y_guardar()
            
            DialogoConfirmacion.mostrar_info(
                self.ventana,
                "Éxito", 
                "Registro actualizado correctamente."
            )
            
            self.desactivar_modo_edicion()
            self.actualizar_contador_registros()
            
        except Exception as e:
            DialogoConfirmacion.mostrar_error(
                self.ventana,
                "Error al Actualizar", 
                f"No se pudo actualizar el registro: {e}"
            )
    
    def cancelar_edicion(self):
        """Cancela el modo de edición y revierte cambios no guardados."""
        DialogoConfirmacion.confirmar(
            self.ventana,
            "Cancelar Edición",
            "¿Seguro que desea cancelar? Se perderán los cambios no guardados.",
            self.desactivar_modo_edicion
        )
    
    # === Métodos de gestión de archivos ===
    
    def crear_nueva_copia(self):
        """Crea una nueva copia de la plantilla."""
        def callback_crear(nombre):
            try:
                crear_copia_plantilla(nombre)
                DialogoConfirmacion.mostrar_info(
                    self.ventana,
                    "Éxito", 
                    f"Archivo '{nombre}' creado."
                )
            except FileExistsError:
                DialogoConfirmacion.mostrar_error(
                    self.ventana,
                    "Error", 
                    "Ya existe un archivo con ese nombre."
                )
            except Exception as e:
                DialogoConfirmacion.mostrar_error(
                    self.ventana,
                    "Error", 
                    f"No se pudo crear el archivo: {e}"
                )
        
        DialogoCrearArchivo(self.ventana, callback_crear)
    
    def seleccionar_archivo_trabajo(self):
        """Selecciona un archivo de trabajo."""
        archivos = listar_archivos_creados()
        if not archivos:
            DialogoConfirmacion.mostrar_info(
                self.ventana,
                "Sin Archivos", 
                "No hay archivos de plantilla creados."
            )
            return
        
        def callback_seleccionar(nombre_archivo):
            try:
                self.archivo_excel = seleccionar_archivo(nombre_archivo)
                self.excel_manager = ExcelManager(self.archivo_excel)
                self.archivo_actual_var.set(f"Trabajando con: {nombre_archivo}")
                self.actualizar_contador_registros()
                DialogoConfirmacion.mostrar_info(
                    self.ventana,
                    "Archivo Seleccionado", 
                    f"Ahora trabajando con: {nombre_archivo}"
                )
            except Exception as e:
                DialogoConfirmacion.mostrar_error(
                    self.ventana,
                    "Error", 
                    f"No se pudo seleccionar el archivo: {e}"
                )
        
        VentanaSeleccionArchivo(
            self.ventana,
            "Seleccionar Archivo de Trabajo",
            archivos,
            callback_seleccionar
        )
    
    def seleccionar_registro_para_editar(self):
        """Abre una ventana para que el usuario elija qué registro editar."""
        if not self.archivo_excel or not self.excel_manager:
            DialogoConfirmacion.mostrar_advertencia(
                self.ventana,
                "Sin Archivo", 
                "Primero debe seleccionar un archivo."
            )
            return
        
        try:
            registros = self.excel_manager.leer_registros()
            
            if not registros:
                DialogoConfirmacion.mostrar_info(
                    self.ventana,
                    "Vacío", 
                    "No hay registros para editar en el archivo."
                )
                return
            
            def callback_editar(fila_num, datos_completos):
                self.fila_editando = fila_num
                self.formulario.cargar_datos_para_edicion(datos_completos)
                self.activar_modo_edicion()
            
            VentanaSeleccionRegistro(self.ventana, registros, callback_editar)
            
        except Exception as e:
            DialogoConfirmacion.mostrar_error(
                self.ventana,
                "Error de Lectura", 
                f"No se pudieron leer los registros: {e}"
            )
    
    def eliminar_archivo_trabajo(self):
        """Elimina un archivo de trabajo."""
        archivos = listar_archivos_creados()
        if not archivos:
            return
        
        def callback_seleccionar(nombre_archivo):
            DialogoConfirmacion.confirmar(
                self.ventana,
                "Confirmar",
                f"¿Seguro que quiere eliminar '{nombre_archivo}'?",
                lambda: self._ejecutar_eliminacion(nombre_archivo)
            )
        
        VentanaSeleccionArchivo(
            self.ventana,
            "Eliminar Archivo",
            archivos,
            callback_seleccionar
        )
    
    def _ejecutar_eliminacion(self, nombre_archivo):
        """Ejecuta la eliminación del archivo."""
        try:
            eliminar_archivo(nombre_archivo)
            DialogoConfirmacion.mostrar_info(
                self.ventana,
                "Eliminado", 
                f"Archivo '{nombre_archivo}' eliminado."
            )
            
            # Si era el archivo actual, limpiar la selección
            if self.archivo_excel and self.archivo_excel.endswith(nombre_archivo):
                self.archivo_excel = None
                self.excel_manager = None
                self.archivo_actual_var.set("Ningún archivo seleccionado")
                self.actualizar_contador_registros()
                
        except Exception as e:
            DialogoConfirmacion.mostrar_error(
                self.ventana,
                "Error", 
                f"No se pudo eliminar el archivo: {e}"
            )
    
    def descargar_archivo_trabajo(self):
        """Descarga un archivo de trabajo."""
        archivos = listar_archivos_creados()
        if not archivos:
            return
        
        def callback_seleccionar(nombre_archivo):
            try:
                destino = descargar_archivo(nombre_archivo)
                if destino:
                    DialogoConfirmacion.mostrar_info(
                        self.ventana,
                        "Descargado", 
                        f"Archivo guardado en:\n{destino}"
                    )
            except Exception as e:
                DialogoConfirmacion.mostrar_error(
                    self.ventana,
                    "Error", 
                    f"No se pudo descargar el archivo: {e}"
                )
        
        VentanaSeleccionArchivo(
            self.ventana,
            "Descargar Archivo",
            archivos,
            callback_seleccionar
        )
    
    # === Métodos auxiliares ===
    
    def actualizar_contador_registros(self):
        """Actualiza la etiqueta del contador de registros en la GUI."""
        if not self.excel_manager:
            self.contador_registros_label.config(text="Registros: 0")
            return
        
        try:
            num_registros = self.excel_manager.contar_registros()
            self.contador_registros_label.config(text=f"Registros: {num_registros}")
        except Exception:
            self.contador_registros_label.config(text="Registros: ?")
    
    def ejecutar(self):
        """Ejecuta el bucle principal de la aplicación."""
        self.ventana.mainloop()