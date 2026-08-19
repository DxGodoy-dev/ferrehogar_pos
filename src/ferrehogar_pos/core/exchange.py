from __future__ import annotations

from pyBCV import Currency

from ferrehogar_pos.core.helpers import sanitizar_float
from ferrehogar_pos.core.logger import logger


class ExchangeRateProvider:
    """Gestiona la obtención y el estado de la tasa de cambio del BCV."""

    def __init__(self) -> None:
        # Almacena la tasa y la fecha en memoria para evitar peticiones repetitivas
        self._cached_rate: float | None = None
        self._last_update: str | None = None

    def fetch_bcv_rate(self) -> tuple[float, str] | None:
        """Intenta obtener la tasa oficial del dólar y su fecha desde pybcv.

        Retorna una tupla (tasa, fecha_actualizacion) si tiene éxito,
        o None si ocurre un error de red o de parsing.
        """
        try:
            bcv = Currency()
            usd_rate_raw = bcv.get_rate(currency_code="USD", prettify=False)
            last_update_raw = bcv.get_rate(currency_code="Fecha")

            usd_rate = sanitizar_float(usd_rate_raw)
            if usd_rate is None or usd_rate <= 0:
                raise ValueError(
                    f"Valor de tasa inválido o no convertible: {usd_rate_raw!r}"
                )

            if not isinstance(last_update_raw, str) or not last_update_raw.strip():
                last_update = "Fecha no especificada"
            else:
                last_update = last_update_raw.strip()

            self._cached_rate = usd_rate
            self._last_update = last_update

            return self._cached_rate, self._last_update
        except Exception as e:
            # Captura fallas de conexión, timeouts o cambios en el DOM del BCV
            logger.warning("Error al obtener tasa del BCV: %s", e)
            return None

    @property
    def current_rate(self) -> float | None:
        """Devuelve la tasa almacenada en memoria."""
        return self._cached_rate

    @current_rate.setter
    def current_rate(self, value: float) -> None:
        """Permite establecer la tasa manualmente en caso de estar offline."""
        self._cached_rate = float(value)

    @property
    def last_update(self) -> str | None:
        """Devuelve la fecha de la última actualización almacenada en memoria."""
        return self._last_update