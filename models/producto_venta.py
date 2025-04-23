# models/producto_venta.py
from . import db

class VentaProducto(db.Model):
    __tablename__ = 'venta_producto'
    
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'), primary_key=True)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False, default=1)
    precio_unitario = db.Column(db.Float, nullable=False)

    producto = db.relationship("Producto", back_populates="ventas")
    venta = db.relationship("Venta", back_populates="productos")
