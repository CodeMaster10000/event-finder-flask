from types import SimpleNamespace

import pytest
from unittest.mock import MagicMock

from sqlalchemy.exc import SQLAlchemyError

from app.repositories.event_repository import EventRepository
from app.error_handler.exceptions import EventNotFound, AppException
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

def test_search_by_embedding(repo, mock_session):
    # Prepare two fake rows with the attributes search_by_embedding expects
    rows = [
        SimpleNamespace(name="E1", type="T1", location="L1", time_str="2025-01-01 10:00:00"),
        SimpleNamespace(name="E2", type="T2", location="L2", time_str="2025-01-02 11:00:00"),
    ]
    mock_exec = mock_session.execute.return_value
    mock_exec.all.return_value = rows

    vector = [0.1, 0.2, 0.3]
    out = repo.search_by_embedding(vector, k=2)

    # it should call execute(...) once
    mock_session.execute.assert_called_once()
    # and return a list of dicts with string value times
    assert out == [
        {"name": "E1", "type": "T1", "location": "L1", "time": "2025-01-01 10:00:00"},
        {"name": "E2", "type": "T2", "location": "L2", "time": "2025-01-02 11:00:00"},
    ]

def test_save_all_success(repo, mock_session):
    events = [Event(), Event()]
    # no side effects: commit succeeds
    result = repo.save_all(events)

    mock_session.add_all.assert_called_once_with(events)
    mock_session.commit.assert_called_once()
    # returns the same list
    assert result is events

def test_save_all_failure(repo, mock_session):
    events = [Event(), Event()]
    mock_session.commit.side_effect = SQLAlchemyError("boom")

    with pytest.raises(AppException) as e:
        repo.save_all(events)

    mock_session.rollback.assert_called_once()
    assert "Failed to save events" in str(e.value)
