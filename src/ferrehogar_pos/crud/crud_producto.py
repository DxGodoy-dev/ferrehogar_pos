from __future__ import annotations

from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import or_
from sqlalchemy.orm import Session, selectinload

from ferrehogar_pos.core.database import SessionLocal
from ferrehogar_pos.models.producto import ProductoAliasDB, ProductoDB
from ferrehogar_pos.schemas.producto import ProductoCrear, ProductoDTO


@contextmanager
def obtener_session() -> Generator[Session, None, None]:
    """Gestiona el ciclo de vida y cierre seguro de sesiones de base de datos.

    Yields:
        Session: Sesión activa de SQLAlchemy para interactuar con la base de datos.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def buscar_productos_por_termino(db: Session, termino: str) -> list[ProductoDTO]:
    """Busca productos por código, coincidencia parcial en nombre o en sus aliases.

    Args:
        db (Session): Sesión activa de base de datos.
        termino (str): Término o criterio de búsqueda (código, nombre o alias).

    Returns:
        list[ProductoDTO]: Lista de productos coincidentes desacoplados de la DB.
    """
    termino_limpio = termino.strip().lower()
    if not termino_limpio:
        return []

    productos_db = (
        db.query(ProductoDB)
        .options(selectinload(ProductoDB.aliases_rel))
        .outerjoin(ProductoDB.aliases_rel)
        .filter(
            or_(
                ProductoDB.codigo == termino_limpio,
                ProductoDB.nombre.ilike(f"%{termino_limpio}%"),
                ProductoAliasDB.alias.ilike(f"%{termino_limpio}%"),
            )
        )
        .distinct()
        .all()
    )

    return [
        ProductoDTO(
            id=p.id,
            codigo=p.codigo,
            nombre=p.nombre,
            area=p.area,
            precio_venta_usd=p.precio_venta_usd,
            precio_compra_usd=p.precio_compra_usd,
            aliases=[a.alias for a in p.aliases_rel] if p.aliases_rel else [],
            ultima_actualizacion=p.ultima_actualizacion,
        )
        for p in productos_db
    ]


def crear_producto_local(db: Session, producto_in: ProductoCrear) -> ProductoDTO:
    """Registra un nuevo producto y sus aliases usando relaciones de SQLAlchemy.

    Args:
        db (Session): Sesión activa de base de datos.
        producto_in (ProductoCrear): Datos validados del producto y sus aliases a persistir.

    Returns:
        ProductoDTO: Instancia validada y persistida en formato DTO.
    """
    nuevo_producto = ProductoDB(
        codigo=producto_in.codigo.strip().lower() if producto_in.codigo else None,
        nombre=producto_in.nombre,
        area=producto_in.area,
        precio_venta_usd=producto_in.precio_venta_usd,
        precio_compra_usd=producto_in.precio_compra_usd,
    )

    if producto_in.aliases:
        nuevo_producto.aliases_rel = [
            ProductoAliasDB(alias=alias_str) for alias_str in producto_in.aliases
        ]

    try:
        db.add(nuevo_producto)
        db.commit()
        db.refresh(nuevo_producto)
    except Exception:
        db.rollback()
        raise

    return ProductoDTO(
        id=nuevo_producto.id,
        codigo=nuevo_producto.codigo,
        nombre=nuevo_producto.nombre,
        area=nuevo_producto.area,
        precio_venta_usd=nuevo_producto.precio_venta_usd,
        precio_compra_usd=nuevo_producto.precio_compra_usd,
        aliases=[a.alias for a in nuevo_producto.aliases_rel] if nuevo_producto.aliases_rel else [],
        ultima_actualizacion=nuevo_producto.ultima_actualizacion,
    )