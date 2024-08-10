from flask import render_template, redirect, url_for, flash, request
from app.main import main_blueprint, event_blueprint
from flask_login import login_required, current_user
from .models import Event, Coment, EventRegistration
from .forms import CreateEvent, WriteComment, EditEvent
from flask_login import current_user
from app.extensions import db


@main_blueprint.route('/')
def index():

    # Obtener todas las categorias para usarlas en el formulario de filtrado
    categories = Event.get_all_categories()

    # Obtener la categoria seleccionada desde los parametros de la URL
    category = request.args.get('category')

    # si se ha seleccionado una categoria, filtrar por ella
    if category:
        events = Event.query.filter_by(category=category).order_by(Event.start_time.asc()).all()
    else:
        events = Event.query.order_by(Event.start_time.asc()).limit(10).all()

    return render_template('index.html', events=events, categories=categories, selected_category=category)


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

@event_blueprint.route('/event_detail/<int:event_id>', methods=['GET', 'POST'])
@login_required
def show_detail(event_id):

    event = Event.query.get_or_404(event_id)
    if event:
        return render_template('event_detail.html', event=event)

@event_blueprint.route('/event_registration/<int:event_id>', methods=['GET', 'POST'])
@login_required
def registration(event_id):

    event = Event.query.get_or_404(event_id)

    if EventRegistration.check_registration(current_user.id, event.id):
        flash('Ya estas inscripto en este evento.', 'warning')
    else:
        new_registration = EventRegistration(
            user_id=current_user.id,
            event_id=event.id
        )
        db.session.add(new_registration)
        db.session.commit()
        flash('Te has inscrito en el evento con éxito.', 'success')
        return redirect(url_for('main.index'))

    return  redirect(url_for('main.index'))

@event_blueprint.route('/event_cancel_registration/<int:event_id>', methods=['GET', 'POST'])
@login_required
def cancel_registration(event_id):

    event = Event.query.get_or_404(event_id)

    if EventRegistration.check_registration(current_user.id, event.id):
        EventRegistration.delete_registration(event, current_user.id, event.id)
        return redirect(url_for('main.index'))
    else:
        flash('No estas registrado en este evento')

