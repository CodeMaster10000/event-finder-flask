from dependency_injector import containers, providers

from app.extensions import db
from app.repositories.event_repository import EventRepository
from app.repositories.user_repository import UserRepository
from app.services.app_service import AppService
from app.services.event_service import EventService
from app.services.user_service import UserService

class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(packages=["app.routes"])

    db_session = providers.Singleton(lambda: db.session)

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
        repository=user_repository
    )

    event_service = providers.Factory(
        EventService,
        repository=event_repository,
        user_repository=user_repository
    )

    app_service = providers.Factory(
        AppService,
        event_repository=event_repository,
        user_repository=user_repository
    )