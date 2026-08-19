from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductoBase(BaseModel):
    """Esquema base con las especificaciones del producto en el catálogo."""

    codigo: str | None = Field(default=None, max_length=50)
    nombre: str = Field(..., min_length=3, max_length=150)
    aliases: list[str] = Field(default_factory=list)
    area: str = Field(default="General", max_length=50)
    precio_venta_usd: float = Field(..., gt=0.0)
    precio_compra_usd: float = Field(default=0.0, ge=0.0)

    @field_validator("nombre")
    @classmethod
    def limpiar_nombre(cls, v: str) -> str:
        """Normaliza el nombre eliminando espacios redundantes."""
        return " ".join(v.split()).strip()

    @field_validator("aliases", mode="before")
    @classmethod
    def normalizar_aliases(cls, v: object) -> list[str]:
        """Asegura que los aliases sean una lista de cadenas limpias en minúsculas."""
        if isinstance(v, str):
            if not v.strip():
                return []
            return [item.strip().lower() for item in v.split(",") if item.strip()]
        if isinstance(v, list):
            return [str(item).strip().lower() for item in v if str(item).strip()]
        return []


class ProductoCrear(ProductoBase):
    """Esquema requerido para la creación de un nuevo producto en base de datos."""

    pass


class ProductoDTO(ProductoBase):
    """DTO inmutable de lectura que representa un producto persistido."""

    id: int
    ultima_actualizacion: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_validator("aliases", mode="before")
    @classmethod
    def extraer_aliases_orm(cls, v: object) -> object:
        """Permite mapear la relación ProductoDB.aliases_rel cuando viene del ORM."""
        if hasattr(v, "__iter__") and not isinstance(v, (str, bytes)):
            items = list(v)
            if items and hasattr(items[0], "alias"):
                return [item.alias for item in items]
        return v