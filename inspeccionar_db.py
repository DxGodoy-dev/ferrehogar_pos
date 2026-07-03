from src.ferrehogar_pos.core.database import SessionLocal, ProductoDB

db = SessionLocal()
productos = db.query(ProductoDB).all()
print(f"DEBUG: Cantidad de productos encontrados en la DB: {len(productos)}")
for p in productos:
    print(f"Producto: {p.nombre}, Código: {p.codigo}")
db.close()