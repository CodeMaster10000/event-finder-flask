from dependency_injector import containers, providers

from app.configuration.config import Config
from app.configuration.model_type import ModelType
from app.extensions import db
from app.repositories import event_repository
from app.repositories.event_repository import EventRepository
from app.repositories.user_repository import UserRepository
from app.services.app_service import AppService
from app.services.event_service import EventService
from app.services.model.cloud.cloud_model_service import CloudModelService
from app.services.model.local.local_model_service import LocalModelService
from app.services.user_service import UserService


def get_model_from_env():
    model_type = Config.MODEL_TYPE
    if model_type == ModelType.LOCAL:
        return providers.Factory(
            LocalModelService,
            event_repository=event_repository,
            model_name=Config.LOCAL_MODEL_NAME
        )
    return providers.Factory(
        CloudModelService,
        event_repository=event_repository
    )

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

    model_service = get_model_from_env()