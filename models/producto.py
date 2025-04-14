# models/producto.py
from . import db

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Float, nullable=True)
    stock = db.Column(db.Integer, nullable=True)
    categoria = db.Column(db.String(50), nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "precio": self.precio,
            "stock": self.stock,
            "categoria": self.categoria,
            "proveedor_id": self.proveedor_id
        }
