import datetime

from sqlalchemy.exc import InvalidRequestError

from app.error_handler.exceptions import UserNotFound, EventNotFound
from app.models.event import Event
from app.repositories.event_repository import EventRepository
from app.repositories.user_repository import UserRepository
from app.services.user_service import validate_user
from app.util.embedding_util import create_embedded_text
from app.util.validaton_util import validate_event


class EventService:
    def __init__(self, repository: EventRepository, user_repository: UserRepository):
        self.repository = repository
        self.user_repository = user_repository

    def get_all_events(self):
        return self.repository.get_all()

    def get_event(self, event_id: int) -> Event:
        event = self.repository.get_by_id(event_id)
        validate_event(event, EventNotFound(f"Event not found for id: {event_id}", 404))
        return event

    def create_event(self, organizer_id: int, event: Event):
        organizer = self.user_repository.get_by_id(organizer_id)
        validate_user(organizer, UserNotFound(f"Organizer not found with id: {organizer_id}"))

        if self.repository.exists_by_name(event.name):
            raise InvalidRequestError(f"Event with name already exists: {event.name}")

        new_event = Event(
            name=event.name,
            location=event.location,
            type=event.type,
            organizer_id=organizer_id,
            time=datetime.datetime.now()
        )

        embedding_vector = create_embedded_text(new_event)
        new_event.embedding = embedding_vector

        saved_event = self.repository.save(new_event)
        return saved_event

    def delete_event(self, event_id: int):
        validate_event(self.repository.get_by_id(event_id), EventNotFound(f"Event not found for id: {event_id}"))
        self.repository.delete_by_id(event_id)

    def create_embeddings_for_events(self):
        events = self.repository.get_all()
        for event in events:
            if event.embedding is None:
                embedding_vector = create_embedded_text(event)
                event.embedding = embedding_vector
                self.repository.save(event)

