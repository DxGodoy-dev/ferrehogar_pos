from __future__ import annotations

from typing import Any

from ferrehogar_pos.core.helpers import calcular_monto_ves, redondear_usd
from ferrehogar_pos.schemas.producto import ProductoDTO
from ferrehogar_pos.schemas.venta import DetalleVentaCrear


class CarritoService:
    """Servicio de dominio encargado de gestionar el estado y operaciones del carrito."""

    def __init__(self) -> None:
        self._items: dict[int, dict[str, Any]] = {}

    @property
    def items(self) -> dict[int, dict[str, Any]]:
        """Retorna los ítems actualmente contenidos en el carrito."""
        return self._items

    @property
    def esta_vacio(self) -> bool:
        """Indica si el carrito no tiene ningún producto cargado."""
        return len(self._items) == 0

    def agregar_o_incrementar(
        self, producto: ProductoDTO, cantidad: int = 1
    ) -> None:
        """Añade un producto al carrito o incrementa su cantidad existente."""
        if cantidad <= 0:
            return

        prod_id = producto.id
        if prod_id in self._items:
            self._items[prod_id]["cantidad"] += cantidad
        else:
            self._items[prod_id] = {
                "producto": producto,
                "cantidad": cantidad,
            }

    def decrementar_o_eliminar(
        self, producto_id: int, cantidad: int = 1
    ) -> None:
        """Decrementa la cantidad de un ítem y lo elimina si llega a cero."""
        if producto_id not in self._items or cantidad <= 0:
            return

        self._items[producto_id]["cantidad"] -= cantidad
        if self._items[producto_id]["cantidad"] <= 0:
            del self._items[producto_id]

    def limpiar(self) -> None:
        """Vacía completamente el contenido del carrito."""
        self._items.clear()

    def calcular_totales(self, tasa_bcv: float | None) -> dict[str, float | int]:
        """Calcula el total en USD y el total en VES redondeado al entero superior."""
        subtotales = [
            item["producto"].precio_venta_usd * item["cantidad"]
            for item in self._items.values()
        ]
        total_usd = redondear_usd(sum(subtotales))
        total_ves = calcular_monto_ves(total_usd, tasa_bcv)

        return {
            "total_usd": total_usd,
            "total_ves": total_ves,
        }

    def generar_detalles_payload(self) -> list[DetalleVentaCrear]:
        """Convierte los ítems del carrito en una lista de esquemas DetalleVentaCrear."""
        detalles: list[DetalleVentaCrear] = []
        for item in self._items.values():
            prod: ProductoDTO = item["producto"]
            cant: int = item["cantidad"]
            subtotal = redondear_usd(prod.precio_venta_usd * cant)

            detalles.append(
                DetalleVentaCrear(
                    producto_id=prod.id,
                    nombre_producto_historico=prod.nombre,
                    cantidad=cant,
                    precio_unitario_usd=prod.precio_venta_usd,
                    subtotal_usd=subtotal,
                )
            )
        return detalles