from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import rq

# Database initialization
db = SQLAlchemy()


def create_app():
    app = Flask(__name__, template_folder='./templates', static_folder='./static')
    app.config.from_object(Config)
    migrate = Migrate(app, db)
    db.init_app(app)

    with app.app_context():
        from .main.routes import bp as main_bp
        from .pizzas.routes import bp as pizzas_bp
        from .pizzas.edit_routes import bp as edit_pizzas_bp
        from .toppings.routes import bp as toppings_bp
        from .error.routes import bp as error_bp

        db.create_all()

        app.register_blueprint(main_bp, url_prefix='/')
        app.register_blueprint(pizzas_bp, url_prefix='/pizzas')
        app.register_blueprint(edit_pizzas_bp, url_prefix='/edit-pizza')
        app.register_blueprint(toppings_bp, url_prefix='/pizza-toppings')
        app.register_blueprint(error_bp, url_prefix='/error')

    return app
