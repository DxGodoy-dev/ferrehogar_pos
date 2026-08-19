from __future__ import annotations

from pathlib import Path

import pandas as pd
from pydantic import ValidationError

from ferrehogar_pos.core.crud import crear_producto_local, obtener_session
from ferrehogar_pos.core.helpers import sanitizar_precio
from ferrehogar_pos.core.logger import logger
from ferrehogar_pos.core.schemas import ProductoCrear


def ejecutar_importacion(archivo_csv: str | Path, area: str) -> None:
    """Importa productos desde un archivo CSV hacia la base de datos local.

    Lee columnas específicas de productos, omite filas vacías o encabezados y
    registra cada ítem en la base de datos dentro de una sesión gestionada.

    Args:
        archivo_csv (str | Path): Ruta del archivo CSV a procesar.
        area (str): Nombre del área o categoría asignada a los productos.

    Raises:
        FileNotFoundError: Si el archivo CSV especificado no existe en la ruta indicada.
    """
    archivo_path = Path(archivo_csv)
    if not archivo_path.is_file():
        raise FileNotFoundError(f"Archivo no encontrado: {archivo_path}")

    df = pd.read_csv(
        archivo_path,
        usecols=[1, 2],
        names=["nombre", "precio_venta_usd"],
        skiprows=2,
    )

    insertados = 0
    omitidos = 0

    with obtener_session() as db:
        for row in df.itertuples(index=False):
            nombre_raw = getattr(row, "nombre", None)
            precio_raw = getattr(row, "precio_venta_usd", None)

            # Filtrar filas vacías o encabezados residuales
            if pd.isna(nombre_raw) or (
                isinstance(nombre_raw, str)
                and nombre_raw.isupper()
                and len(nombre_raw.strip()) < 10
            ):
                omitidos += 1
                continue

            precio_usd = sanitizar_precio(precio_raw)
            if precio_usd is None or precio_usd <= 0:
                omitidos += 1
                continue

            try:
                producto_in = ProductoCrear(
                    nombre=str(nombre_raw),
                    area=area,
                    precio_venta_usd=precio_usd,
                    precio_compra_usd=0.0,
                )
                crear_producto_local(db, producto_in)
                insertados += 1
            except ValidationError as ve:
                logger.warning(
                    f"Fallo de validación en fila '{nombre_raw}': {ve}"
                )
                omitidos += 1
            except Exception as e:
                logger.error(
                    f"Error al insertar producto '{nombre_raw}': {e}"
                )
                db.rollback()
                omitidos += 1

    logger.info(
        f"Importación de '{archivo_path.name}' completada: "
        f"{insertados} productos insertados, {omitidos} filas omitidas."
    )


if __name__ == "__main__":
    ejecutar_importacion(
        "SISTEMA INVERSIONES BRIMU DEF.xlsx - Ferreteria. Lavadora.csv",
        "Ferretería",
    )
    ejecutar_importacion(
        "SISTEMA INVERSIONES BRIMU DEF.xlsx - Refrigeración.csv",
        "Refrigeración",
    )
    logger.info("Carga finalizada con éxito.")