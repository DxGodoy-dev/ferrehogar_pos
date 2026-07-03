import pandas as pd
from crud import crear_producto_local, obtener_session
from schemas import ProductoCrear

def ejecutar_importacion(archivo_csv, area):
    # Ajuste: leer columnas específicas (nombre en col 1, precio venta en col 2)
    # Ajustamos skiprows según la estructura detectada
    df = pd.read_csv(archivo_csv, usecols=[1, 2], names=["nombre", "precio_venta_usd"], skiprows=2)
    
    with obtener_session() as db:
        for _, row in df.iterrows():
            try:
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
            except Exception as e:
                print(f"Error procesando {row['nombre']}: {e}")

# Ejecución
ejecutar_importacion("SISTEMA INVERSIONES BRIMU DEF.xlsx - Ferreteria. Lavadora.csv", "Ferretería")
ejecutar_importacion("SISTEMA INVERSIONES BRIMU DEF.xlsx - Refrigeración.csv", "Refrigeración")
print("Carga finalizada con éxito.")