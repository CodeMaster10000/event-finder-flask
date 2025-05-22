from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from app.models.user import User


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        fields = (
            'id',
            'name',
            'surname',
            'email',
            'participating_events',
            'organized_event',
        )
        load_instance = True
        include_relationships = True

    id = auto_field()
    name = auto_field()
    surname = auto_field()
    email = auto_field()

    participating_events = fields.Method("get_participating_event_ids", dump_only=True)

    organized_event = fields.Method("get_organized_event_id", dump_only=True)

    def get_participating_event_ids(self, user):
        return [event.id for event in user.participating_events]

    def get_organized_event_id(self, user):
        return user.organized_event.id if user.organized_event else None

user_many = UserSchema(many=True)
user_single = UserSchema()
