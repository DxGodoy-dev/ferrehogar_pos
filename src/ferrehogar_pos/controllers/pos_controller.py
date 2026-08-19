from __future__ import annotations

from typing import Any

from ferrehogar_pos.core.exchange import ExchangeRateProvider
from ferrehogar_pos.core.logger import logger
from ferrehogar_pos.crud.crud_producto import (
    buscar_productos_por_termino,
    obtener_session,
)
from ferrehogar_pos.crud.crud_venta import registrar_venta
from ferrehogar_pos.schemas.producto import ProductoDTO
from ferrehogar_pos.schemas.venta import VentaCrear, VentaDTO
from ferrehogar_pos.services.carrito_service import CarritoService


class POSController:
    """Controlador ligero que orquesta los servicios de carrito, tasa y persistencia."""

    def __init__(self) -> None:
        self.tasa_service = ExchangeRateProvider()
        self.carrito_service = CarritoService()

        # Sincronización inicial de la tasa oficial
        self.tasa_service.fetch_bcv_rate()

    @property
    def carrito(self) -> dict[int, dict[str, Any]]:
        """Expone los ítems del carrito para compatibilidad directa con los componentes de la vista."""
        return self.carrito_service.items

    def buscar_productos(self, termino: str) -> list[ProductoDTO]:
        """Ejecuta una búsqueda de productos en la base de datos local."""
        with obtener_session() as db:
            return buscar_productos_por_termino(db, termino)

    def gestionar_cantidad(
        self, producto: ProductoDTO, decremento: bool = False
    ) -> None:
        """Añade, incrementa o decrementa la cantidad de un producto en el carrito."""
        if not decremento:
            self.carrito_service.agregar_o_incrementar(producto, cantidad=1)
        else:
            self.carrito_service.decrementar_o_eliminar(producto.id, cantidad=1)

    def limpiar_carrito(self) -> None:
        """Vacía todos los artículos del carrito."""
        self.carrito_service.limpiar()

    def obtener_tasa_actual(self) -> float | None:
        """Retorna el valor numérico de la tasa de cambio activa."""
        return self.tasa_service.current_rate

    @property
    def fecha_actualizacion_tasa(self) -> str | None:
        """Retorna el metadato de fecha de la tasa BCV activa."""
        return self.tasa_service.last_update

    def calcular_totales(self) -> dict[str, float | int]:
        """Calcula los totales en USD y VES delegando en el servicio de carrito."""
        tasa = self.obtener_tasa_actual()
        return self.carrito_service.calcular_totales(tasa_bcv=tasa)

    def procesar_venta(self) -> VentaDTO:
        """Valida, registra la transacción en base de datos y vacía el carrito.

        Raises:
            ValueError: Si el carrito está vacío o si no hay una tasa válida.
        """
        if self.carrito_service.esta_vacio:
            raise ValueError(
                "El carrito está vacío. Agregue productos antes de cobrar."
            )

        tasa = self.obtener_tasa_actual()
        if not tasa or tasa <= 0:
            raise ValueError(
                "No hay una tasa de cambio válida establecida para procesar la transacción."
            )

        totales = self.calcular_totales()
        fecha_ref = self.fecha_actualizacion_tasa or "No disponible"
        detalles = self.carrito_service.generar_detalles_payload()

        venta_payload = VentaCrear(
            tasa_bcv_aplicada=tasa,
            tasa_fecha_referencia=fecha_ref,
            total_usd=float(totales["total_usd"]),
            total_ves=int(totales["total_ves"]),
            detalles=detalles,
        )

        with obtener_session() as db:
            venta_registrada = registrar_venta(db, venta_payload)

        logger.info(
            f"Venta #{venta_registrada.id} procesada exitosamente: "
            f"${venta_registrada.total_usd:.2f} USD ({venta_registrada.total_ves} VES)"
        )

        self.carrito_service.limpiar()
        return venta_registrada