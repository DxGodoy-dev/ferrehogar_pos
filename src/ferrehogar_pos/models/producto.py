from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ferrehogar_pos.core.database import Base


class ProductoAliasDB(Base):
    """Modelo que almacena los aliases individuales de un producto para búsquedas eficientes."""

    __tablename__ = "producto_aliases"

    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(
        Integer,
        ForeignKey("productos.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    alias = Column(String(100), nullable=False, index=True)

    # Relación inversa hacia el producto
    producto = relationship("ProductoDB", back_populates="aliases_rel")


class ProductoDB(Base):
    """Modelo relacional principal que define la estructura física de la tabla productos."""

    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(50), unique=True, nullable=True, index=True)
    nombre = Column(String(150), nullable=False, index=True)
    area = Column(String(50), default="General", index=True)
    precio_venta_usd = Column(Float, nullable=False)
    precio_compra_usd = Column(Float, nullable=False)
    ultima_actualizacion = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relación uno-a-muchos con borrado en cascada
    aliases_rel = relationship(
        "ProductoAliasDB",
        back_populates="producto",
        cascade="all, delete-orphan",
        lazy="selectinload",
    )