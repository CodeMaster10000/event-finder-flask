import pytest
from unittest.mock import MagicMock
from sqlalchemy.exc import InvalidRequestError

from app.error_handler.exceptions import UserNotFound, EventNotFound
from app.models.event import Event
from app.models.user import User
from app.services.event_service import EventService

@pytest.fixture
def mock_repo():
    return MagicMock(spec=['get_all', 'get_by_id', 'exists_by_name', 'save', 'delete_by_id'])

@pytest.fixture
def mock_user_repo():
    return MagicMock(spec=['get_by_id'])

@pytest.fixture
def svc(mock_repo, mock_user_repo):
    return EventService(event_repository=mock_repo, user_repository=mock_user_repo)

@pytest.fixture
def dummy_user():
    u = MagicMock(spec=User)
    u.id = 10
    u.name = "Organizer"
    return u

@pytest.fixture
def dummy_event():
    e = MagicMock(spec=Event)
    e.id = 20
    e.name = "MyEvent"
    e.location = "Loc"
    e.type = "Type"
    return e

def test_get_all_events_calls_repo(svc, mock_repo):
    mock_repo.get_all.return_value = ["e1", "e2"]
    result = svc.get_all_events()
    assert result == ["e1", "e2"]
    mock_repo.get_all.assert_called_once()

def test_get_event_success(svc, mock_repo, dummy_event):
    mock_repo.get_by_id.return_value = dummy_event
    result = svc.get_event(20)
    assert result is dummy_event
    mock_repo.get_by_id.assert_called_once_with(20)

def test_get_event_not_found_raises(svc, mock_repo):
    mock_repo.get_by_id.return_value = None
    with pytest.raises(EventNotFound) as exc:
        svc.get_event(99)
    assert "Event not found for id: 99" in str(exc.value)

def test_create_event_success(svc, mock_repo, mock_user_repo, dummy_event, dummy_user):
    # Setup: organizer exists, no duplicate name
    mock_user_repo.get_by_id.return_value = dummy_user
    mock_repo.exists_by_name.return_value = False
    # The repository.save should return the event passed
    mock_repo.save.side_effect = lambda ev: ev

    # Call with a prototype Event
    proto = MagicMock(spec=Event)
    proto.name = "NewName"
    proto.location = "NewLoc"
    proto.type = "NewType"

    saved = svc.create_event(organizer_id=10, event=proto)

    # The returned Event must have correct fields
    assert isinstance(saved, Event)
    assert saved.name == "NewName"
    assert saved.location == "NewLoc"
    assert saved.type == "NewType"
    assert saved.organizer_id == 10

    mock_user_repo.get_by_id.assert_called_once_with(10)
    mock_repo.exists_by_name.assert_called_once_with("NewName")
    mock_repo.save.assert_called_once()

def test_create_event_user_not_found(svc, mock_repo, mock_user_repo, dummy_event):
    mock_user_repo.get_by_id.return_value = None
    proto = MagicMock(spec=Event, name="X", location="L", type="T")
    with pytest.raises(UserNotFound) as exc:
        svc.create_event(organizer_id=123, event=proto)
    assert "Organizer not found with id: 123" in str(exc.value)

def test_create_event_duplicate_name_raises(svc, mock_repo, mock_user_repo, dummy_event, dummy_user):
    mock_user_repo.get_by_id.return_value = dummy_user
    mock_repo.exists_by_name.return_value = True
    proto = MagicMock(spec=Event)
    proto.name = "Dup"
    with pytest.raises(InvalidRequestError) as exc:
        svc.create_event(organizer_id=10, event=proto)
    assert "Event with name already exists: Dup" in str(exc.value)

def test_delete_event_success(svc, mock_repo, dummy_event):
    # get_event called internally by delete, so stub get_by_id
    mock_repo.get_by_id.return_value = dummy_event
    svc.delete_event(20)
    mock_repo.delete_by_id.assert_called_once_with(20)

def test_delete_event_not_found_raises(svc, mock_repo):
    mock_repo.get_by_id.return_value = None
    with pytest.raises(EventNotFound) as exc:
        svc.delete_event(77)
    assert "Event not found for id: 77" in str(exc.value)
