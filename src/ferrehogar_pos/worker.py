from __future__ import annotations

import flet as ft

from ferrehogar_pos.controllers.pos_controller import POSController
from ferrehogar_pos.core.database import init_db
from ferrehogar_pos.views.search_view import main_app


def start_session(page: ft.Page) -> None:
    """Inicializa un controlador aislado por cada sesión/pestaña de usuario."""
    controller = POSController()
    main_app(page, controller)


def run_worker() -> None:
    """Punto de entrada del subproceso servidor para Flet Web."""
    init_db()
    ft.app(
        target=start_session,
        view=ft.AppView.WEB_BROWSER,
    )


if __name__ == "__main__":
    run_worker()