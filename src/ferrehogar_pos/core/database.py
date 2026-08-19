from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, relationship, sessionmaker


def _obtener_db_url() -> str:
    """Determina la URL de la base de datos según variables de entorno o ruta local estándar."""
    env_url = os.environ.get("FERREHOGAR_DB_URL")
    if env_url:
        return env_url

    env_path = os.environ.get("FERREHOGAR_DB_PATH")
    if env_path:
        db_path = Path(env_path)
    else:
        # Ruta estándar multiplataforma
        if os.name == "nt":
            app_data = os.environ.get("LOCALAPPDATA") or os.environ.get("APPDATA")
            base_dir = Path(app_data) / "ferrehogar-pos" if app_data else Path.home() / ".ferrehogar-pos"
        else:
            base_dir = Path.home() / ".local" / "share" / "ferrehogar-pos"

        base_dir.mkdir(parents=True, exist_ok=True)
        db_path = base_dir / "ferreteria.db"

    return f"sqlite:///{db_path}"


DATABASE_URL = _obtener_db_url()

# Configuración del motor SQLite
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)


# Habilitar el soporte de claves foráneas en SQLite
@event.listens_for(Engine, "connect")
def _activar_foreign_keys(dbapi_connection: object, connection_record: object) -> None:
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    cursor.close()


# Creador de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Clase base moderna de SQLAlchemy 2.0
class Base(DeclarativeBase):
    pass


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


def init_db() -> None:
    """Crea todas las tablas definidas si no existen en la base de datos."""
    Base.metadata.create_all(bind=engine)