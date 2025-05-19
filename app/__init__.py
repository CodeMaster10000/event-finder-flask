from flask import Flask
from flask_restx import Api
from app.config import Config
from app.container import Container
from app.controllers.app_controller import base_ns
from app.controllers.event_controller import event_ns
from app.controllers.user_controller import user_ns
from app.error_handler.error_handler import register_error_handlers
from app.extensions import db, ma, bcrypt, jwt
from app.services import user_service


def create_api(app: Flask):
    api = Api(
        app,
        title="Event Finder API",
        version="1.0",
        description="REST API",
        doc="/swagger/"  # optional: where Swagger UI lives
    )
    api.add_namespace(event_ns, path="/events")
    api.add_namespace(user_ns, path="/users")
    api.add_namespace(base_ns, path="/app")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Dependency injection
    container = Container()
    container.init_resources()
    container.wire(modules=[
        "app.controllers.app_controller",
        "app.controllers.user_controller",
        "app.controllers.event_controller",
    ])

    # Register global error handlers
    register_error_handlers(app)

    # Auto-create tables (for dev)
    with app.app_context():
        db.create_all()

    create_api(app)


    return app

