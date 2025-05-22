import unittest
from flask import Flask
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, InvalidRequestError
from app.error_handler.error_handler import register_error_handlers
from app.error_handler.exceptions import AppException


class TestErrorHandlers(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        register_error_handlers(self.app)

        # Add routes to simulate exceptions
        @self.app.route("/raise-app-exception")
        def raise_app_exception():
            raise AppException("Custom error", status_code=418)

        @self.app.route("/raise-integrity-error")
        def raise_integrity_error():
            raise IntegrityError("Unique constraint", None, BaseException())

        @self.app.route("/raise-sqlalchemy-error")
        def raise_sqlalchemy_error():
            raise SQLAlchemyError("General DB error")

        @self.app.route("/raise-invalid-request")
        def raise_invalid_request():
            raise InvalidRequestError("Bad SQL usage")

        self.client = self.app.test_client()

    def test_app_exception_handler(self):
        response = self.client.get("/raise-app-exception")
        self.assertEqual(response.status_code, 418)
        self.assertEqual(response.get_json(), {"error": "Custom error"})

    def test_integrity_error_handler(self):
        response = self.client.get("/raise-integrity-error")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Database integrity error", response.get_json()["error"])

    def test_sqlalchemy_error_handler(self):
        response = self.client.get("/raise-sqlalchemy-error")
        self.assertEqual(response.status_code, 500)
        self.assertIn("A database error occurred", response.get_json()["error"])

    def test_invalid_request_error_handler(self):
        response = self.client.get("/raise-invalid-request")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid request", response.get_json()["error"])


if __name__ == "__main__":
    unittest.main()
