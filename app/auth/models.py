"""
Propósito: Definir los módulos que manejaran la lógica de la gestion
y auntenticacion de usuarios
"""

from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime
class Users(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    rol = db.Column(db.Enum, default='user')

    def set_password(self, password_hash):
        self.password_hash = generate_password_hash(password_hash)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Roles(db.Model):

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key = True)
    role_name = db.Column(db.String(50), default='user')

class UserRoles(db.Model):

    __tablename__ = 'user_roles'

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), primary_key=True ,nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), primary_key=True, nullable=False)
