"""
Propósito: crear los formularios que se serviran para la creacion e interaccion de eventos
"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, DateField, TextAreaField
from wtforms.fields.datetime import DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import Event


class CreateEvent(FlaskForm):

    title = StringField('Título/nombre del evento: ', validators=[DataRequired(), Length(min=5, max=150)])
    start_time = DateField('Fecha de inicio: ', validators=[DataRequired()])
    end_time = DateField('Fecha de finalación: ', validators=[DataRequired()])
    description = TextAreaField('Descripción: ')
    location = StringField('Dirección')         # aca tengo que arreglaro, hay que normalizar la base de datos y hacer un campo calle/ciudad, etc
    submit = SubmitField('Crear evento')

class EditEvent(FlaskForm):
    title = StringField('Título/nombre del evento: ')
    start_time = DateField('Fecha de inicio: ', validators=[])
    end_time = DateField('Fecha de finalación: ', validators=[])
    description = TextAreaField('Descripción: ')
    location = StringField('Dirección')  # aca tengo que arreglaro, hay que normalizar la base de datos y hacer un campo calle/ciudad, etc
    submit = SubmitField('Actualizar evento')

class WriteComment(FlaskForm):

    content = TextAreaField('Deja un comentario: ', validators=[DataRequired(), Length(min=5, max=500)])
    submit = SubmitField('Enviar comentario')