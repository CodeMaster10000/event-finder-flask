import unittest
from datetime import datetime
from app.schemas.event_schema import EventSchema
from app.models.event import Event
from app.models.user import User  # Assuming you have a User model

class TestEventSchema(unittest.TestCase):
    def setUp(self):
        # Mock users
        self.organizer = User(id=1, name="Alice", surname="Smith", email="alice@example.com", password_hash="secure")
        self.participant1 = User(id=2, name="Bob", surname="Jones", email="bob@example.com", password_hash="secure")
        self.participant2 = User(id=3, name="Charlie", surname="Brown", email="charlie@example.com", password_hash="secure")

        # Mock event
        self.event = Event(
            id=100,
            name="Tech Meetup",
            location="Berlin",
            time=datetime(2025, 5, 25, 18, 0),
            organizer=self.organizer,
            participants=[self.participant1, self.participant2]
        )

    def test_event_schema_serialization(self):
        schema = EventSchema()
        result = schema.dump(self.event)

        self.assertEqual(result['id'], self.event.id)
        self.assertEqual(result['name'], self.event.name)
        self.assertEqual(result['location'], self.event.location)
        self.assertEqual(result['time'], self.event.time.isoformat())
        self.assertEqual(result['organizer_name'], self.organizer.name)
        self.assertEqual(result['participants'], [self.participant1.name, self.participant2.name])

    def test_event_many_schema_serialization(self):
        schema = EventSchema(many=True)
        result = schema.dump([self.event])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['organizer_name'], self.organizer.name)
        self.assertIn(self.participant1.name, result[0]['participants'])

if __name__ == '__main__':
    unittest.main()
