from .clientes import bp as clientes_bp
from .productos import bp as productos_bp
from .proveedores import bp as proveedores_bp
from .ventas import bp as ventas_bp

def register_blueprints(app):
    app.register_blueprint(clientes_bp)
    app.register_blueprint(productos_bp)
    app.register_blueprint(proveedores_bp)
    app.register_blueprint(ventas_bp)
