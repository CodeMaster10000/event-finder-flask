import unittest
from unittest.mock import MagicMock, patch
from app.container import Container
from app.services.user_service import UserService
from app.services.event_service import EventService
from app.services.app_service import AppService

class TestContainer(unittest.TestCase):

    def setUp(self):
        # Patch external dependencies
        self.db_patch = patch("app.container.db")

        self.mock_db = self.db_patch.start()

        self.mock_db.session = MagicMock(name="db.session")

        # Rebind the providers with mocks
        self.container = Container()
        self.container.db_session.override(self.mock_db.session)

    def tearDown(self):
        patch.stopall()

    def test_user_service_resolution(self):
        user_service = self.container.user_service()
        self.assertIsInstance(user_service, UserService)

    def test_event_service_resolution(self):
        event_service = self.container.event_service()
        self.assertIsInstance(event_service, EventService)

    def test_app_service_resolution(self):
        app_service = self.container.app_service()
        self.assertIsInstance(app_service, AppService)


if __name__ == "__main__":
    unittest.main()
