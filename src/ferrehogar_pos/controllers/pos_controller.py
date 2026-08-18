import math
from sqlalchemy.orm import Session
from ..core.database import init_db, ProductoDB, SessionLocal
from ..core.exchange import ExchangeRateProvider
from ..core import crud
from ..core.crud import obtener_session

class POSController:
    """Controlador principal que gestiona la lógica de negocio para el punto de venta."""

    def __init__(self):
        # Inicializa el proveedor de tasa de cambio
        self.exchange_provider = ExchangeRateProvider()
        
        # El carrito será un diccionario: {producto_id: {"producto": ProductoDB, "cantidad": int}}
        self.carrito: dict[int, dict] = {}
        
        # Almacena la fecha de la última actualización de la tasa en el controlador
        self.fecha_actualizacion_tasa: str = "No disponible"
        
        # Intentar cargar la tasa del BCV al iniciar el controlador
        self.actualizar_tasa_bcv()

    def actualizar_tasa_bcv(self) -> tuple[float, str] | None:
        """Intenta obtener la tasa oficial del día y actualiza la fecha en memoria."""
        resultado = self.exchange_provider.fetch_bcv_rate()
        if resultado:
            tasa, fecha = resultado
            self.fecha_actualizacion_tasa = fecha
            return resultado
        return None

    def establecer_tasa_manual(self, valor: float):
        """Permite al usuario ingresar una tasa a mano y marca la fecha como Manual."""
        self.exchange_provider.current_rate = valor
        self.fecha_actualizacion_tasa = "Ingresada manualmente"

    def obtener_tasa_actual(self) -> float | None:
        """Devuelve la tasa de cambio activa en memoria."""
        return self.exchange_provider.current_rate

    def buscar_productos(self, termino: str) -> list[ProductoDB]:
        """Invoca la búsqueda inteligente en la base de datos."""
        with obtener_session() as db:
            return crud.buscar_productos_por_termino(db, termino)

    def gestionar_cantidad(self, producto, decremento=False):
        """Gestiona el incremento o decremento de cantidades en el carrito."""
        if producto.id not in self.carrito:
            if not decremento:
                self.carrito[producto.id] = {"producto": producto, "cantidad": 1}
            return

        if decremento:
            self.carrito[producto.id]["cantidad"] -= 1
            if self.carrito[producto.id]["cantidad"] <= 0:
                del self.carrito[producto.id] # Eliminamos si llega a cero
        else:
            self.carrito[producto.id]["cantidad"] += 1

    def limpiar_carrito(self):
        """Vacía todos los elementos de la simulación actual."""
        self.carrito.clear()

    def calcular_totales(self) -> dict[str, any]:
        """Calcula el total acumulado en dólares y bolívares,

        e incluye la fecha y hora de la última actualización de la tasa.
        """
        tasa = self.obtener_tasa_actual() or 0.0
        total_usd = 0.0

        for item in self.carrito.values():
            producto = item["producto"]
            cantidad = item["cantidad"]
            total_usd += producto.precio_venta_usd * cantidad

        total_usd_redondeado = round(total_usd, 2)
        total_ves_entero = math.ceil(total_usd_redondeado * tasa)

        return {
            "total_usd": total_usd_redondeado,
            "total_ves": total_ves_entero,
            "tasa_fecha": self.fecha_actualizacion_tasa,
        }
