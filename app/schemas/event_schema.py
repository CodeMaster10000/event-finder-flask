from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from app.models.event import Event


class EventSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Event
        fields = (
            'id',
            'name',
            'location',
            'time',
            'organizer_name',
            'type',
            'participants',
        )
        load_instance = True
        include_relationships = True

    id = auto_field()
    name = auto_field()
    location = auto_field()
    time = auto_field()
    type = auto_field()

    organizer_name = fields.Method('get_organizer_name', dump_only=True)
    participants = fields.Method('get_participant_names', dump_only=True)

    def get_organizer_name(self, event):
        return event.organizer.name if event.organizer else None

    def get_participant_names(self, event):
        return [user.name for user in event.participants]


event_many = EventSchema(many=True)
event_single = EventSchema()
