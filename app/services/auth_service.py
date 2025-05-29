from werkzeug.security import generate_password_hash, check_password_hash

from app import extensions
from app.error_handler.exceptions import UserNotFound, Unauthorized
from app.models.user import User
from app.util.validaton_util import validate_user

auth = extensions.auth
db = extensions.db

@auth.verify_password
def verify_password(
    username: str,
    password: str
):
    user = User.query.filter_by(name=username).first()
    validate_user(user, UserNotFound(f"User not found with name: {username}"))
    check_password(user.password_hash, password)
    return user

def create_password_hash(password):
    return generate_password_hash(password)

def check_password(hashed_password, password):
    if not check_password_hash(hashed_password, password):
        raise Unauthorized("Password is incorrect, try again", 401)