from dependency_injector.wiring import inject, Provide
from flask import request
from flask_restx import Namespace, Resource, fields

from app.container import Container
from app.models.user import User
from app.schemas import user_schema
from app.services.user_service import UserService

user_ns = Namespace("users", description="User based operations")


@user_ns.route("")
class UserBaseResource(Resource):
    @inject
    def get(self, user_service: UserService = Provide[Container.user_service]):
        """Get all users"""
        users = user_service.get_all_users()
        return user_schema.user_many.dump(users), 200

    user_create_input = user_ns.model('user_create_input', {
        'name': fields.String(required=True),
        'surname': fields.String(required=True),
        'email': fields.String(required=True),
        'password_hash': fields.String(required=True),
    })

    @user_ns.expect(user_create_input)
    @inject
    def post(self, user_service: UserService = Provide[Container.user_service]):
        """Create a new user"""
        data = request.get_json()
        user = User(**data)
        saved_user = user_service.save_user(user)
        return user_schema.user_single.dump(saved_user), 201

@user_ns.route("/<int:user_id>")
class SpecificUserResource(Resource):
    @inject
    def get(self, user_id: int, user_service: UserService = Provide[Container.user_service]):
        """Get a user by id"""
        user = user_service.get_user(user_id)
        return user_schema.user_single.dump(user), 200

    @inject
    def delete(self, user_id: int, user_service: UserService = Provide[Container.user_service]):
        """Delete a user by id"""
        user_service.delete_user(user_id)
        return {"message": "User deleted successfully"}, 200

