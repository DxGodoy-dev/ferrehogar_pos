from pyBCV import Currency


class ExchangeRateProvider:
    """Gestiona la obtención y el estado de la tasa de cambio del BCV."""

    def __init__(self):
        # Almacena la tasa y la fecha en memoria para evitar peticiones repetitivas
        self._cached_rate: float | None = None
        self._last_update: str | None = None

    def fetch_bcv_rate(self) -> tuple[float, str] | None:
        """Intenta obtener la tasa oficial del dólar y su fecha desde pybcv.

        Retorna una tupla (tasa, fecha_actualizacion) si tiene éxito, 
        o None si ocurre un error de red.
        """
        try:
            bcv = Currency()
            usd_rate = bcv.get_rate(currency_code='USD', prettify=False)
            last_update = bcv.get_rate(currency_code='Fecha')
            
            self._cached_rate = float(usd_rate)
            self._last_update = str(last_update)
            
            return self._cached_rate, self._last_update
        except Exception:
            # Captura fallas de conexión, timeouts o cambios en el DOM del BCV
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