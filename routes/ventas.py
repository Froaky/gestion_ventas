import datetime  # Asegúrate de importar el módulo datetime
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, flash
from models import db, Venta, Cliente, Producto

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
    productos = Producto.query.all()  # Para mostrar productos, si lo deseas
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

@bp.route('/')
def home():
    # Obtener los datos de los últimos 5 meses (puedes reemplazar los datos ficticios con consultas reales)
    labels, totals = get_ventas_ultimos_5_meses()
    return render_template('home.html', labels=labels, totals=totals)

def get_ventas_ultimos_5_meses():
    """
    Lógica para calcular los últimos 5 meses.
    Devuelve dos listas:
      - labels: nombres de cada mes (ej: "2023-12")
      - totals: totales de ventas para cada mes (datos ficticios en este ejemplo)
    """
    hoy = datetime.date.today()
    labels = []
    totals = []
    
    # Retrocede 4 meses + mes actual = 5 meses en total.
    for i in range(4, -1, -1):
        mes = hoy.month - i
        year = hoy.year
        while mes <= 0:
            mes += 12
            year -= 1

        mes_str = f"{year}-{mes:02d}"
        labels.append(mes_str)
        
        # Lógica ficticia: reemplaza con tu consulta real.
        total_ventas = 1000 + i * 50  # Datos ficticios
        totals.append(total_ventas)

    return labels, totals
