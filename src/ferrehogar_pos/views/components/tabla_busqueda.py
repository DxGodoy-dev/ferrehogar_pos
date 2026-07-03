import flet as ft

class TablaBusqueda(ft.Container):
    """Componente de interfaz que maneja el diseño del buscador y sus resultados."""
    def __init__(self, on_busqueda_change, on_agregar_click):
        self.on_agregar_click = on_agregar_click  # Guardamos el callback para usarlo al renderizar
        
        # Lista vertical que contendrá las tarjetas de productos encontrados
        self.lista_resultados = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        
        # Campo de entrada de texto interactivo
        self.input_buscar = ft.TextField(
            label="Buscar por código, nombre o alias...",
            prefix_icon="search",
            on_change=on_busqueda_change,
            autofocus=True
        )
        
        # Inicializamos el contenedor expandible ocupando su espacio correspondiente
        super().__init__(
            content=ft.Column([
                self.input_buscar,
                ft.Text("Resultados de la búsqueda:", weight=ft.FontWeight.BOLD, size=14),
                self.lista_resultados
            ], expand=True),
            expand=3
        )

    def renderizar_resultados(self, lista_productos: list):
        self.lista_resultados.controls.clear()
        
        for prod in lista_productos:
            # Creamos la card
            card = ft.Card(
                content=ft.Container(
                    content=ft.Column([
                        ft.ListTile(
                            title=ft.Text(prod.nombre),
                            subtitle=ft.Text(f"Código: {prod.codigo} | Área: {prod.area}"),
                            trailing=ft.Text(f"${prod.precio_venta_usd:.2f}")
                        ),
                        # Forzamos un contenedor con altura para los botones
                        ft.Container(
                            height=50, 
                            content=ft.Row([
                                ft.ElevatedButton("Restar", icon="remove", on_click=lambda _, p=prod: self.on_agregar_click(p, decremento=True)),
                                ft.ElevatedButton("Sumar", icon="add", on_click=lambda _, p=prod: self.on_agregar_click(p, decremento=False))
                            ], alignment=ft.MainAxisAlignment.END)
                        )
                    ]),
                    padding=10
                )
            )
            self.lista_resultados.controls.append(card)
        
        self.lista_resultados.update()
        self.update()