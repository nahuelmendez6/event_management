from flask import Blueprint

main_blueprint = Blueprint('main', __name__)
event_blueprint = Blueprint('event', __name__)

from app.main import controllers