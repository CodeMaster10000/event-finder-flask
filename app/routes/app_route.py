from dependency_injector.wiring import inject, Provide
from flask import request
from flask_restx import Namespace, Resource
from app.container import Container
from app.services.app_service import AppService

from app.services.model.model_service import ModelService

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


@base_ns.route('/message-query')
class MessageQueryResource(Resource):

    @inject
    @base_ns.doc(params={'prompt': 'User prompt'})
    def get(
            self,
            model_service: ModelService = Provide[Container.model_service],
    ):
        user_prompt = request.args.get('prompt')
        return {'response': model_service.query_prompt(user_prompt)}