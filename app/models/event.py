import datetime

from app.extensions import db
from app.models.user import user_event_association

class Event(db.Model):
    __tablename__ = 'event'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())

    organizer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    organizer = db.relationship(
        'User',
        back_populates='organized_event'
    )

    participants = db.relationship(
        'User',
        secondary=user_event_association,
        back_populates='participating_events',
    )

    def __repr__(self):
        return f"<Event: {self.name} at {self.location}>"