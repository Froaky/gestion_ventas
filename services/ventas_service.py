
import datetime
from sqlalchemy import cast, DateTime
from models import db
from models.venta import Venta
from models.producto import Producto  # si no está ya importado
from models.producto_venta import VentaProducto

def get_all_ventas():
    return Venta.query.all()

def create_venta(cliente_id, total, productos_seleccionados):
    nueva_venta = Venta(cliente_id=cliente_id, total=total)
    db.session.add(nueva_venta)

    for item in productos_seleccionados:
        producto_id = item.get('producto_id')
        cantidad = item.get('cantidad')

        producto = Producto.query.get(producto_id)
        if not producto:
            raise ValueError(f"Producto con ID {producto_id} no encontrado.")

        if producto.stock is None:
            raise ValueError(f"El producto '{producto.name}' no tiene stock definido.")

        if producto.stock < cantidad:
            raise ValueError(f"Stock insuficiente para el producto '{producto.name}'. Stock disponible: {producto.stock}, solicitado: {cantidad}")

        venta_producto = VentaProducto(
            venta=nueva_venta,
            producto=producto,
            cantidad=cantidad,
            precio_unitario=producto.precio
        )
        db.session.add(venta_producto)
        producto.stock -= cantidad

    db.session.commit()
    return nueva_venta



def update_venta(id, cliente_id, total):
    venta = Venta.query.get_or_404(id)
    venta.cliente_id = cliente_id
    venta.total = total
    db.session.commit()
    return venta

def delete_venta(id):
    venta = Venta.query.get_or_404(id)
    db.session.delete(venta)
    db.session.commit()


def get_ventas_ultimos_5_meses():
    """
    Calcula los totales y la cantidad (número) de ventas para cada uno de los últimos 5 meses.
    Devuelve tres listas:
      - labels: nombres de cada mes en formato "YYYY-MM"
      - totals: suma total de ventas en dólares para cada mes
      - counts: cantidad de ventas registradas en cada mes
    Se utiliza datetime.datetime y se fuerza el cast del campo fecha a DateTime.
    """
    hoy = datetime.datetime.today()  # Incluye fecha y hora
    labels = []
    totals = []
    counts = []
    
    # Retroceder 4 meses + mes actual = 5 meses
    for i in range(4, -1, -1):
        mes = hoy.month - i
        year = hoy.year
        while mes <= 0:
            mes += 12
            year -= 1

        mes_str = f"{year}-{mes:02d}"
        labels.append(mes_str)
        
        # Calcular las fechas de inicio y fin para el mes usando datetime
        inicio_mes = datetime.datetime(year, mes, 1)
        if mes == 12:
            fin_mes = datetime.datetime(year + 1, 1, 1)
        else:
            fin_mes = datetime.datetime(year, mes + 1, 1)
        
        # Forzar la conversión de Venta.fecha a DateTime con cast
        ventas_mes = Venta.query.filter(
            cast(Venta.fecha, DateTime) >= inicio_mes,
            cast(Venta.fecha, DateTime) < fin_mes
        ).all()
        
        total_mes = sum(venta.total for venta in ventas_mes)
        count_mes = len(ventas_mes)
        
        totals.append(total_mes)
        counts.append(count_mes)
        
    return labels, totals, counts
