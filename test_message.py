import flet as ft

def main(page: ft.Page):
    page.title = "Test de Mensajes"
    
    def mostrar_mensaje(mensaje):
        """Muestra un mensaje usando AlertDialog."""
        print(f"=== DEBUG: Llamado _mostrar_mensaje con: {mensaje} ===")
        
        def cerrar_mensaje(e):
            dlg.open = False
            page.update()
        
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Información", size=16, weight=ft.FontWeight.BOLD, color="#1E40AF"),
            content=ft.Text(mensaje, size=14, color="#374151"),
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
        print("=== DEBUG: Mensaje mostrado ===")
    
    def test_mensaje(e):
        mostrar_mensaje("Primero debe seleccionar un archivo")
    
    # Crear botón de prueba
    btn_test = ft.ElevatedButton(
        "Probar Mensaje de Validación",
        on_click=test_mensaje,
        width=300,
        height=50,
    )
    
    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("Prueba de Sistema de Mensajes", size=20, weight=ft.FontWeight.BOLD),
                ft.Container(height=20),
                btn_test,
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=50,
            alignment=ft.alignment.center,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)
