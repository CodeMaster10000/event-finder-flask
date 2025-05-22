from unittest.mock import MagicMock

import pytest
from sqlalchemy.exc import InvalidRequestError

from app.error_handler.exceptions import UserNotFound
from app.models.user import User
from app.services.user_service import UserService


@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def mock_bcrypt():
    # bcrypt isn’t used in these methods, but required by the ctor
    return MagicMock()


@pytest.fixture
def svc(mock_repo, mock_bcrypt):
    return UserService(repository=mock_repo, bcrypt=mock_bcrypt)


@pytest.fixture
def dummy_user():
    u = MagicMock(spec=User)
    u.id = 5
    u.name = "Alice"
    u.email = "alice@example.com"
    return u

def test_get_all_users_calls_repo(svc, mock_repo):
    mock_repo.get_all.return_value = ["u1", "u2"]
    result = svc.get_all_users()
    assert result == ["u1", "u2"]
    mock_repo.get_all.assert_called_once()

def test_get_user_success(svc, mock_repo, dummy_user):
    mock_repo.get_by_id.return_value = dummy_user
    result = svc.get_user(5)
    assert result is dummy_user
    mock_repo.get_by_id.assert_called_once_with(5)

def test_get_user_not_found_raises(svc, mock_repo):
    mock_repo.get_by_id.return_value = None
    with pytest.raises(UserNotFound) as exc:
        svc.get_user(99)
    assert "Does not exist for id: 99" in str(exc.value)

def test_get_user_by_email_success(svc, mock_repo, dummy_user):
    mock_repo.get_by_email.return_value = dummy_user
    result = svc.get_user_by_email("alice@example.com")
    assert result is dummy_user
    mock_repo.get_by_email.assert_called_once_with("alice@example.com")

def test_get_user_by_email_not_found_raises(svc, mock_repo):
    mock_repo.get_by_email.return_value = None
    with pytest.raises(UserNotFound) as exc:
        svc.get_user_by_email("bob@example.com")
    assert "Does not exist with this email: bob@example.com" in str(exc.value)

def test_save_user_success(svc, mock_repo, dummy_user):
    mock_repo.exists_by_name.return_value = False
    result = svc.save_user(dummy_user)
    mock_repo.save.assert_called_once_with(dummy_user)
    assert result is dummy_user

def test_save_user_name_exists_raises(svc, mock_repo, dummy_user):
    mock_repo.exists_by_name.return_value = True
    dummy_user.name = "ExistingName"
    with pytest.raises(InvalidRequestError) as exc:
        svc.save_user(dummy_user)
    assert "User with this name already exists: ExistingName" in str(exc.value)

def test_delete_user_calls_repo(svc, mock_repo):
    svc.delete_user(7)
    mock_repo.delete_by_id.assert_called_once_with(7)