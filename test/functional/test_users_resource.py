from typing import List

import pytest
from flask import Flask

from app.database import db
from app.models import User
from app.schemas import UserSchema

USERS_ENDPOINT: str = "/users"
TEST_USERNAME = "mishi"
TEST_EMAIL = "mishi@test.com"
TEST_USER_ATTRIBUTES: dict = {"foo": "bar"}


@pytest.fixture(autouse=True)
def populate_test_user():
    user = User(
        username=TEST_USERNAME, email=TEST_EMAIL, attributes=TEST_USER_ATTRIBUTES
    )
    db.session.add(user)
    db.session.commit()


def test_get_user_by_id(client: Flask):
    response = client.get(f"{USERS_ENDPOINT}/{TEST_USERNAME}")
    assert response.status_code == 200
    assert response.json is not None
    user: User = UserSchema().load(response.json)
    print(user)
    assert user is not None
    assert user.username == TEST_USERNAME
    assert user.email == TEST_EMAIL
    assert user.attributes == TEST_USER_ATTRIBUTES


def test_get_user_by_nonexistant_id_produces_404(client: Flask):
    nonexistent_username: str = "pipsqueak"
    response = client.get(f"{USERS_ENDPOINT}/{nonexistent_username}")
    assert response.status_code == 404


def test_update_current_user(client: Flask):
    updated_user_username: str = "bign"
    updated_user_email: str = "bign@test.com"
    updated_user_attributes: dict = {"foo": "barbar"}

    user: User = User(
        username=updated_user_username,
        email=updated_user_email,
        attributes=updated_user_attributes,
    )
    user_json: UserSchema = UserSchema().dump(user)

    update_response = client.put(f"{USERS_ENDPOINT}/{TEST_USERNAME}", json=user_json)
    assert update_response.status_code == 200

    print(User.query.all())

    # Retrieve user to verify update
    get_response = client.get(f"{USERS_ENDPOINT}/{updated_user_username}")
    assert get_response.status_code == 200
    assert get_response.json is not None

    user: User = UserSchema().load(get_response.json)

    assert user is not None
    assert user.username == updated_user_username
    assert user.email == updated_user_email
    assert user.attributes == updated_user_attributes

    # assert only 1 user exists
    response = client.get(USERS_ENDPOINT)
    assert response.status_code == 200
    assert response.json is not None

    users_json: List[User] = [UserSchema().load(user) for user in response.json]
    assert len(users_json) == 1


def test_delete_user(client: Flask):
    update_response = client.delete(f"{USERS_ENDPOINT}/{TEST_USERNAME}")
    assert update_response.status_code == 200

    # Attempt to retrieve user
    get_response = client.get(f"{USERS_ENDPOINT}/{TEST_USERNAME}")
    assert get_response.status_code == 404
