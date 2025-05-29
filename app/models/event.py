import datetime

from pgvector.sqlalchemy import Vector
from app.configuration.config import Config
from app.extensions import db
from app.models.user import user_event_association

class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    embedding = db.Column(Vector(Config.VECTOR_DIM), nullable=True)

    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete = 'CASCADE'), nullable=False)
    organizer = db.relationship(
        'User',
        back_populates='organized_events'
    )

    participants = db.relationship(
        'User',
        secondary=user_event_association,
        back_populates='participating_events',
    )

    def __repr__(self):
        return f"<Event: {self.name} at {self.location}>"