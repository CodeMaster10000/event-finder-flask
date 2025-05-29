import os
from pathlib import Path

import pytest
from sqlalchemy import create_engine, text
from testcontainers.postgres import PostgresContainer
from werkzeug.security import generate_password_hash

from app import create_app
from app import db
from app.configuration.config import Config
from app.models.event import Event
from app.models.user import User
from app.util.embedding_util import create_embedded_text

username = "Mile"
password = "test_password"

@pytest.fixture(scope="session")
def pg_container():
    """
    Launch a Dockerized Postgres with pgvector pre-installed.
    """
    with PostgresContainer("pgvector/pgvector:pg15") as pg:
        root_url = pg.get_connection_url()
        root_engine = create_engine(root_url)
        with root_engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
            stmt = text("SELECT 1 FROM pg_database WHERE datname = :name")
            exists = conn.scalar(stmt, {"name": Config.DB_NAME})
            if not exists:
                conn.execute(text("CREATE DATABASE " + Config.DB_NAME + ";"))
        Config.SQLALCHEMY_DATABASE_URI = pg.get_connection_url()
        os.environ["DATABASE_URL"] = pg.get_connection_url()
        yield pg


@pytest.fixture(scope="session")
def app(pg_container):
    """
    Create a Flask app against the testcontainer’s Postgres,
    then run all Alembic migrations from the project’s migrations folder.
    """
    project_root = Path(__file__).resolve().parents[1]
    app = create_app(project_root / "migrations")
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
        name = username,
        surname = "Stanislavov",
        email="test@example.com",
        password_hash=generate_password_hash(password)
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

    embedding = create_embedded_text(test_event)
    test_event.embedding = embedding

    db_session.add(test_user)
    db_session.add(test_event)
    db_session.commit()

    db_session.refresh(test_user)
    db_session.refresh(test_event)

    return test_user.id, test_event.id