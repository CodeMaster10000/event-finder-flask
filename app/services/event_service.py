from sqlalchemy.exc import InvalidRequestError

from app.error_handler.exceptions import UserNotFound, EventNotFound
from app.models.event import Event
from app.repositories.event_repository import EventRepository
from app.repositories.user_repository import UserRepository
from app.services.user_service import validate_user


def validate_event(event, exc):
    if event is None:
        raise exc


class EventService:
    def __init__(self, repository: EventRepository, user_repository: UserRepository):
        self.repository = repository
        self.user_repository = user_repository

    def get_all_events(self):
        return self.repository.get_all()

    def get_event(self, event_id: int) -> Event:
        event = self.repository.get_by_id(event_id)
        validate_event(event, EventNotFound(f"Event not found for id: {event_id}"))
        return event

    def create_event(self, organizer_id: int, event: Event):
        organizer = self.user_repository.get_by_id(organizer_id)
        validate_user(organizer, UserNotFound(f"Organizer not found with id: {organizer_id}"))

        if self.repository.exists_by_name(event.name):
            raise InvalidRequestError(f"Event with name already exists: {event.name}")

        event.organizer = organizer
        self.repository.save(event)
        return event

    def delete_event(self, event_id: int):
        event = self.get_event(event_id)
        self.repository.delete(event)
