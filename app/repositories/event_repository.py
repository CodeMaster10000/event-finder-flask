from abc import ABC

from app.error_handler.exceptions import EventNotFound
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
        except BaseException as e:
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
