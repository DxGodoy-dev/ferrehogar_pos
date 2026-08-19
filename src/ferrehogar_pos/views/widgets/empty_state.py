from __future__ import annotations

import flet as ft


def crear_estado_vacio(
    icono: str = ft.Icons.INBOX_OUTLINED,
    mensaje: str = "No hay elementos disponibles",
    submensaje: str | None = None,
) -> ft.Container:
    """Construye un contenedor visual estandarizado para estados sin datos.

    Args:
        icono (str): Nombre del icono del catálogo de ft.Icons.
        mensaje (str): Título principal descriptivo.
        submensaje (str | None): Detalle secundario opcional con instrucciones.

    Returns:
        ft.Container: Componente visual centrado y estilizado.
    """
    controles: list[ft.Control] = [
        ft.Icon(icono, size=44, color=ft.Colors.GREY_400),
        ft.Text(
            mensaje,
            size=14,
            color=ft.Colors.GREY_600,
            weight=ft.FontWeight.W_500,
            text_align=ft.TextAlign.CENTER,
        ),
    ]

    if submensaje:
        controles.append(
            ft.Text(
                submensaje,
                size=12,
                color=ft.Colors.GREY_500,
                text_align=ft.TextAlign.CENTER,
            )
        )

    return ft.Container(
        content=ft.Column(
            controls=controles,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=4,
        ),
        padding=ft.padding.symmetric(vertical=30, horizontal=15),
        alignment=ft.alignment.center,
    )