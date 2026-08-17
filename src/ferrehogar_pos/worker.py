import flet as ft

from ferrehogar_pos.controllers.pos_controller import POSController
from ferrehogar_pos.core.database import init_db
from ferrehogar_pos.views.search_view import main_app


def run_worker() -> None:
    init_db()
    controller = POSController()
    ft.app(
        target=lambda page: main_app(page, controller),
        view=ft.AppView.WEB_BROWSER,
    )


if __name__ == "__main__":
    run_worker()
