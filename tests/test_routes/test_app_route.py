# tests/test_routes/test_app_route.py

base_path = "app"

def test_add_participant_e2e(client, init_data, app):
    user_id, event_id = init_data

    # Call the route
    resp = client.put(f"/{base_path}/{event_id}/{user_id}")
    assert resp.status_code == 201
    assert resp.json["message"] == f"Guest: {user_id} added to event: {event_id}"

    # Fetch fresh from DB
    with app.app_context():
        from app.models.event import Event as EventModel
        from app.models.user import User as UserModel

        event = EventModel.query.get(event_id)
        user = UserModel.query.get(user_id)
        assert user in event.participants

def test_remove_participant_e2e(client, init_data, app):
    user_id, event_id = init_data

    # First add
    client.put(f"/{base_path}/{event_id}/{user_id}")

    # Then remove
    resp = client.delete(f"/{base_path}/{event_id}/{user_id}")
    assert resp.status_code == 200
    assert resp.json["message"] == f"Guest: {user_id} removed from event: {event_id}"

    # Verify removal
    with app.app_context():
        from app.models.event import Event as EventModel
        from app.models.user import User as UserModel

        event = EventModel.query.get(event_id)
        user = UserModel.query.get(user_id)
        assert user not in event.participants
