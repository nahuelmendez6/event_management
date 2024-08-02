from flask import Flask
from .config import Config
from .extensions import db, migrate, login_manager
#from .routes import register_blueprints
from app.auth import auth_bp
from app.main import main_blueprint
from .auth.models import Users
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Funcion user_loader
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    # Registrar blueprints
    #register_blueprints(app)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_bp, url_prefix='/auth')

    return app