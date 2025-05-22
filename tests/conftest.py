import pytest

from app import create_app, db
from app.models.event import Event
from app.models.user import User


@pytest.fixture
def app():
    app = create_app()
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db_session(app):
    with app.app_context():
        db.create_all()

        yield db.session

        db.session.remove()
        db.drop_all()


@pytest.fixture
def test_user():
    return User(
        name = "Mile",
        surname = "Stanislavov",
        email="test@example.com",
        password_hash="test_password"
    )


@pytest.fixture
def test_event(test_user):
    return Event(
        name="TestEvent",
        location="TestLocation",
        type="TestType",
        organizer=test_user
    )


@pytest.fixture
def init_data(db_session, test_user, test_event):
    """Insert one User and one Event, return their IDs."""
    db_session.add(test_user)
    db_session.add(test_event)
    db_session.commit()

    # Refresh the objects to ensure they're up to date
    db_session.refresh(test_user)
    db_session.refresh(test_event)

    return test_user.id, test_event.id