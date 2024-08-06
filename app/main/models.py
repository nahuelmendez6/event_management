from app.extensions import db
from datetime import date, datetime

"""
Propósito: Definir los modelos (clases) que manejaran la lógica de creación
de eventos.
"""

class Event(db.Model):

    __tablename__ = "events"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(255), nullable=False)
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

    def update_event(self, title=None, start_time=None, end_time=None, description=None, location=None):
        if title is not None:
            self.title = title
        if start_time is not None:              # tengo que solucionar este problema
            self.start_time = start_time
        if end_time is not None:
            self.end_time = end_time
        if description is not None:
            self.description = description
        if location is not None:
            self.location = location
        db.session.commit()


class Coment(db.Model):

    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=True)

