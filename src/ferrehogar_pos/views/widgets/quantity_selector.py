from __future__ import annotations

from collections.abc import Callable

import flet as ft


def crear_selector_cantidad(
    cantidad: int,
    on_incrementar: Callable[[], None],
    on_decrementar: Callable[[], None],
) -> ft.Row:
    """Construye un control compacto con botones de incremento/decremento y visor numérico.

    Args:
        cantidad (int): Valor numérico actual a mostrar.
        on_incrementar (Callable[[], None]): Callback ejecutado al presionar el botón de sumar.
        on_decrementar (Callable[[], None]): Callback ejecutado al presionar el botón de restar.

    Returns:
        ft.Row: Fila alineada con los controles de ajuste de cantidad.
    """
    return ft.Row(
        controls=[
            ft.IconButton(
                icon=ft.Icons.REMOVE_CIRCLE_OUTLINE,
                icon_size=18,
                icon_color=ft.Colors.RED_400,
                tooltip="Disminuir",
                on_click=lambda _: on_decrementar(),
            ),
            ft.Text(
                str(cantidad),
                size=13,
                weight=ft.FontWeight.BOLD,
            ),
            ft.IconButton(
                icon=ft.Icons.ADD_CIRCLE_OUTLINE,
                icon_size=18,
                icon_color=ft.Colors.GREEN_600,
                tooltip="Aumentar",
                on_click=lambda _: on_incrementar(),
            ),
        ],
        spacing=0,
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )