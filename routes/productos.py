# routes/productos.py
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from services.productos_service import (
    get_all_productos,
    create_producto,
    update_producto,
    delete_producto
)
from models.producto import Producto  # Para obtener un objeto en vistas de edición
from models.proveedor import Proveedor

bp = Blueprint('productos', __name__, url_prefix='/productos')

# --- API REST Endpoints ---
@bp.route('/api', methods=['GET'])
def get_productos_api():
    productos = get_all_productos()
    return jsonify([producto.to_dict() for producto in productos])

@bp.route('/api', methods=['POST'])
def create_producto_api():
    data = request.get_json()
    nuevo = create_producto(
        name=data.get('name'),
        precio=data.get('precio'),
        stock=data.get('stock'),
        categoria=data.get('categoria'),
        proveedor_id=data.get('proveedor_id')
    )
    return jsonify(nuevo.to_dict()), 201

@bp.route('/api/<int:id>', methods=['PUT'])
def update_producto_api(id):
    data = request.get_json()
    actualizado = update_producto(
        id,
        name=data.get('name'),
        precio=data.get('precio'),
        stock=data.get('stock'),
        categoria=data.get('categoria'),
        proveedor_id=data.get('proveedor_id')
    )
    return jsonify(actualizado.to_dict())

@bp.route('/api/<int:id>', methods=['DELETE'])
def delete_producto_api(id):
    delete_producto(id)
    return jsonify({"message": "Producto eliminado"}), 204

# --- Vistas HTML ---
@bp.route('/lista', methods=['GET'])
def lista_productos():
    productos = get_all_productos()
    return render_template('productos/lista.html', productos=productos)

@bp.route('/crear', methods=['GET', 'POST'])
def crear_producto_view():
    proveedores = Proveedor.query.all()

    if request.method == 'POST':
        name = request.form['name']
        precio = request.form['precio']
        stock = request.form['stock']
        categoria = request.form['categoria']
        proveedor_id = request.form['proveedor_id']  # ahora es un ID

        create_producto(name, precio, stock, categoria, proveedor_id)
        return redirect(url_for('productos.lista_productos'))

    return render_template('productos/crear.html', proveedores=proveedores)

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_producto_view(id):
    producto = Producto.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form.get('name')
        precio = request.form.get('precio')
        stock = request.form.get('stock')
        categoria = request.form.get('categoria')
        proveedor_id = request.form.get('proveedor_id')
        update_producto(id, name, precio, stock, categoria, proveedor_id)
        flash('Producto actualizado correctamente', 'success')
        return redirect(url_for('productos.lista_productos'))
    return render_template('productos/editar.html', producto=producto)

@bp.route('/eliminar/<int:id>', methods=['GET'])
def eliminar_producto_view(id):
    delete_producto(id)
    flash('Producto eliminado correctamente', 'success')
    return redirect(url_for('productos.lista_productos'))

@bp.route("/catalogo")
def catalogo():
    lista_de_productos = get_all_productos()
    return render_template('productos/catalogo.html', products=lista_de_productos)
