from app.error_handler.exceptions import UserNotFound, AppException, EventNotFound
from app.models.event import Event
from app.repositories.event_repository import EventRepository
from app.repositories.user_repository import UserRepository
from app.services.event_service import validate_event
from app.services.user_service import validate_user


class AppService:
    def __init__(
            self,
            event_repository: EventRepository,
            user_repository: UserRepository):
        self.event_repository = event_repository
        self.user_repository = user_repository

    def add_participant(self, event_id: int, user_id: int) -> Event:
        event = self.event_repository.get_by_id(event_id)
        user = self.user_repository.get_by_id(user_id)
        validate_user(user, UserNotFound(f"Participant not found with id: {user_id}"))
        validate_event(event, EventNotFound(f"Event not found with id: {event_id}"))
        if user in event.participants:
            raise AppException(f"User {user_id} already participating in event {event_id}", 400)
        event.participants.append(user)
        self.event_repository.save(event)
        return event