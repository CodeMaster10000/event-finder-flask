from tests.conftest import test_user

base_path = "users"

def test_get_all_users_e2e(client, init_data):
    user_id, _ = init_data
    """
    GET /users should return at least the pre-populated user.
    """
    resp = client.get(f"/{base_path}")
    assert resp.status_code == 200

    data = resp.get_json()
    # Should be a list; find our user by ID
    assert isinstance(data, list)
    ids = [u["id"] for u in data]
    assert user_id in ids

def test_get_user_by_id_e2e(client, init_data, test_user):
    """
    GET /users/<id> should return the specific user.
    """
    user_id, _ = init_data
    test_user_obj = test_user
    resp = client.get(f"/{base_path}/{user_id}")
    assert resp.status_code == 200

    user = resp.get_json()
    assert user["id"] == user_id
    assert user["name"] == test_user_obj.name
    assert user["email"] == test_user_obj.email
    assert user["surname"] == test_user_obj.surname

def test_create_user_e2e(client, init_data):
    """
    POST /users should create a new user.
    """
    new_user = {
        "name": "Filip",
        "email": "new@example.com",
        "surname": "Stanislavov",
        "password_hash": "secured_password"
    }

    resp = client.post(
        f"/{base_path}",
        json=new_user
    )
    assert resp.status_code == 201

    user = resp.get_json()
    assert user["name"] == new_user["name"]
    assert user["email"] == new_user["email"]
    assert user["surname"] == new_user["surname"]
    assert "id" in user
    assert "password_hash" not in user  # Password should not be returned
    new_id = user["id"]

    # Verify the user was created by getting it
    get_resp = client.get(f"/{base_path}/{new_id}")
    assert get_resp.status_code == 200
    assert get_resp.get_json()["id"] == new_id

def test_delete_user_e2e(client, init_data):
    """
    DELETE /users/<id> should delete the user.
    """
    user_id, _ = init_data

    resp = client.delete(f"/{base_path}/{user_id}")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["message"] == f"User {user_id} deleted successfully"