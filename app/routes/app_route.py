from dependency_injector.wiring import inject, Provide
from flask_restx import Namespace, Resource
from app.container import Container
from app.services.app_service import AppService

base_ns = Namespace('Application', description='Base application operations')

@base_ns.route('/<int:event_id>/<int:guest_id>')
class ModifyParticipantResource(Resource):

    @inject
    def put(
        self,
        event_id: int,
        guest_id: int,
        app_service: AppService = Provide[Container.app_service]
    ):
        """Add a guest to an event"""
        app_service.add_participant(event_id, guest_id)
        return {'message': f'Guest: {guest_id} added to event: {event_id}'}, 201

    @inject
    def delete(
        self,
        event_id: int,
        guest_id: int,
        app_service: AppService = Provide[Container.app_service]
    ):
        """Remove a guest from an event"""
        app_service.remove_participant(event_id, guest_id)
        return {'message': f'Guest: {guest_id} removed from event: {event_id}'}, 200