from sqlalchemy.exc import InvalidRequestError

from app.error_handler.exceptions import UserNotFound
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.services.auth_service import create_password_hash
from app.util.validaton_util import validate_user


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def get_all_users(self):
        return self.user_repository.get_all()

    def get_user(self, user_id: int) -> User:
        user = self.user_repository.get_by_id(user_id)
        validate_user(user, UserNotFound(f"Does not exist for id: {user_id}"))
        return user

    def get_user_by_email(self, email: str) -> User:
        user = self.user_repository.get_by_email(email)
        validate_user(user, UserNotFound(f"Does not exist with this email: {email}"))
        return user

    def save_user(self, user: User):
        if self.user_repository.exists_by_name(user.name):
            raise InvalidRequestError(f"User with this name already exists: {user.name}")
        user.password_hash = create_password_hash(user.password_hash)
        self.user_repository.save(user)
        return user

    def delete_user(self, user_id: int):
        self.user_repository.delete_by_id(user_id)

    def get_user_by_name(self, username):
        user = self.user_repository.get_by_name(username)
        validate_user(user, UserNotFound(f"Does not exist with this name: {username}"))
        return user
