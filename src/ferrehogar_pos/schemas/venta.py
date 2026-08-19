from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DetalleVentaBase(BaseModel):
    """Esquema base para un ítem individual de una venta."""

    producto_id: int | None = None
    nombre_producto_historico: str = Field(..., min_length=1, max_length=150)
    cantidad: int = Field(..., gt=0)
    precio_unitario_usd: float = Field(..., ge=0.0)
    subtotal_usd: float = Field(..., ge=0.0)


class DetalleVentaCrear(DetalleVentaBase):
    """Payload de entrada para registrar una línea de detalle."""

    pass


class DetalleVentaDTO(DetalleVentaBase):
    """DTO inmutable de lectura para una línea de detalle persistida."""

    id: int

    model_config = ConfigDict(from_attributes=True)


class VentaBase(BaseModel):
    """Esquema base para la cabecera de la transacción de venta."""

    tasa_bcv_aplicada: float = Field(..., gt=0.0)
    tasa_fecha_referencia: str = Field(default="No disponible", max_length=100)
    total_usd: float = Field(..., ge=0.0)
    total_ves: int = Field(..., ge=0)


class VentaCrear(VentaBase):
    """Payload de entrada para procesar una venta completa con sus ítems."""

    detalles: list[DetalleVentaCrear] = Field(..., min_length=1)


class VentaDTO(VentaBase):
    """DTO inmutable de lectura que representa una venta persistida con sus ítems."""

    id: int
    fecha_utc: datetime
    detalles: list[DetalleVentaDTO] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)