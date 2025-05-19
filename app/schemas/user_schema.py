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

    # backref list of Events → pull each .id
    participating_events = fields.List(
        fields.Integer(attribute='id'),
        attribute='participating_events',
        dump_only=True,
    )

    # single related Event → pull its .id
    organized_event = fields.Integer(
        attribute='organized_event.id',
        dump_only=True,
    )


user_many = UserSchema(many=True)
user_single = UserSchema()
