from __future__ import annotations

import math


def parsear_precio(valor: str | float | int) -> float:
    """Convierte una cadena o número a un float válido manejando comas y puntos.

    Args:
        valor (str | float | int): Representación numérica o textual del precio.

    Returns:
        float: Valor decimal saneado o 0.0 si no es convertible.
    """
    if isinstance(valor, (float, int)):
        return float(valor)
    if not valor:
        return 0.0

    valor_limpio = str(valor).strip().replace(" ", "").replace("$", "")

    if "," in valor_limpio and "." not in valor_limpio:
        valor_limpio = valor_limpio.replace(",", ".")
    elif "," in valor_limpio and "." in valor_limpio:
        # Discriminar formatos internacionales (ej: "1,250.50" vs "1.250,50")
        if valor_limpio.rfind(",") > valor_limpio.rfind("."):
            valor_limpio = valor_limpio.replace(".", "").replace(",", ".")
        else:
            valor_limpio = valor_limpio.replace(",", "")

    try:
        return float(valor_limpio)
    except ValueError:
        return 0.0


def redondear_usd(monto: float) -> float:
    """Redondea un monto monetario en USD a 2 decimales estándar."""
    return round(float(monto), 2)


def calcular_monto_ves(monto_usd: float, tasa: float | None) -> int:
    """Calcula el equivalente en Bolívares (VES) redondeando al entero superior (ceil).

    Args:
        monto_usd (float): Monto base en dólares.
        tasa (float | None): Tasa de cambio activa.

    Returns:
        int: Monto en VES redondeado hacia arriba o 0 si la tasa es inválida.
    """
    if not tasa or tasa <= 0:
        return 0
    usd_redondeado = redondear_usd(monto_usd)
    return math.ceil(usd_redondeado * tasa)