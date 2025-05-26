from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

from app.error_handler.exceptions import UserNotFound, Unauthorized
from app.repositories.user_repository import UserRepository
from app.util.validaton_util import validate_user

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password, repository: UserRepository):
    user = repository.get_by_name(username)
    validate_user(user, UserNotFound(f"User not found with name: {username}"))
    check_password(user.password_hash, password)
    return user

def create_password_hash(password):
    return generate_password_hash(password)


def check_password(hashed_password, password):
     if not check_password_hash(hashed_password, password):
         raise Unauthorized("Password is incorrect, try again", 401)
