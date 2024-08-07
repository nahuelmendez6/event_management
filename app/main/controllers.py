from flask import render_template, redirect, url_for, flash
from app.main import main_blueprint, event_blueprint
from flask_login import login_required, current_user
from .models import Event, Coment
from .forms import CreateEvent, WriteComment, EditEvent
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
            category = form.category.data,
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


@event_blueprint.route('/user_events')
@login_required
def user_events():
    userEvents = Event.get_events_by_user(current_user.id)
    return render_template('user_event.html', events=userEvents)


@event_blueprint.route('/delete_event/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    event = Event.query.get(event_id)
    print(event)
    if event and event.user_id == current_user.id:
        Event.delete_event_by_id(event, event_id)
        return redirect(url_for('event.user_events'))
    else:
        # manejar el caso donde el evento no existe o no pertenece al usuario
        return redirect(url_for('main.index'))


@event_blueprint.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)

    if event.user_id != current_user.id:
        flash('No tienes permiso para modificar este evento.', 'danger')
        return redirect(url_for('event.user_events'))

    form = EditEvent()

    if form.validate_on_submit():
        event.update_event(
            title=form.title.data,
            category=form.category.data,
            start_time=form.start_time.data,
            end_time=form.end_time.data,
            description=form.description.data,
            location=form.location.data
        )
        flash('El evento ha sido actualizado con éxito.', 'succes')
        return redirect(url_for('event.user_events'))
    return render_template('edit_event.html', form=form)