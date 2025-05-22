from app.extensions import db

# user - event MtM db association
user_event_association = db.Table(
    'user_event',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('event_id', db.Integer, db.ForeignKey('event.id')))

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    # Relationships
    organized_events = db.relationship(
        'Event',
        back_populates='organizer',
        cascade='all',
        passive_deletes=True
    )

    participating_events = db.relationship(
        'Event',
        secondary=user_event_association,
        back_populates='participants')

    def __repr__(self):
        return f"<User: {self.name}, email: {self.email}>"