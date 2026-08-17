from ferrehogar_pos.core.database import ProductoDB, SessionLocal


def debug():
    db = SessionLocal()
    productos = db.query(ProductoDB).all()
    print(f"DEBUG: Cantidad de productos encontrados en la DB: {len(productos)}")
    for p in productos:
        print(f"Producto: {p.nombre}, Código: {p.codigo}")
    db.close()

if __name__ == "__debug__":
    debug()