from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from models import db, Venta, Cliente, Producto
# Nota: En este ejemplo, los detalles de venta no se gestionan en la interfaz HTML.
bp = Blueprint('ventas', __name__, url_prefix='/ventas')

# --- API REST Endpoints ---
@bp.route('/api', methods=['GET'])
def get_ventas_api():
    ventas = Venta.query.all()
    return jsonify([venta.to_dict() for venta in ventas])

@bp.route('/api', methods=['POST'])
def create_venta_api():
    data = request.get_json()
    new_venta = Venta(
        cliente_id=data.get('cliente_id'),
        total=data.get('total', 0.0)
    )
    db.session.add(new_venta)
    db.session.commit()
    return jsonify(new_venta.to_dict()), 201

# --- Vistas HTML ---
@bp.route('/lista', methods=['GET'])
def lista_ventas():
    ventas = Venta.query.all()
    return render_template('ventas.html', ventas=ventas)

@bp.route('/crear', methods=['GET', 'POST'])
def crear_venta():
    clientes = Cliente.query.all()
    productos = Producto.query.all()  # Si quieres mostrar productos para detalles
    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        total = request.form.get('total', 0.0)
        nueva_venta = Venta(cliente_id=cliente_id, total=total)
        db.session.add(nueva_venta)
        db.session.commit()
        flash('Venta creada correctamente', 'success')
        return redirect(url_for('ventas.lista_ventas'))
    return render_template('crear_venta.html', clientes=clientes, productos=productos)

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_venta(id):
    venta = Venta.query.get_or_404(id)
    if request.method == 'POST':
        venta.cliente_id = request.form.get('cliente_id')
        venta.total = request.form.get('total', venta.total)
        db.session.commit()
        flash('Venta actualizada correctamente', 'success')
        return redirect(url_for('ventas.lista_ventas'))
    clientes = Cliente.query.all()
    return render_template('editar_venta.html', venta=venta, clientes=clientes)

@bp.route('/eliminar/<int:id>', methods=['GET'])
def eliminar_venta(id):
    venta = Venta.query.get_or_404(id)
    db.session.delete(venta)
    db.session.commit()
    flash('Venta eliminada correctamente', 'success')
    return redirect(url_for('ventas.lista_ventas'))
