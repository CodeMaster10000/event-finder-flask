from unittest.mock import MagicMock

import pytest

from app.error_handler.exceptions import UserNotFound
from app.models.user import User
from app.repositories.user_repository import UserRepository


@pytest.fixture
def mock_session():
    return MagicMock()


@pytest.fixture
def repo(mock_session):
    return UserRepository(session=mock_session)


def test_get_by_id_calls_session_get(repo, mock_session):
    repo.get_by_id(123)
    mock_session.get.assert_called_once_with(User, 123)


def test_get_by_email_calls_filter_and_first(repo, mock_session):
    # Arrange
    query = MagicMock()
    mock_session.filter_by.return_value = query
    query.first.return_value = "some_user"

    # Act
    result = repo.get_by_email("a@b.com")

    # Assert
    mock_session.filter_by.assert_called_once_with(email="a@b.com")
    query.first.assert_called_once()
    assert result == "some_user"


def test_get_all_calls_query_all(repo, mock_session):
    query = MagicMock()
    mock_session.query.return_value = query
    query.all.return_value = ["u1", "u2"]

    result = repo.get_all()

    mock_session.query.assert_called_once_with(User)
    query.all.assert_called_once()
    assert result == ["u1", "u2"]


def test_save_adds_and_commits_and_returns_user(repo, mock_session):
    user = User()
    # Act
    returned = repo.save(user)

    # Assert
    mock_session.add.assert_called_once_with(user)
    mock_session.commit.assert_called_once()
    assert returned is user


def test_delete_by_id_success(repo, mock_session):
    # Arrange: session.get returns a user
    existing = User()
    mock_session.get.return_value = existing

    # Act
    repo.delete_by_id(5)

    # Assert
    mock_session.get.assert_called_once_with(User, 5)
    mock_session.delete.assert_called_once_with(existing)
    mock_session.commit.assert_called_once()


def test_delete_by_id_not_found_raises(repo, mock_session):
    # Arrange: session.get returns None
    mock_session.get.return_value = None

    # Act & Assert
    with pytest.raises(UserNotFound) as exc:
        repo.delete_by_id(99)
    assert "User with id 99 not found" in str(exc.value)
    # commit/delete should not be called
    mock_session.delete.assert_not_called()
    mock_session.commit.assert_not_called()


def test_exists_by_id_true(repo, mock_session):
    query = MagicMock()
    mock_session.query.return_value = query
    query.filter_by.return_value = query
    query.first.return_value = User()

    assert repo.exists_by_id(7) is True
    mock_session.query.assert_called_once_with(User)
    query.filter_by.assert_called_once_with(id=7)
    query.first.assert_called_once()


def test_exists_by_id_false(repo, mock_session):
    query = MagicMock()
    mock_session.query.return_value = query
    query.filter_by.return_value = query
    query.first.return_value = None

    assert repo.exists_by_id(8) is False


def test_exists_by_name_true(repo, mock_session):
    query = MagicMock()
    mock_session.query.return_value = query
    query.filter_by.return_value = query
    query.first.return_value = User()

    assert repo.exists_by_name("Alice") is True
    mock_session.query.assert_called_once_with(User)
    query.filter_by.assert_called_once_with(name="Alice")
    query.first.assert_called_once()


def test_exists_by_name_false(repo, mock_session):
    query = MagicMock()
    mock_session.query.return_value = query
    query.filter_by.return_value = query
    query.first.return_value = None

    assert repo.exists_by_name("Bob") is False
