from __future__ import annotations

from sqlalchemy.orm import Session, selectinload

from ferrehogar_pos.models.venta import DetalleVentaDB, VentaDB
from ferrehogar_pos.schemas.venta import DetalleVentaDTO, VentaCrear, VentaDTO


def registrar_venta(db: Session, venta_in: VentaCrear) -> VentaDTO:
    """Registra una transacción de venta y su desglose de ítems de forma atómica.

    Args:
        db (Session): Sesión activa de base de datos.
        venta_in (VentaCrear): Payload con cabecera y lista de detalles a registrar.

    Returns:
        VentaDTO: Entidad de venta persistida con sus ítems en formato DTO.
    """
    nueva_venta = VentaDB(
        tasa_bcv_aplicada=venta_in.tasa_bcv_aplicada,
        tasa_fecha_referencia=venta_in.tasa_fecha_referencia,
        total_usd=venta_in.total_usd,
        total_ves=venta_in.total_ves,
    )

    nueva_venta.detalles_rel = [
        DetalleVentaDB(
            producto_id=d.producto_id,
            nombre_producto_historico=d.nombre_producto_historico,
            cantidad=d.cantidad,
            precio_unitario_usd=d.precio_unitario_usd,
            subtotal_usd=d.subtotal_usd,
        )
        for d in venta_in.detalles
    ]

    try:
        db.add(nueva_venta)
        db.commit()
        db.refresh(nueva_venta)
    except Exception:
        db.rollback()
        raise

    return VentaDTO(
        id=nueva_venta.id,
        fecha_utc=nueva_venta.fecha_utc,
        tasa_bcv_aplicada=nueva_venta.tasa_bcv_aplicada,
        tasa_fecha_referencia=nueva_venta.tasa_fecha_referencia,
        total_usd=nueva_venta.total_usd,
        total_ves=nueva_venta.total_ves,
        detalles=[
            DetalleVentaDTO(
                id=det.id,
                producto_id=det.producto_id,
                nombre_producto_historico=det.nombre_producto_historico,
                cantidad=det.cantidad,
                precio_unitario_usd=det.precio_unitario_usd,
                subtotal_usd=det.subtotal_usd,
            )
            for det in nueva_venta.detalles_rel
        ],
    )


def obtener_venta_por_id(db: Session, venta_id: int) -> VentaDTO | None:
    """Recupera una venta histórica por su identificador primario.

    Args:
        db (Session): Sesión activa de base de datos.
        venta_id (int): Identificador numérico de la venta.

    Returns:
        VentaDTO | None: Venta encontrada en formato DTO o None si no existe.
    """
    venta_db = (
        db.query(VentaDB)
        .options(selectinload(VentaDB.detalles_rel))
        .filter(VentaDB.id == venta_id)
        .first()
    )
    if not venta_db:
        return None

    return VentaDTO(
        id=venta_db.id,
        fecha_utc=venta_db.fecha_utc,
        tasa_bcv_aplicada=venta_db.tasa_bcv_aplicada,
        tasa_fecha_referencia=venta_db.tasa_fecha_referencia,
        total_usd=venta_db.total_usd,
        total_ves=venta_db.total_ves,
        detalles=[
            DetalleVentaDTO(
                id=det.id,
                producto_id=det.producto_id,
                nombre_producto_historico=det.nombre_producto_historico,
                cantidad=det.cantidad,
                precio_unitario_usd=det.precio_unitario_usd,
                subtotal_usd=det.subtotal_usd,
            )
            for det in venta_db.detalles_rel
        ],
    )