from flask import render_template, redirect, url_for
from app.main import main_blueprint, event_blueprint
from flask_login import login_required
from .models import Event, Coment
from .forms import CreateEvent, WriteComment
from flask_login import current_user
from app.extensions import db
@main_blueprint.route('/')
def index():
    return render_template('index.html')

@event_blueprint.route('/create_event')
@login_required
def create_event():
    return render_template('new_event.html')

@event_blueprint.route('/new_event', methods=['GET', 'POST'])
@login_required
def new_event():

    form = CreateEvent()
    if form.validate_on_submit():
        newEvent = Event(
            title = form.title.data,
            start_time = form.start_time.data,
            end_time = form.end_time.data,
            description = form.description.data,
            location = form.location.data,
            user_id = current_user.id
        )
        db.session.add(newEvent)
        db.session.commit()
        return redirect(url_for('main.index'))

    return render_template('new_event.html', form=form)

