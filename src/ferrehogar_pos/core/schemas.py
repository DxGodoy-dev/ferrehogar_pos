from datetime import datetime
from pydantic import BaseModel, Field, field_validator


class ProductoBase(BaseModel):
    """Esquema base con las especificaciones del negocio de la ferretería."""

    codigo: str | None = Field(default=None, max_length=50)
    nombre: str = Field(..., min_length=3, max_length=150)
    aliases: list[str] = Field(default_factory=list)
    area: str = Field(default="General", max_length=50)
    precio_venta_usd: float = Field(..., gt=0.0)
    precio_compra_usd: float = Field(..., gt=0.0)

    @field_validator("nombre")
    @classmethod
    def limpiar_nombre(cls, v: str) -> str:
        """Normaliza el nombre eliminando espacios vacíos o dobles."""
        return " ".join(v.split()).strip()

    @field_validator("aliases", mode="before")
    @classmethod
    def normalizar_aliases(cls, v: any) -> list[str]:
        """Asegura que los aliases sean siempre una lista de strings limpios y en minúsculas."""
        if isinstance(v, str):
            if not v.strip():
                return []
            return [item.strip().lower() for item in v.split(",") if item.strip()]
        if isinstance(v, list):
            return [str(item).strip().lower() for item in v if str(item).strip()]
        return []


class ProductoCrear(ProductoBase):
    """Esquema requerido para registrar un nuevo producto."""

    pass


class ProductoDTO(ProductoBase):
    """Representa el producto con metadatos provenientes de la base de datos."""

    id: int
    ultima_actualizacion: datetime

    class Config:
        from_attributes = True