# models/venta.py
import datetime
from . import db

class Venta(db.Model):
    __tablename__ = 'ventas'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    total = db.Column(db.Float, default=0.0)

    def to_dict(self):
        return {
            "id": self.id,
            "cliente_id": self.cliente_id,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "total": self.total
        }

