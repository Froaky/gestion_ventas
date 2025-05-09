from flask import Flask, render_template
from config import Config
from models import db    # Asegurate de que models/__init__.py inicialice db = SQLAlchemy()
from flask_migrate import Migrate
from routes import register_blueprints  # Suponiendo que registrás blueprints en una función

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    register_blueprints(app)

    @app.route('/')
    def home():
        return render_template('home.html')

    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
