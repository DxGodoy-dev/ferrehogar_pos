from __future__ import annotations

import os
from pathlib import Path

from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


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
            base_dir = (
                Path(app_data) / "ferrehogar-pos"
                if app_data
                else Path.home() / ".ferrehogar-pos"
            )
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


# Clase base declarativa de SQLAlchemy 2.0
class Base(DeclarativeBase):
    pass


def init_db() -> None:
    """Crea todas las tablas definidas importando los modelos para registrarlos en Base."""
    # Importación diferida para registrar las clases hijas en Base.metadata sin dependencias circulares
    from ferrehogar_pos.models import producto, venta  # noqa: F401

    Base.metadata.create_all(bind=engine)