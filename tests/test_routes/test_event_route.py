from tests.conftest import test_event

base_path = "events"

def test_get_all_events_e2e(client, init_data):
    """
    GET /events should return at least the pre-populated event.
    """
    _, event_id = init_data

    resp = client.get(f"/{base_path}")
    assert resp.status_code == 200

    data = resp.get_json()
    # Should be a list; find our event by ID
    assert isinstance(data, list)
    ids = [e["id"] for e in data]
    assert event_id in ids

def test_get_event_by_id_e2e(client, init_data, test_event):
    """
    GET /events/<id> should return the specific event.
    """
    _, event_id = init_data

    resp = client.get(f"/{base_path}/{event_id}")
    assert resp.status_code == 200

    ev = resp.get_json()
    assert ev["id"] == event_id
    assert ev["name"] == test_event.name
    assert ev["location"] == test_event.location
    assert ev["type"] == test_event.type

def test_create_event_e2e(client, init_data):
    """
    POST /events/organizer/<organizer_id> should create a new event.
    """
    user_id, _ = init_data
    new_event = {
        "name": "NewEvent",
        "location": "NewLocation",
        "type": "NewType"
    }

    resp = client.post(
        f"/{base_path}/organizer/{user_id}",
        json=new_event
    )
    assert resp.status_code == 201

    ev = resp.get_json()
    assert ev["name"] == new_event["name"]
    assert ev["location"] == new_event["location"]
    assert ev["type"] == new_event["type"]
    assert "id" in ev
    new_id = ev["id"]

    get_resp = client.get(f"/{base_path}/{new_id}")
    assert get_resp.status_code == 200
    assert get_resp.get_json()["id"] == new_id

def test_delete_event_e2e(client, init_data):
    """
    DELETE /events/<id> should delete the event.
    """
    _, event_id = init_data

    resp = client.delete(f"/{base_path}/{event_id}")
    data = resp.get_json()
    assert resp.status_code == 200
    assert data["message"] == f"Event {event_id} successfully deleted"
