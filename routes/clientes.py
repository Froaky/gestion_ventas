from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from services.clientes_service import (
    get_all_clientes,
    create_cliente,
    update_cliente,
    delete_cliente,
    search_clientes
)

bp = Blueprint('clientes', __name__, url_prefix='/clientes')

# ==============================
#  API REST Endpoints
# ==============================

@bp.route('/api', methods=['GET'])
def get_clientes_api():
    clientes = get_all_clientes()
    return jsonify([c.to_dict() for c in clientes])

@bp.route('/api', methods=['POST'])
def create_cliente_api():
    data = request.get_json()
    nuevo = create_cliente(data.get('name'), data.get('telefono'))
    return jsonify(nuevo.to_dict()), 201

@bp.route('/api/<int:id>', methods=['PUT'])
def update_cliente_api(id):
    data = request.get_json()
    actualizado = update_cliente(id, data.get('name'), data.get('telefono'))
    return jsonify(actualizado.to_dict())

@bp.route('/api/<int:id>', methods=['DELETE'])
def delete_cliente_api(id):
    delete_cliente(id)
    return jsonify({'message': 'Cliente eliminado'}), 204

# ==============================
#  Vistas HTML
# ==============================

@bp.route('/lista', methods=['GET'])
def lista_clientes():
    clientes = get_all_clientes()
    return render_template('clientes/lista.html', clientes=clientes)

@bp.route('/crear', methods=['GET', 'POST'])
def crear_cliente_view():
    if request.method == 'POST':
        name = request.form.get('name')
        telefono = request.form.get('telefono')
        create_cliente(name, telefono)
        flash('Cliente creado correctamente', 'success')
        return redirect(url_for('clientes.lista_clientes'))
    return render_template('clientes/crear.html')

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_cliente_view(id):
    if request.method == 'POST':
        name = request.form.get('name')
        telefono = request.form.get('telefono')
        update_cliente(id, name, telefono)
        flash('Cliente actualizado correctamente', 'success')
        return redirect(url_for('clientes.lista_clientes'))
    # GET
    from models.cliente import Cliente
    cliente = Cliente.query.get_or_404(id)
    return render_template('clientes/editar.html', cliente=cliente)

@bp.route('/eliminar/<int:id>', methods=['GET'])
def eliminar_cliente_view(id):
    delete_cliente(id)
    flash('Cliente eliminado correctamente', 'success')
    return redirect(url_for('clientes.lista_clientes'))

@bp.route('/buscar', methods=['GET', 'POST'])
def buscar_cliente_view():
    resultados = []
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        resultados = search_clientes(nombre)
    return render_template('clientes/buscar.html', resultados=resultados)
