# routes/proveedores.py
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from services.proveedores_service import (
    get_all_proveedores,
    create_proveedor,
    update_proveedor,
    delete_proveedor
)
from models.proveedor import Proveedor  # Para obtener un objeto en vistas de edición

bp = Blueprint('proveedores', __name__, url_prefix='/proveedores')

# --- API REST Endpoints ---
@bp.route('/api', methods=['GET'])
def get_proveedores_api():
    proveedores = get_all_proveedores()
    return jsonify([p.to_dict() for p in proveedores])

@bp.route('/api', methods=['POST'])
def create_proveedor_api():
    data = request.get_json()
    nuevo = create_proveedor(
        name=data.get('name'),
        telefono=data.get('telefono')
    )
    return jsonify(nuevo.to_dict()), 201

# --- Vistas HTML ---
@bp.route('/lista', methods=['GET'])
def lista_proveedores():
    proveedores = get_all_proveedores()
    return render_template('proveedores/lista.html', proveedores=proveedores)

@bp.route('/crear', methods=['GET', 'POST'])
def crear_proveedor_view():
    if request.method == 'POST':
        name = request.form.get('name')
        telefono = request.form.get('telefono')
        create_proveedor(name, telefono)
        flash('Proveedor creado correctamente', 'success')
        return redirect(url_for('proveedores.lista_proveedores'))
    return render_template('proveedores/crear.html')

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_proveedor_view(id):
    proveedor = Proveedor.query.get_or_404(id)
    if request.method == 'POST':
        name = request.form.get('name')
        telefono = request.form.get('telefono')
        update_proveedor(id, name, telefono)
        flash('Proveedor actualizado correctamente', 'success')
        return redirect(url_for('proveedores.lista_proveedores'))
    return render_template('proveedores/editar.html', proveedor=proveedor)

@bp.route('/eliminar/<int:id>', methods=['GET'])
def eliminar_proveedor_view(id):
    delete_proveedor(id)
    flash('Proveedor eliminado correctamente', 'success')
    return redirect(url_for('proveedores.lista_proveedores'))

@bp.route('/buscar', methods=['GET', 'POST'])
def buscar_proveedor_view():
    resultados = []
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        # Ejemplo de búsqueda usando ilike
        from models.proveedor import Proveedor
        resultados = Proveedor.query.filter(Proveedor.name.ilike(f"%{nombre}%")).all()
    return render_template('proveedores/buscar.html', resultados=resultados)
