from ferrehogar_pos.core.database import ProductoDB
from ferrehogar_pos.core.crud import obtener_session
from ferrehogar_pos.core.logger import logger


def debug() -> None:
    """Consulta y registra en logs los productos existentes en la base de datos.

    Args:
        None

    Returns:
        None

    Raises:
        Exception: Si ocurre un fallo durante la consulta o conexión con la base de datos.
    """
    with obtener_session() as db:
        productos = db.query(ProductoDB).all()
        logger.debug(f"Cantidad de productos encontrados en la DB: {len(productos)}")
        for p in productos:
            logger.debug(f"Producto: {p.nombre}, Código: {p.codigo}")

if __name__ == "__main__":
    debug()