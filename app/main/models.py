from app.extensions import db
from app.auth.models import Users
from datetime import date, datetime

"""
Propósito: Definir los modelos (clases) que manejaran la lógica de creación
de eventos.
"""

class Event(db.Model):

    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @classmethod
    def get_events_by_user(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    def delete_event_by_id(self, event_id):
        event = self.query.get(event_id)
        if event:
            db.session.delete(event)
            db.session.commit()
            return True
        return False

    def update_event(self, title=None, category=None,start_time=None, end_time=None, description=None, location=None):
        if title is not None:
            self.title = title
        if category is not None:
            self.category = category
        if start_time is not None:              # tengo que solucionar este problema
            self.start_time = start_time
        if end_time is not None:
            self.end_time = end_time
        if description is not None:
            self.description = description
        if location is not None:
            self.location = location
        db.session.commit()

    @classmethod
    def get_all_categories(cls):
        return db.session.query(cls.category).distinct().all()

class EventRegistration(db.Model):

    __tablename__ = 'event_registration'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    user = db.relationship('Users', backref=db.backref('event_registration', lazy=True))
    event = db.relationship('Event', backref=db.backref('event_registration', lazy=True))

    @staticmethod
    def check_registration(user_id, event_id):

        # Busca si existe una inscripcion con user_idy event_id proporcionados
        registration = db.session.query(EventRegistration).filter_by(user_id=user_id, event_id=event_id).first()

        return registration is not None

    def delete_registration(self, user_id,event_id):
        registration = EventRegistration.query.filter_by(user_id=user_id, event_id=event_id).first()

        if registration:
            db.session.delete(registration)
            db.session.commit()
            return True
        return False


class Coment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=True)

