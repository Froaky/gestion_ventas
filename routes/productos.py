from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from models import db, Producto

bp = Blueprint('productos', __name__, url_prefix='/productos')

# --- API REST Endpoints ---
@bp.route('/api', methods=['GET'])
def get_productos_api():
    productos = Producto.query.all()
    return jsonify([producto.to_dict() for producto in productos])

@bp.route('/api', methods=['POST'])
def create_producto_api():
    data = request.get_json()
    nuevo_producto = Producto(
        name=data.get('name'),
        precio=data.get('precio'),
        stock=data.get('stock'),
        categoria=data.get('categoria'),
        proveedor_id=data.get('proveedor_id')
    )
    db.session.add(nuevo_producto)
    db.session.commit()
    return jsonify(nuevo_producto.to_dict()), 201

# --- Vistas HTML ---
@bp.route('/lista', methods=['GET'])
def lista_productos():
    productos = Producto.query.all()
    return render_template('productos.html', productos=productos)

@bp.route('/crear', methods=['GET', 'POST'])
def crear_producto():
    if request.method == 'POST':
        name = request.form.get('name')
        precio = request.form.get('precio')
        stock = request.form.get('stock')
        categoria = request.form.get('categoria')
        proveedor_id = request.form.get('proveedor_id')
        nuevo_producto = Producto(
            name=name,
            precio=precio,
            stock=stock,
            categoria=categoria,
            proveedor_id=proveedor_id
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        flash('Producto creado correctamente', 'success')
        return redirect(url_for('productos.lista_productos'))
    return render_template('crear_producto.html')

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = Producto.query.get_or_404(id)
    if request.method == 'POST':
        producto.name = request.form.get('name')
        producto.precio = request.form.get('precio')
        producto.stock = request.form.get('stock')
        producto.categoria = request.form.get('categoria')
        producto.proveedor_id = request.form.get('proveedor_id')
        db.session.commit()
        flash('Producto actualizado correctamente', 'success')
        return redirect(url_for('productos.lista_productos'))
    return render_template('editar_producto.html', producto=producto)

@bp.route('/eliminar/<int:id>', methods=['GET'])
def eliminar_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()
    flash('Producto eliminado correctamente', 'success')
    return redirect(url_for('productos.lista_productos'))
