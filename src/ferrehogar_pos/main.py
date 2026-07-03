import flet as ft
# Ajustamos la importación para que sea absoluta desde la raíz src
from ferrehogar_pos.core.database import init_db
from ferrehogar_pos.views.search_view import main_app
from ferrehogar_pos.controllers.pos_controller import POSController

def ejecutar_pos():
    """Punto de entrada principal para lanzar el POS."""
    # 1. Preparar infraestructura (Atómico)
    init_db()

    controller = POSController()
    
    ft.app(
        target=lambda page: main_app(page, controller),
        view=ft.AppView.WEB_BROWSER
    )

if __name__ == "__main__":
    ejecutar_pos()