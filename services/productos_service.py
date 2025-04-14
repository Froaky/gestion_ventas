from models import db
from models.producto import Producto
from models.proveedor import Proveedor  # Asegurate de importar esto

def get_all_productos():
    return Producto.query.all()

def create_producto(name, precio, stock, categoria, proveedor_id):
    nuevo_producto = Producto(
        name=name,
        precio=precio,
        stock=stock,
        categoria=categoria,
        proveedor_id=proveedor_id
    )
    db.session.add(nuevo_producto)
    db.session.commit()
    return nuevo_producto



def update_producto(id, name, precio, stock, categoria, proveedor_id):
    producto = Producto.query.get_or_404(id)
    producto.name = name
    producto.precio = precio
    producto.stock = stock
    producto.categoria = categoria
    producto.proveedor_id = proveedor_id
    db.session.commit()
    return producto

def delete_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
