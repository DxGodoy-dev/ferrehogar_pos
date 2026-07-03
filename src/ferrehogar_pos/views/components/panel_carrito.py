import flet as ft

class PanelCarrito(ft.Container):
    """Componente de interfaz que encapsula el diseño del carrito de compras y los totales."""
    def __init__(self, on_limpiar_click):
        # Lista vertical interna para ir renderizando los productos agregados
        self.lista_items = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        
        # Textos de totales con estilos legibles para el mostrador
        self.txt_subtotal_usd = ft.Text("$0.00", size=18, weight=ft.FontWeight.W_500)
        self.txt_total_ves = ft.Text("0 VES", size=32, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_700)
        
        # Botón para vaciar la transacción, invocando el callback externo
        self.btn_limpiar = ft.ElevatedButton(
            "Limpiar Venta",
            icon="delete_outline",
            on_click=on_limpiar_click,
            style=ft.ButtonStyle(color=ft.Colors.RED_700)
        )
        
        # Construimos el contenedor con su diseño de fondo y padding
        super().__init__(
            content=ft.Column([
                ft.Text("Detalle de la Cuenta:", weight=ft.FontWeight.BOLD, size=16),
                ft.Divider(),
                self.lista_items,
                ft.Divider(),
                ft.Row([ft.Text("Subtotal USD:"), self.txt_subtotal_usd], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([ft.Text("TOTAL VES:"), self.txt_total_ves], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Container(expand=True),
                self.btn_limpiar
            ], expand=True),
            expand=2,
            padding=15,
            bgcolor=ft.Colors.GREY_50,
            border_radius=8
        )

    def actualizar_interfaz_carrito(self, items_carrito: dict, total_usd: float, total_ves: int):
        """Método expuesto para re-renderizar los montos y productos desde el mediador."""
        self.txt_subtotal_usd.value = f"${total_usd:.2f}"
        self.txt_total_ves.value = f"{total_ves} VES"
        
        # Limpiamos visualmente las filas anteriores y agregamos el estado actual
        self.lista_items.controls.clear()
        for item_id, datos in items_carrito.items():
            prod = datos["producto"]
            cant = datos["cantidad"]
            sub_usd = prod.precio_venta_usd * cant
            
            self.lista_items.controls.append(
                ft.ListTile(
                    title=ft.Text(prod.nombre, max_lines=1),
                    subtitle=ft.Text(f"{cant} x ${prod.precio_venta_usd:.2f}"),
                    trailing=ft.Text(f"${sub_usd:.2f}", weight=ft.FontWeight.BOLD)
                )
            )