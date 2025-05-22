from abc import ABC

from app.error_handler.exceptions import UserNotFound, AppException
from app.models.user import User
from app.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository, ABC):
    def __init__(self, session):
        self.session = session

    def get_by_id(self, user_id: int) -> User:
        return self.session.get(User, user_id)

    def get_by_email(self, email: str) -> User:
        return self.session.filter_by(email=email).first()

    def get_by_name(self, name: str) -> User:
        return self.session.filter_by(name=name).first()

    def get_all(self):
        return self.session.query(User).all()

    def save(self, user: User):
        self.session.add(user)
        self.session.commit()
        return user

    def delete_by_id(self, user_id: int):
        user = self.get_by_id(user_id)
        if not user:
            raise UserNotFound(f"User with id {user_id} not found")
        self.session.delete(user)
        try:
            self.session.commit()
        except BaseException as e:
            raise AppException(f"Could not delete user, {e}", 500)

    def exists_by_id(self, user_id):
        return (self.session.query(User)
                .filter_by(id=user_id)
                .first()
                is not None)

    def exists_by_name(self, name):
        return (self.session.query(User)
                .filter_by(name=name)
                .first()
                is not None)
