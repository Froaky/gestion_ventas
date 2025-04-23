# models/venta.py
import datetime
from . import db

class Venta(db.Model):
    __tablename__ = 'ventas'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'))
    total = db.Column(db.Float, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    productos = db.relationship("VentaProducto", back_populates="venta")

    def to_dict(self):
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "total": self.total,
            "productos": [
                {
                    "id": pv.producto.id,
                    "nombre": pv.producto.name,
                    "cantidad": pv.cantidad,
                    "precio_unitario": pv.precio_unitario,
                    "subtotal": pv.cantidad * pv.precio_unitario
                } for pv in self.productos
            ]
        }
