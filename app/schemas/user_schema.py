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
            'organized_events',
        )
        load_instance = True
        include_relationships = True

    id = auto_field()
    name = auto_field()
    surname = auto_field()
    email = auto_field()

    participating_events = fields.Method("get_participating_events", dump_only=True)

    organized_events = fields.Method("get_organized_events", dump_only=True)

    def get_participating_events(self, user):
        return [event.name for event in user.participating_events]

    def get_organized_events(self, user):
        return [event.name for event in user.organized_events]

user_many = UserSchema(many=True)
user_single = UserSchema()
