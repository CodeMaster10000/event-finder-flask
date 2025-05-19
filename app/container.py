from dependency_injector import containers, providers
from app.repositories.user_repository import UserRepository
from app.repositories.event_repository import EventRepository
from app.services.user_service import UserService
from app.services.event_service import EventService
from app.extensions import db, bcrypt

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["app.controllers"])

    db_session = providers.Singleton(lambda: db.session)
    password_hasher = providers.Singleton(lambda: bcrypt)

    # Repositories
    user_repository = providers.Factory(
        UserRepository,
        session=db_session
    )

    event_repository = providers.Factory(
        EventRepository,
        session=db_session
    )

    # Services
    user_service = providers.Factory(
        UserService,
        repository=user_repository,
        bcrypt=password_hasher
    )

    event_service = providers.Factory(
        EventService,
        repository=event_repository,
        user_repository=user_repository
    )
