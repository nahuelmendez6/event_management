"""
Proposito: Contiene las funciones que manejan las solicitudes HTTP
relacionadas con:
                - autenticacion
                - registro
                - inicio de sesion
                - cierre de sesion
"""
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import LoginForm, RegistrationForm
from .models import Users, Roles, UserRoles
from app.extensions import db
from . import auth_bp

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm() # Instancia del formulario de login
    if form.validate_on_submit():   # Si el formulario ha sido enviado, comenzamos con la logica de login
        user = Users.query.filter_by(username=form.username.data).first
        if user and Users.check_password(form.password.data):
            login_user(user)
            flash('Inicio de sesión exitoso.')
            return redirect(url_for('main.index'))
        else:
            flash('No se pudo iniciar sesion. Revisa tu usuario y/o contraseña') # si las credenciales no son validas largamos error

    return render_template('login.html', form=form)     # si el formulario no ha sido enviado el usuario es redirigido al login

@auth_bp.register('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()   # Instancia del formulario de registro
    if form.validate_on_submit():   # Si el formulario se ha enviado, procedemos al registro del usuarios
        if form.password.data != form.confirm_password.data:
            flash('Las contraseñas no coinciden')
            return redirect(url_for('auth.register'))
        password_hashed = generate_password_hash(form.password.data)
        user = Users(
            username= form.username.data,
            email = form.email.data,
            password = password_hashed,
            rol = form.rol.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Cuenta creada existosamente')
        return redirect(url_for('auth.login'))
    return render_template('register.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    pass
