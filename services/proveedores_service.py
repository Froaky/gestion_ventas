# services/proveedores_service.py
from models import db
from models.proveedor import Proveedor

def get_all_proveedores():
    return Proveedor.query.all()

def create_proveedor(name, telefono):
    nuevo_proveedor = Proveedor(name=name, telefono=telefono)
    db.session.add(nuevo_proveedor)
    db.session.commit()
    return nuevo_proveedor

def update_proveedor(id, name, telefono):
    proveedor = Proveedor.query.get_or_404(id)
    proveedor.name = name
    proveedor.telefono = telefono
    db.session.commit()
    return proveedor

def delete_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    db.session.delete(proveedor)
    db.session.commit()
