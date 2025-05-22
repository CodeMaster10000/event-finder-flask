from sqlalchemy.exc import IntegrityError, SQLAlchemyError, InvalidRequestError

from app.error_handler.exceptions import AppException


def register_error_handlers(app):
    @app.errorhandler(AppException)
    def handle_app_exception(error):
        return {'error': error.message}, error.status_code

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        return {'error': f'Database integrity error: {str(error)}'}, 400

    @app.errorhandler(SQLAlchemyError)
    def handle_sqlalchemy_error(error):
        return {'error': f'A database error occurred: {str(error)}'}, 500

    @app.errorhandler(InvalidRequestError)
    def handle_invalid_request(error):
        return {'error': f'Invalid request: {str(error)}'}, 400
