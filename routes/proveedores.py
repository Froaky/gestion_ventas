from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from models import db, Proveedor

bp = Blueprint('proveedores', __name__, url_prefix='/proveedores')

# --- API REST Endpoints ---
@bp.route('/api', methods=['GET'])
def get_proveedores_api():
    proveedores = Proveedor.query.all()
    return jsonify([proveedor.to_dict() for proveedor in proveedores])

@bp.route('/api', methods=['POST'])
def create_proveedor_api():
    data = request.get_json()
    nuevo_proveedor = Proveedor(
        name=data.get('name'),
        telefono=data.get('telefono')
    )
    db.session.add(nuevo_proveedor)
    db.session.commit()
    return jsonify(nuevo_proveedor.to_dict()), 201

# --- Vistas HTML ---
@bp.route('/lista', methods=['GET'])
def lista_proveedores():
    proveedores = Proveedor.query.all()
    return render_template('proveedores.html', proveedores=proveedores)

@bp.route('/crear', methods=['GET', 'POST'])
def crear_proveedor():
    if request.method == 'POST':
        name = request.form.get('name')
        telefono = request.form.get('telefono')
        nuevo_proveedor = Proveedor(name=name, telefono=telefono)
        db.session.add(nuevo_proveedor)
        db.session.commit()
        flash('Proveedor creado correctamente', 'success')
        return redirect(url_for('proveedores.lista_proveedores'))
    return render_template('crear_proveedor.html')

@bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    if request.method == 'POST':
        proveedor.name = request.form.get('name')
        proveedor.telefono = request.form.get('telefono')
        db.session.commit()
        flash('Proveedor actualizado correctamente', 'success')
        return redirect(url_for('proveedores.lista_proveedores'))
    return render_template('editar_proveedor.html', proveedor=proveedor)

@bp.route('/eliminar/<int:id>', methods=['GET'])
def eliminar_proveedor(id):
    proveedor = Proveedor.query.get_or_404(id)
    db.session.delete(proveedor)
    db.session.commit()
    flash('Proveedor eliminado correctamente', 'success')
    return redirect(url_for('proveedores.lista_proveedores'))
