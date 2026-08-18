import os
from pathlib import Path
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# Configuración del motor de la base de datos local
BASE_DIR = Path.home() / ".local" / "share" / "ferrehogar-pos"
BASE_DIR.mkdir(parents=True, exist_ok=True) # Crea el directorio si no existe

# Construir la URL absoluta
DATABASE_PATH = BASE_DIR / "ferreteria.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Configuración del motor
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Creador de sesiones para interactuar con las tablas
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para los modelos relacionales
Base = declarative_base()


class ProductoAliasDB(Base):
    """Modelo que almacena los aliases individuales de un producto para búsquedas eficientes."""

    __tablename__ = "producto_aliases"

    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(
        Integer, 
        ForeignKey("productos.id", ondelete="CASCADE"), 
        nullable=False, 
        index=True
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
    ultima_actualizacion = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relación uno-a-muchos con carga inmediata (eager loading) para facilitar el DTO
    aliases_rel = relationship(
        "ProductoAliasDB", 
        back_populates="producto", 
        cascade="all, delete-orphan",
        lazy="joined"
    )


def init_db():
    """Crea todas las tablas definidas si no existen en la base de datos."""
    Base.metadata.create_all(bind=engine)