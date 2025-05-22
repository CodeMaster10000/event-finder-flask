from unittest.mock import MagicMock
import pytest
from app.error_handler.exceptions import AppException
from app.services.app_service import AppService


@pytest.fixture
def mock_event():
    mock = MagicMock()
    mock.participants = []
    return mock


@pytest.fixture
def mock_user():
    return MagicMock()


@pytest.fixture
def mock_event_repo():
    return MagicMock()


@pytest.fixture
def mock_user_repo():
    return MagicMock()


@pytest.fixture
def app_service(mock_event_repo, mock_user_repo):
    return AppService(mock_event_repo, mock_user_repo)


def test_add_participant_success(app_service, mock_event_repo, mock_user_repo, mock_event, mock_user):
    mock_event_repo.get_by_id.return_value = mock_event
    mock_user_repo.get_by_id.return_value = mock_user

    result = app_service.add_participant(event_id=1, user_id=2)

    assert mock_user in mock_event.participants
    mock_event_repo.save.assert_called_once_with(mock_event)
    assert result == mock_event


def test_add_participant_already_exists(app_service, mock_event_repo, mock_user_repo, mock_event, mock_user):
    mock_event.participants = [mock_user]
    mock_event_repo.get_by_id.return_value = mock_event
    mock_user_repo.get_by_id.return_value = mock_user

    with pytest.raises(AppException) as exc:
        app_service.add_participant(event_id=1, user_id=2)

    assert "already participating" in str(exc.value)


def test_remove_participant_success(app_service, mock_event_repo, mock_user_repo, mock_event, mock_user):
    mock_event.participants = [mock_user]
    mock_event_repo.get_by_id.return_value = mock_event
    mock_user_repo.get_by_id.return_value = mock_user

    result = app_service.remove_participant(event_id=1, user_id=2)

    assert mock_user not in mock_event.participants
    mock_event_repo.save.assert_called_once_with(mock_event)
    assert result == mock_event


def test_remove_participant_not_found(app_service, mock_event_repo, mock_user_repo, mock_event, mock_user):
    mock_event.participants = []
    mock_event_repo.get_by_id.return_value = mock_event
    mock_user_repo.get_by_id.return_value = mock_user

    with pytest.raises(AppException) as exc:
        app_service.remove_participant(event_id=1, user_id=2)

    assert "not participating" in str(exc.value)
