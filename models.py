from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Cliente(db.Model):
    __tablename__ = 'clientes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20), nullable=True)
    ventas = db.relationship('Venta', backref='cliente', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'telefono': self.telefono
        }

class Proveedor(db.Model):
    __tablename__ = 'proveedores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    productos = db.relationship('Producto', backref='proveedor', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'telefono': self.telefono
        }

class Producto(db.Model):
    __tablename__ = 'productos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    precio = db.Column(db.Float, nullable=True)
    stock = db.Column(db.Integer, nullable=True)
    categoria = db.Column(db.String(50), nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'), nullable=False)
    detalles = db.relationship('DetalleVenta', backref='producto', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'precio': self.precio,
            'stock': self.stock,
            'categoria': self.categoria,
            'proveedor_id': self.proveedor_id
        }

class Venta(db.Model):
    __tablename__ = 'ventas'
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, default=0.0)
    detalles = db.relationship('DetalleVenta', backref='venta', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'fecha': self.fecha.isoformat(),
            'total': self.total
        }

class DetalleVenta(db.Model):
    __tablename__ = 'detalle_ventas'
    id = db.Column(db.Integer, primary_key=True)
    venta_id = db.Column(db.Integer, db.ForeignKey('ventas.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'), nullable=False)
    cantidad = db.Column(db.Integer, default=1)
    precio_unitario = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'venta_id': self.venta_id,
            'producto_id': self.producto_id,
            'cantidad': self.cantidad,
            'precio_unitario': self.precio_unitario
        }
