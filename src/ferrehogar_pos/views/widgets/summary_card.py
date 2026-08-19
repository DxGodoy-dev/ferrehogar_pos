from __future__ import annotations

from collections.abc import Callable

import flet as ft


def crear_tarjeta_resumen(
    total_usd: float,
    total_ves: int,
    on_limpiar: Callable[[], None],
    on_cobrar: Callable[[], None],
    deshabilitado: bool = False,
) -> ft.Container:
    """Construye una tarjeta visual con el desglose de totales (USD / VES) y botones de acción.

    Args:
        total_usd (float): Monto total expresado en dólares.
        total_ves (int): Monto total expresado en bolívares (entero redondeado).
        on_limpiar (Callable[[], None]): Callback para resetear o vaciar la orden actual.
        on_cobrar (Callable[[], None]): Callback para iniciar la persistencia/cobro.
        deshabilitado (bool): Bandera para bloquear la interactividad de los botones.

    Returns:
        ft.Container: Tarjeta formateada con montos y botones de confirmación.
    """
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text("Total USD:", size=14, color=ft.Colors.GREY_700),
                        ft.Text(
                            f"${total_usd:.2f}",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.GREEN_800,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Row(
                    controls=[
                        ft.Text("Total Bs (BCV):", size=14, color=ft.Colors.GREY_700),
                        ft.Text(
                            f"{total_ves:,} Bs",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_900,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                ft.Divider(height=15, thickness=1),
                ft.Row(
                    controls=[
                        ft.OutlinedButton(
                            text="Limpiar",
                            icon=ft.Icons.DELETE_OUTLINE,
                            icon_color=ft.Colors.RED_400,
                            disabled=deshabilitado,
                            on_click=lambda _: on_limpiar(),
                        ),
                        ft.ElevatedButton(
                            text="Cobrar",
                            icon=ft.Icons.CHECK_CIRCLE_OUTLINE,
                            bgcolor=ft.Colors.GREEN_600,
                            color=ft.Colors.WHITE,
                            disabled=deshabilitado,
                            on_click=lambda _: on_cobrar(),
                            expand=True,
                        ),
                    ],
                    spacing=10,
                ),
            ],
            spacing=6,
        ),
        padding=12,
        bgcolor=ft.Colors.GREY_100,
        border_radius=8,
    )