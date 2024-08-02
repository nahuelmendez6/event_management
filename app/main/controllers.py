from flask import render_template
from app.main import main_blueprint

@main_blueprint.route('/')
def index():
    return render_template('index.html')