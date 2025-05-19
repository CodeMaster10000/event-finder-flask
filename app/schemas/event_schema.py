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
            'participants',
        )
        load_instance = True
        include_relationships = True

    id = auto_field()
    name = auto_field()
    location = auto_field()
    time = auto_field()

    # grab the related User.name
    organizer_name = fields.String(
        attribute='organizer.name',
        dump_only=True,
    )

    # for each User in .participants, grab .name
    participants = fields.List(
        fields.String(attribute='name'),
        attribute='participants',
        dump_only=True,
    )


event_many = EventSchema(many=True)
event_single = EventSchema()
