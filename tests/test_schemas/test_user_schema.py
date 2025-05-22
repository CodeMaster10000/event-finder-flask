import unittest
from app.models.user import User
from app.models.event import Event
from app.schemas.user_schema import UserSchema


class TestUserSchema(unittest.TestCase):
    def setUp(self):
        # Mock users
        self.organizer = User(id=1, name="Alice", surname="Smith", email="alice@example.com")
        self.participant = User(id=2, name="Bob", surname="Jones", email="bob@example.com")

        # Mock event
        self.event = Event(
            id=100,
            name="Tech Conference",
            location="Berlin",
            time=None,
            organizer=self.organizer,
            participants=[self.participant]
        )

        # Set reverse relationships
        self.organizer.organized_event = self.event
        self.participant.participating_events = [self.event]

    def test_user_schema_organizer(self):
        schema = UserSchema()
        result = schema.dump(self.organizer)

        self.assertEqual(result["id"], 1)
        self.assertEqual(result["name"], "Alice")
        self.assertEqual(result["organized_event"], 100)
        self.assertEqual(result["participating_events"], [])

    def test_user_schema_participant(self):
        schema = UserSchema()
        result = schema.dump(self.participant)

        self.assertEqual(result["id"], 2)
        self.assertEqual(result["name"], "Bob")
        self.assertIsNone(result["organized_event"])
        self.assertEqual(result["participating_events"], [100])


if __name__ == "__main__":
    unittest.main()