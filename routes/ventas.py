import datetime
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from services.ventas_service import (
    get_all_ventas,
    create_venta,
    update_venta,
    delete_venta,
    get_ventas_ultimos_5_meses
)
from models.venta import Venta

bp = Blueprint('ventas', __name__, url_prefix='/ventas')

# --- API REST Endpoints ---

@bp.route('/api', methods=['GET'])
def get_ventas_api():
    ventas = get_all_ventas()
    return jsonify([venta.to_dict() for venta in ventas])

@bp.route('/api', methods=['POST'])
def create_venta_api():
    data = request.get_json()
    nueva = create_venta(
        cliente_id=data.get('cliente_id'),
        total=float(data.get('total', 0.0))
        # Aquí podrías agregar productos si implementás lógica en el API también
    )
    return jsonify(nueva.to_dict()), 201

@bp.route('/api/<int:id>', methods=['PUT'])
def update_venta_api(id):
    data = request.get_json()
    actualizado = update_venta(
        id,
        cliente_id=data.get('cliente_id'),
        total=float(data.get('total', 0.0))
    )
    return jsonify(actualizado.to_dict())

@bp.route('/api/<int:id>', methods=['DELETE'])
def delete_venta_api(id):
    delete_venta(id)
    return jsonify({"message": "Venta eliminada"}), 204

@bp.route('/api/sales_by_month', methods=['GET'])
def sales_by_month():
    labels, totals, counts = get_ventas_ultimos_5_meses()
    return jsonify({"labels": labels, "totals": totals, "counts": counts})

# --- Vistas HTML ---

@bp.route('/lista', methods=['GET'])
def lista_ventas():
    ventas = get_all_ventas()
    return render_template('ventas/lista.html', ventas=ventas)

@bp.route('/crear', methods=['GET', 'POST'])
def crear_venta_view():
    from models.cliente import Cliente
    from models.producto import Producto
    clientes = Cliente.query.all()
    productos = Producto.query.all()

    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        total = float(request.form.get('total', 0.0))
        producto_ids = request.form.getlist('producto_ids')  # 👈 agregado para recibir productos

        create_venta(cliente_id, total, producto_ids)  # 👈 ahora incluye productos
        flash('Venta creada correctamente', 'success')
        return redirect(url_for('ventas.lista_ventas'))

    return render_template('ventas/crear.html', clientes=clientes, productos=productos)

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_venta_view(id):
    venta = Venta.query.get_or_404(id)
    from models.cliente import Cliente
    clientes = Cliente.query.all()
    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        total = float(request.form.get('total', venta.total))
        update_venta(id, cliente_id, total)
        flash('Venta actualizada correctamente', 'success')
        return redirect(url_for('ventas.lista_ventas'))
    return render_template('ventas/editar.html', venta=venta, clientes=clientes)

@bp.route('/eliminar/<int:id>', methods=['GET'])
def eliminar_venta_view(id):
    delete_venta(id)
    flash('Venta eliminada correctamente', 'success')
    return redirect(url_for('ventas.lista_ventas'))

@bp.route('/')
def home():
    labels, totals, counts = get_ventas_ultimos_5_meses()
    return render_template('home.html', labels=labels, totals=totals, counts=counts)
