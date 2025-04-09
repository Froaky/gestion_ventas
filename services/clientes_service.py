from models import db
from models.cliente import Cliente

def get_all_clientes():
    return Cliente.query.all()

def create_cliente(name, telefono):
    nuevo_cliente = Cliente(name=name, telefono=telefono)
    db.session.add(nuevo_cliente)
    db.session.commit()
    return nuevo_cliente

def update_cliente(id, name, telefono):
    cliente = Cliente.query.get_or_404(id)
    cliente.name = name
    cliente.telefono = telefono
    db.session.commit()
    return cliente

def delete_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()

def search_clientes(nombre):
    return Cliente.query.filter(Cliente.name.ilike(f"%{nombre}%")).all()
