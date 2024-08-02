from app.main import main_blueprint as main_blueprint
from app.auth import auth_bp as auth_blueprint


def register_blueprints(app):
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint)
