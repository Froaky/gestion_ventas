# models/venta.py
import datetime
from . import db

venta_producto = db.Table('venta_producto',
    db.Column('venta_id', db.Integer, db.ForeignKey('ventas.id')),
    db.Column('producto_id', db.Integer, db.ForeignKey('productos.id'))
)

class Venta(db.Model):
    __tablename__ = 'ventas'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    total = db.Column(db.Float, nullable=False)

    productos = db.relationship('Producto', secondary=venta_producto, backref='ventas')

    def to_dict(self):
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "total": self.total
        }

