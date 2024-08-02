from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import Users, UserRoles

class RegistrationForm(FlaskForm):

    username = StringField('Nombre de usuario', validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=8, max=16)])
    confirm_password = PasswordField('Confirma contraseña', validators=[DataRequired(), Length(min=8, max=16)])
    rol = SelectField('Rol', choices=[('user', 'User'), ('admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Registrate')

    def validate_username(self, username):
        """
        :param username:
        :return: Si el username es incorrecto (ya esta registrado) esta funcion
        devuelve un error
        """

        user = Users.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Nombre de usuario no disponible. Elige uno diferente')

    def validate_email(self, email):
        """
        :param email:
        :return: Si el email es incorrecto (ya esta registrado) esta funcion
        devuelve un error
        """

        user = Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email no disponible. Elige uno diferente')


class LoginForm(FlaskForm):

    username = StringField('Nombre de usuario', validators=[DataRequired()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Ingresar')