from __future__ import annotations

import logging
import os
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def _obtener_log_path() -> Path:
    """Determina la ruta absoluta del archivo de logs según la configuración o el SO."""
    env_file = os.environ.get("FERREHOGAR_LOG_FILE")
    if env_file:
        log_path = Path(env_file)
    else:
        env_dir = os.environ.get("FERREHOGAR_LOG_DIR")
        if env_dir:
            base_dir = Path(env_dir)
        elif os.name == "nt":
            app_data = os.environ.get("LOCALAPPDATA") or os.environ.get("APPDATA")
            base_dir = Path(app_data) / "ferrehogar-pos" if app_data else Path.home() / ".ferrehogar-pos"
        else:
            base_dir = Path.home() / ".local" / "share" / "ferrehogar-pos"

        base_dir.mkdir(parents=True, exist_ok=True)
        log_path = base_dir / "ferrehogar_pos.log"

    log_path.parent.mkdir(parents=True, exist_ok=True)
    return log_path


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
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Handler 1: Consola (Muestra desde INFO para no saturar la pantalla de testeo)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formato)
    logger.addHandler(console_handler)

    # Handler 2: Archivo Físico (Guarda TODO, incluyendo DEBUG, rotando a los 5MB)
    log_file_path = _obtener_log_path()
    file_handler = RotatingFileHandler(
        filename=str(log_file_path),
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=3,
        encoding="utf-8",
        delay=True,
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formato)
    logger.addHandler(file_handler)

    return logger


# Instancia global lista para ser importada en el core, controladores o pruebas
logger = configurar_logger()