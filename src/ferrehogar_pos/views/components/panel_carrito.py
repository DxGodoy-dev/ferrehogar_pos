from __future__ import annotations

from collections.abc import Callable
from typing import Any

import flet as ft

from ferrehogar_pos.schemas.producto import ProductoDTO
from ferrehogar_pos.views.widgets.empty_state import crear_estado_vacio
from ferrehogar_pos.views.widgets.quantity_selector import crear_selector_cantidad
from ferrehogar_pos.views.widgets.summary_card import crear_tarjeta_resumen


def crear_panel_carrito(
    carrito: dict[int, dict[str, Any]],
    totales: dict[str, float | int],
    on_incrementar: Callable[[ProductoDTO], None],
    on_decrementar: Callable[[ProductoDTO], None],
    on_limpiar: Callable[[], None],
    on_cobrar: Callable[[], None],
) -> ft.Container:
    """Construye el panel lateral derecho correspondiente al carrito componiendo widgets atómicos."""
    esta_vacio = len(carrito) == 0

    if esta_vacio:
        cuerpo_control: ft.Control = crear_estado_vacio(
            icono=ft.Icons.SHOPPING_CART_OUTLINED,
            mensaje="El carrito está vacío",
            submensaje="Seleccione productos del catálogo para comenzar",
        )
    else:
        filas_items: list[ft.Control] = []
        for item in carrito.values():
            prod: ProductoDTO = item["producto"]
            cant: int = item["cantidad"]
            subtotal_usd = prod.precio_venta_usd * cant

            fila = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Column(
                            controls=[
                                ft.Text(
                                    prod.nombre,
                                    size=13,
                                    weight=ft.FontWeight.BOLD,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                                ft.Text(
                                    f"${prod.precio_venta_usd:.2f} c/u",
                                    size=11,
                                    color=ft.Colors.GREY_600,
                                ),
                            ],
                            expand=True,
                            spacing=2,
                        ),
                        crear_selector_cantidad(
                            cantidad=cant,
                            on_incrementar=lambda p=prod: on_incrementar(p),
                            on_decrementar=lambda p=prod: on_decrementar(p),
                        ),
                        ft.Text(
                            f"${subtotal_usd:.2f}",
                            size=13,
                            weight=ft.FontWeight.BOLD,
                            text_align=ft.TextAlign.RIGHT,
                            width=65,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.padding.symmetric(vertical=6, horizontal=8),
                border=ft.border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_200)),
            )
            filas_items.append(fila)

        cuerpo_control = ft.ListView(
            controls=filas_items,
            expand=True,
            spacing=2,
        )

    tarjeta_resumen = crear_tarjeta_resumen(
        total_usd=float(totales.get("total_usd", 0.0)),
        total_ves=int(totales.get("total_ves", 0)),
        on_limpiar=on_limpiar,
        on_cobrar=on_cobrar,
        deshabilitado=esta_vacio,
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.SHOPPING_BAG, color=ft.Colors.BLUE_GREY_700),
                        ft.Text(
                            "Resumen de Venta",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_GREY_800,
                        ),
                    ],
                    spacing=8,
                ),
                ft.Divider(height=10, thickness=1),
                cuerpo_control,
                tarjeta_resumen,
            ],
            expand=True,
            spacing=10,
        ),
        padding=12,
        bgcolor=ft.Colors.WHITE,
        border_radius=8,
        border=ft.border.all(1, ft.Colors.GREY_300),
        expand=True,
    )