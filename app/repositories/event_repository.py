from abc import ABC

from sqlalchemy import text
from sqlalchemy import select
from app.error_handler.exceptions import EventNotFound, AppException
from app.models.event import Event
from app.repositories.base_repository import BaseRepository


class EventRepository(BaseRepository, ABC):
    def __init__(self, session):
        self.session = session

    def get_by_id(self, event_id: int) -> Event:
        return self.session.get(Event, event_id)

    def get_by_name(self, name: str) -> Event:
        return self.session.filter_by(name=name).first()

    def get_all(self) -> list[Event]:
        return self.session.query(Event).all()

    def save(self, event: Event):
        self.session.add(event)
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise AppException(f"Failed to save event: {e}", 500)
        return event

    def delete_by_id(self, event_id):
        event = self.get_by_id(event_id)
        if not event:
            raise EventNotFound(f"Event with id {event_id} not found")
        self.session.delete(event)
        self.session.commit()

    def exists_by_id(self, event_id):
        return (
                self.session.query(Event)
                .filter_by(id=event_id)
                .first()
                is not None
        )

    def exists_by_name(self, name):
        return (
                self.session.query(Event)
                .filter_by(name=name)
                .first()
                is not None
        )

    def search_by_embedding(self, vector: list[float], k: int = 5):
        try:
            stmt = (
                select(
                    Event.name,
                    Event.type,
                    Event.location,
                    Event.time.label("time_str"),
                )
                .where(Event.embedding.is_not(None))
                .order_by(Event.embedding.l2_distance(vector))
                .limit(k)
            )
            rows = self.session.execute(stmt).all()
            return [
                {
                    "name": r.name,
                    "type": r.type,
                    "location": r.location,
                    "time": str(r.time_str),
                }
                for r in rows
            ]
        except SQLAlchemyError as e:
            raise AppException(f"Data access Failure while searching for embedded events: {e}", 500)
        except Exception as e:
            raise AppException(f"Unexpected error while searching for embedded events: {e}", 500)

    def save_all(self, events: list[Event]) -> list[Event]:
        """
        Add or update a list of Event objects in one transaction.
        Rolls back on any failure and raises AppException.
        """
        try:
            self.session.add_all(events)
            self.session.commit()
        except SQLAlchemyError as e:
            self.session.rollback()
            raise AppException(f"Failed to save events: {e}", 500)
        return events
