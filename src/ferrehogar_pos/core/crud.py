from contextlib import contextmanager
from sqlalchemy import or_
from sqlalchemy.orm import Session

from .database import ProductoAliasDB, ProductoDB, SessionLocal
from .schemas import ProductoCrear


@contextmanager
def obtener_session():
    """Context manager para asegurar el cierre seguro de sesiones en Flet."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def buscar_productos_por_termino(db: Session, termino: str) -> list[ProductoDB]:
    """Busca productos por código, coincidencia parcial en nombre o en sus aliases."""
    termino_limpio = termino.strip().lower()
    if not termino_limpio:
        return []

    return (
        db.query(ProductoDB)
        .outerjoin(ProductoDB.aliases_rel)
        .filter(
            or_(
                ProductoDB.codigo == termino_limpio,
                ProductoDB.nombre.ilike(f"%{termino_limpio}%"),
                ProductoAliasDB.alias.ilike(f"%{termino_limpio}%"),
            )
        )
        .distinct()  # Evita productos duplicados si coinciden múltiples aliases
        .all()
    )


def crear_producto_local(db: Session, producto_in: ProductoCrear) -> ProductoDB:
    """Registra un nuevo producto y sus aliases usando relaciones de SQLAlchemy."""
    # Creamos la instancia principal del producto
    nuevo_producto = ProductoDB(
        codigo=producto_in.codigo.strip().lower() if producto_in.codigo else None,
        nombre=producto_in.nombre,
        area=producto_in.area,
        precio_venta_usd=producto_in.precio_venta_usd,
        precio_compra_usd=producto_in.precio_compra_usd,
    )
    
    # Mapeamos la lista de strings de los aliases a instancias de ProductoAliasDB
    if producto_in.aliases:
        nuevo_producto.aliases_rel = [
            ProductoAliasDB(alias=alias_str) for alias_str in producto_in.aliases
        ]

    db.add(nuevo_producto)
    db.commit()
    db.refresh(nuevo_producto)
    return nuevo_producto