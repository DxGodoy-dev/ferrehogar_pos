from __future__ import annotations

import flet as ft

from ferrehogar_pos.controllers.pos_controller import POSController
from ferrehogar_pos.core.schemas import ProductoDTO

from .components.banner_tasa import BannerTasa
from .components.panel_carrito import PanelCarrito
from .components.tabla_busqueda import TablaBusqueda


def main_app(page: ft.Page, controller: POSController) -> None:
    """Mediador que ensambla los componentes y gestiona la lógica de flujo."""
    page.title = "FerreHogar POS"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20

    # Funciones de lógica de negocio (Callbacks)
    def on_busqueda_change(e: ft.ControlEvent) -> None:
        termino = e.control.value.strip()
        if len(termino) >= 2:
            resultados = controller.buscar_productos(termino)
            componente_busqueda.renderizar_resultados(resultados)
        else:
            componente_busqueda.renderizar_resultados([])

    def on_agregar_producto(producto: ProductoDTO, decremento: bool = False) -> None:
        controller.gestionar_cantidad(producto, decremento=decremento)
        refrescar_ui()

    def on_limpiar_venta(e: ft.ControlEvent) -> None:
        controller.limpiar_carrito()
        refrescar_ui()

    def refrescar_ui() -> None:
        totales = controller.calcular_totales()
        componente_carrito.actualizar_interfaz_carrito(
            controller.carrito,
            totales["total_usd"],
            totales["total_ves"],
        )
        componente_banner.actualizar_tasa(
            controller.obtener_tasa_actual(),
            controller.fecha_actualizacion_tasa,
        )
        page.update()

    # Instanciación única de componentes modulares
    componente_banner = BannerTasa()
    componente_busqueda = TablaBusqueda(on_busqueda_change, on_agregar_producto)
    componente_carrito = PanelCarrito(on_limpiar_venta)

    # Layout final
    page.add(
        componente_banner,
        ft.Divider(),
        ft.Row(
            [
                componente_busqueda,
                ft.VerticalDivider(),
                componente_carrito,
            ],
            expand=True,
        ),
    )

    # Carga inicial del estado
    refrescar_ui()