from __future__ import annotations

import re
from typing import Any

import pandas as pd


def sanitizar_float(valor: Any) -> float | None:
    """Convierte cualquier valor o cadena numérica a float de forma tolerante.

    Soporta formatos con comas decimales (ej. '652,97'), puntos ('652.97')
    o cadenas con texto o caracteres adicionales.
    Retorna None si no es convertible o si es nulo.
    """
    if valor is None or pd.isna(valor):
        return None
    if isinstance(valor, (int, float)):
        return float(valor)

    texto = str(valor).strip()
    texto_limpio = re.sub(r"[^\d.,-]", "", texto)
    if not texto_limpio or texto_limpio == "-":
        return None

    # Normalización de separadores según presencia de coma/punto
    if "," in texto_limpio and "." in texto_limpio:
        texto_limpio = texto_limpio.replace(",", "")
    elif "," in texto_limpio:
        texto_limpio = texto_limpio.replace(",", ".")

    try:
        return float(texto_limpio)
    except ValueError:
        return None


def sanitizar_precio(valor: Any) -> float | None:
    """Convierte valores a un precio float válido no negativo (>= 0.0)."""
    resultado = sanitizar_float(valor)
    if resultado is not None and resultado >= 0.0:
        return resultado
    return None