from flask_bcrypt import Bcrypt
from sqlalchemy.exc import InvalidRequestError

from app.error_handler.exceptions import UserNotFound
from app.models.user import User
from app.repositories.user_repository import UserRepository


def validate_user(user, exc):
    if user is None:
        raise exc

class UserService:
    def __init__(self, repository: UserRepository, bcrypt: Bcrypt):
        self.repository = repository
        self.bcrypt = bcrypt

    def get_all_users(self):
        return self.repository.get_all()

    def get_user(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)
        validate_user(user, UserNotFound(f"Does not exist for id: {user_id}"))
        return user

    def get_user_by_email(self, email: str) -> User:
        user = self.repository.get_by_email(email)
        validate_user(user, UserNotFound(f"Does not exist with this email: {email}"))
        return user

    def save_user(self, user: User):
        if self.repository.exists_by_name(user.name):
            raise InvalidRequestError(f"User with this name already exists: {user.name}")
        self.repository.save(user)
        return user

    def delete_user(self, user_id: int):
        self.repository.delete_by_id(user_id)