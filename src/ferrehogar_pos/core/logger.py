import logging
import sys
from logging.handlers import RotatingFileHandler

def configurar_logger() -> logging.Logger:
    """Configura un sistema de logging de doble salida: consola y archivo rotativo."""
    logger = logging.getLogger("ferrehogar_pos")
    logger.setLevel(logging.DEBUG)

    # Evitar duplicar handlers si se inicializa más de una vez
    if logger.handlers:
        return logger

    # Formato profesional para auditoría de transacciones y errores
    formato = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] (%(name)s:%(filename)s:%(lineno)d) - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Handler 1: Consola (Muestra desde INFO para no saturar la pantalla de testeo)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formato)
    logger.addHandler(console_handler)

    # Handler 2: Archivo Físico (Guarda TODO, incluyendo DEBUG, rotando a los 5MB)
    file_handler = RotatingFileHandler(
        filename="ferrehogar_pos.log",
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formato)
    logger.addHandler(file_handler)

    return logger

# Instancia global lista para ser importada en el core, controladores o pruebas
logger = configurar_logger()