import flet as ft

def main(page: ft.Page):
    page.title = "Test de Diálogos"
    page.padding = 20
    
    def test_crear_archivo(e):
        from gui.main_window import DialogoCrearArchivo
        
        def callback(nombre):
            resultado.value = f"Archivo a crear: {nombre}"
            page.update()
        
        DialogoCrearArchivo(page, callback)
    
    def test_mensaje(e):
        def cerrar_mensaje(e):
            dlg.open = False
            page.update()
        
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Información", size=18, weight=ft.FontWeight.BOLD),
            content=ft.Text("Este es un mensaje de prueba", size=14, color="#374151"),
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
        
        page.overlay.append(dlg)
        dlg.open = True
        page.update()
    
    resultado = ft.Text("Esperando interacción...", size=16)
    
    page.add(
        ft.Column([
            ft.Text("Test de Diálogos Flet", size=24, weight=ft.FontWeight.BOLD),
            ft.Container(height=20),
            ft.ElevatedButton("Probar Crear Archivo", on_click=test_crear_archivo),
            ft.ElevatedButton("Probar Mensaje", on_click=test_mensaje),
            ft.Container(height=20),
            resultado,
        ])
    )

if __name__ == "__main__":
    ft.app(target=main)
