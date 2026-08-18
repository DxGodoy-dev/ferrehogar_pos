import pandas as pd
from pathlib import Path
from ferrehogar_pos.core.crud import crear_producto_local, obtener_session
from ferrehogar_pos.core.schemas import ProductoCrear
from ferrehogar_pos.core.logger import logger

def ejecutar_importacion(archivo_csv: str | Path, area: str) -> None:
    """Importa productos desde un archivo CSV hacia la base de datos local.

    Lee columnas específicas de productos, omite filas vacías o encabezados y
    registra cada ítem en la base de datos dentro de una sesión gestionada.

    Args:
        archivo_csv (str | Path): Ruta del archivo CSV a procesar.
        area (str): Nombre del área o categoría asignada a los productos.

    Returns:
        None

    Raises:
        FileNotFoundError: Si el archivo CSV especificado no existe en la ruta indicada.
    """
    archivo_path = Path(archivo_csv)
    if not archivo_path.is_file():
        raise FileNotFoundError(f"Archivo no encontrado: {archivo_path}")

    # Ajuste: leer columnas específicas (nombre en col 1, precio venta en col 2)
    # Ajustamos skiprows según la estructura detectada
    df = pd.read_csv(archivo_path, usecols=[1, 2], names=["nombre", "precio_venta_usd"], skiprows=2)
    
    with obtener_session() as db:
        for _, row in df.iterrows():
            # Filtramos filas vacías o encabezados residuales
            if pd.isna(row["nombre"]) or (isinstance(row["nombre"], str) and row["nombre"].isupper() and len(row["nombre"]) < 10):
                continue
                
            producto_in = ProductoCrear(
                nombre=str(row["nombre"]),
                area=area,
                precio_venta_usd=float(row["precio_venta_usd"]),
                precio_compra_usd=0.0  # PRECIO DE COMPRA FIJADO EN 0
            )
            crear_producto_local(db, producto_in)


if __name__ == "__main__":
    ejecutar_importacion("SISTEMA INVERSIONES BRIMU DEF.xlsx - Ferreteria. Lavadora.csv", "Ferretería")
    ejecutar_importacion("SISTEMA INVERSIONES BRIMU DEF.xlsx - Refrigeración.csv", "Refrigeración")
    logger.info("Carga finalizada con éxito.")