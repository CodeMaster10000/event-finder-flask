import pytest
from unittest.mock import MagicMock

from app.repositories.event_repository import EventRepository
from app.error_handler.exceptions import EventNotFound
from app.models.event import Event

@pytest.fixture
def mock_session():
    return MagicMock()

@pytest.fixture
def repo(mock_session):
    return EventRepository(session=mock_session)

def test_get_by_id_calls_session_get(repo, mock_session):
    repo.get_by_id(123)
    mock_session.get.assert_called_once_with(Event, 123)

def test_get_by_name_calls_filter_and_first(repo, mock_session):
    query = MagicMock()
    mock_session.filter_by.return_value = query
    query.first.return_value = "evt"

    result = repo.get_by_name("MyEvent")

    mock_session.filter_by.assert_called_once_with(name="MyEvent")
    query.first.assert_called_once()
    assert result == "evt"

def test_get_all_calls_query_all(repo, mock_session):
    query = MagicMock()
    mock_session.query.return_value = query
    query.all.return_value = ["e1", "e2"]

    result = repo.get_all()

    mock_session.query.assert_called_once_with(Event)
    query.all.assert_called_once()
    assert result == ["e1", "e2"]

def test_save_adds_and_commits_and_returns_event(repo, mock_session):
    evt = Event()
    returned = repo.save(evt)

    mock_session.add.assert_called_once_with(evt)
    mock_session.commit.assert_called_once()
    assert returned is evt

def test_delete_by_id_success(repo):
    existing = Event()
    repo.get_by_id = MagicMock(return_value=existing)

    repo.delete_by_id(5)

    repo.get_by_id.assert_called_once_with(5)
    repo.session.delete.assert_called_once_with(existing)
    repo.session.commit.assert_called_once()

def test_delete_by_id_not_found_raises(repo):
    repo.get_by_id = MagicMock(return_value=None)

    with pytest.raises(EventNotFound) as exc:
        repo.delete_by_id(99)
    assert "Event with id 99 not found" in str(exc.value)

    repo.session.delete.assert_not_called()
    repo.session.commit.assert_not_called()

def test_exists_by_id_true(repo, mock_session):
    query = MagicMock()
    mock_session.query.return_value = query
    query.filter_by.return_value = query
    query.first.return_value = Event()

    assert repo.exists_by_id(7) is True
    mock_session.query.assert_called_once_with(Event)
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
    query.first.return_value = Event()

    assert repo.exists_by_name("E1") is True
    mock_session.query.assert_called_once_with(Event)
    query.filter_by.assert_called_once_with(name="E1")
    query.first.assert_called_once()

def test_exists_by_name_false(repo, mock_session):
    query = MagicMock()
    mock_session.query.return_value = query
    query.filter_by.return_value = query
    query.first.return_value = None

    assert repo.exists_by_name("X") is False
