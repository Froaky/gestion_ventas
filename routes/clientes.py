from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from models import db, Cliente

bp = Blueprint('clientes', __name__, url_prefix='/clientes')

# --- API REST Endpoints ---
@bp.route('/api', methods=['GET'])
def get_clientes_api():
    clientes = Cliente.query.all()
    return jsonify([cliente.to_dict() for cliente in clientes])

@bp.route('/api', methods=['POST'])
def create_cliente_api():
    data = request.get_json()
    new_cliente = Cliente(
        name=data.get('name'),
        telefono=data.get('telefono')
    )
    db.session.add(new_cliente)
    db.session.commit()
    return jsonify(new_cliente.to_dict()), 201

@bp.route('/api/<int:id>', methods=['PUT'])
def update_cliente_api(id):
    data = request.get_json()
    cliente = Cliente.query.get_or_404(id)
    cliente.name = data.get('name', cliente.name)
    cliente.telefono = data.get('telefono', cliente.telefono)
    db.session.commit()
    return jsonify(cliente.to_dict())

@bp.route('/api/<int:id>', methods=['DELETE'])
def delete_cliente_api(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    return jsonify({'message': 'Cliente eliminado'}), 204

# --- Vistas HTML ---
@bp.route('/lista', methods=['GET'])
def lista_clientes():
    clientes = Cliente.query.all()
    return render_template('clientes.html', clientes=clientes)

@bp.route('/crear', methods=['GET', 'POST'])
def crear_cliente():
    if request.method == 'POST':
        name = request.form.get('name')
        telefono = request.form.get('telefono')
        nuevo_cliente = Cliente(name=name, telefono=telefono)
        db.session.add(nuevo_cliente)
        db.session.commit()
        flash('Cliente creado correctamente', 'success')
        return redirect(url_for('clientes.lista_clientes'))
    return render_template('crear_cliente.html')

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    if request.method == 'POST':
        cliente.name = request.form.get('name')
        cliente.telefono = request.form.get('telefono')
        db.session.commit()
        flash('Cliente actualizado correctamente', 'success')
        return redirect(url_for('clientes.lista_clientes'))
    return render_template('editar_cliente.html', cliente=cliente)

@bp.route('/eliminar/<int:id>', methods=['GET'])
def eliminar_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()
    flash('Cliente eliminado correctamente', 'success')
    return redirect(url_for('clientes.lista_clientes'))
