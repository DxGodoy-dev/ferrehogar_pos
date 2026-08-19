from __future__ import annotations

from collections.abc import Callable
from typing import Any

import flet as ft

from ferrehogar_pos.core.schemas import ProductoDTO


class TablaBusqueda(ft.Container):
    """Componente de interfaz que maneja el diseño del buscador y sus resultados."""

    def __init__(
        self,
        on_busqueda_change: Callable[[Any], None],
        on_agregar_click: Callable[[ProductoDTO, bool], None],
    ) -> None:
        self.on_agregar_click = on_agregar_click

        # Lista vertical que contendrá las tarjetas de productos encontrados
        self.lista_resultados = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

        # Campo de entrada de texto interactivo
        self.input_buscar = ft.TextField(
            label="Buscar por código, nombre o alias...",
            prefix_icon=ft.Icons.SEARCH,
            on_change=on_busqueda_change,
            autofocus=True,
        )

        # Inicializamos el contenedor expandible ocupando su espacio correspondiente
        super().__init__(
            content=ft.Column(
                [
                    self.input_buscar,
                    ft.Text(
                        "Resultados de la búsqueda:",
                        weight=ft.FontWeight.BOLD,
                        size=14,
                    ),
                    self.lista_resultados,
                ],
                expand=True,
            ),
            expand=3,
        )

    def renderizar_resultados(self, lista_productos: list[ProductoDTO]) -> None:
        """Limpia y construye las tarjetas de productos en base a los DTOs recibidos."""
        self.lista_resultados.controls.clear()

        for prod in lista_productos:
            codigo_str = prod.codigo if prod.codigo else "S/C"

            card = ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(
                                title=ft.Text(prod.nombre),
                                subtitle=ft.Text(f"Código: {codigo_str} | Área: {prod.area}"),
                                trailing=ft.Text(f"${prod.precio_venta_usd:.2f}"),
                            ),
                            ft.Container(
                                height=50,
                                content=ft.Row(
                                    [
                                        ft.ElevatedButton(
                                            "Restar",
                                            icon=ft.Icons.REMOVE,
                                            on_click=lambda _, p=prod: self.on_agregar_click(
                                                p, decremento=True
                                            ),
                                        ),
                                        ft.ElevatedButton(
                                            "Sumar",
                                            icon=ft.Icons.ADD,
                                            on_click=lambda _, p=prod: self.on_agregar_click(
                                                p, decremento=False
                                            ),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.END,
                                ),
                            ),
                        ]
                    ),
                    padding=10,
                )
            )
            self.lista_resultados.controls.append(card)

        if self.page:
            self.update()