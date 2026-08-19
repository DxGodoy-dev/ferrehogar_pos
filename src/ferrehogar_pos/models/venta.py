from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ferrehogar_pos.core.database import Base


class VentaDB(Base):
    """Modelo de cabecera que registra una transacción de venta completada."""

    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha_utc = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        index=True,
    )
    tasa_bcv_aplicada = Column(Float, nullable=False)
    tasa_fecha_referencia = Column(String(100), default="No disponible", nullable=False)
    total_usd = Column(Float, nullable=False)
    total_ves = Column(Integer, nullable=False)

    # Relación con el desglose de productos vendidos
    detalles_rel = relationship(
        "DetalleVentaDB",
        back_populates="venta",
        cascade="all, delete-orphan",
        lazy="selectinload",
    )


class DetalleVentaDB(Base):
    """Modelo que almacena cada ítem individual dentro de una venta."""

    __tablename__ = "detalle_ventas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    venta_id = Column(
        Integer,
        ForeignKey("ventas.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    producto_id = Column(
        Integer,
        ForeignKey("productos.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    nombre_producto_historico = Column(String(150), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario_usd = Column(Float, nullable=False)
    subtotal_usd = Column(Float, nullable=False)

    # Relaciones relacionales hacia la cabecera y hacia el catálogo
    venta = relationship("VentaDB", back_populates="detalles_rel")
    producto = relationship("ProductoDB")