from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from .cliente import Cliente
from .proveedor import Proveedor
from .producto import Producto
from .venta import Venta
