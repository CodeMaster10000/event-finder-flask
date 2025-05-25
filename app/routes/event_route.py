from dependency_injector.wiring import inject, Provide
from flask import request
from flask_restx import Resource, Namespace, fields
from app.container import Container
from app.models.event import Event
from app.schemas import event_schema

from app.services.event_service import EventService

event_ns = Namespace("events", description="Event operations")

@event_ns.route("")
class EventListResource(Resource):

    @inject
    def get(self, event_service: EventService = Provide[Container.event_service]):
        """Get all events"""
        events = event_service.get_all_events()
        return event_schema.event_many.dump(events), 200

@event_ns.route("")
class EventEmbeddings(Resource):

    @inject
    def put(self, event_service: EventService = Provide[Container.event_service]):
        """Embedd all events"""
        event_service.create_embeddings_for_events()
        return {"Finished embedding events": "Success"}, 200

@event_ns.route("/<int:event_id>")
class EventResource(Resource):

    @inject
    def get(self, event_id, event_service: EventService = Provide[Container.event_service]):
        """Get an event by id"""
        event = event_service.get_event(event_id)
        return event_schema.event_single.dump(event), 200

    @inject
    def delete(self, event_id, event_service: EventService = Provide[Container.event_service]):
        """Delete an event by id"""
        event_service.delete_event(event_id)
        return {"message": f"Event {event_id} successfully deleted"}, 200


@event_ns.route("/organizer/<int:organizer_id>")
class EventCreateResource(Resource):

    event_input = event_ns.model("EventInput", {
        "name": fields.String(required=True),
        "location": fields.String(required=True),
        "type": fields.String(required=True),
    })

    @event_ns.expect(event_input)
    @inject
    def post(self, organizer_id, event_service: EventService = Provide[Container.event_service]):
        """Create a new event"""
        data = request.get_json()
        saved = event_service.create_event(organizer_id, Event(**data))
        return event_schema.event_single.dump(saved), 201
