import flet as ft

class BannerTasa(ft.Row):
    """Componente puramente visual que renderiza el encabezado de la tasa del POS."""
    def __init__(self):
        # Inicializamos los textos con estilos base limpios
        self.txt_titulo = ft.Text(
            "FerreHogar POS - Mostrador", 
            size=22, 
            weight=ft.FontWeight.BOLD
        )
        self.txt_info_tasa = ft.Text(
            "Tasa BCV: Cargando...", 
            size=14, 
            weight=ft.FontWeight.W_500
        )
        
        # Pasamos los controles al inicializador del Row nativo de Flet
        super().__init__(
            controls=[self.txt_titulo, self.txt_info_tasa],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        )

    def actualizar_tasa(self, valor_tasa: float, fecha_tasa: str):
        """Método expuesto para que el mediador actualice los textos externamente."""
        self.txt_info_tasa.value = f"Tasa BCV: {valor_tasa:.2f} VES/USD ({fecha_tasa})"
        # Nota: No llamamos a self.update() aquí para dejar que la página principal controle el render