from typing import List

import pytest
from flask import Flask

from app import db
from app.models import User
from app.schemas import UserSchema

USERS_ENDPOINT: str = "/users"
TEST_USERNAME: str = "mishi"
TEST_EMAIL: str = "mishi@test.com"
TEST_USER_ATTRIBUTES: dict = {"foo": "bar"}


@pytest.fixture(autouse=True)
def populate_test_user():
    user = User(
        username=TEST_USERNAME, email=TEST_EMAIL, attributes=TEST_USER_ATTRIBUTES
    )
    db.session.add(user)
    db.session.commit()


def test_get_all_users(client: Flask):
    response = client.get(USERS_ENDPOINT)
    assert response.status_code == 200
    assert response.json is not None

    users_json: List[User] = [UserSchema().load(user) for user in response.json]

    assert len(users_json) == 1

    user: User = users_json[0]
    assert user.username == TEST_USERNAME
    assert user.email == TEST_EMAIL
    assert user.attributes == TEST_USER_ATTRIBUTES


def test_add_new_user(client: Flask):
    new_user_username: str = "squeaky"
    new_user_email: str = "squeaky@test.com"
    new_user_attributes: dict = {"foo": "barbar"}

    user: User = User(
        username=new_user_username, email=new_user_email, attributes=new_user_attributes
    )
    user_json: UserSchema = UserSchema().dump(user)

    create_response = client.post(USERS_ENDPOINT, json=user_json)
    assert create_response.status_code == 201
    # Also assert userId

    # Attempt to retrieve user
    get_response = client.get(f"{USERS_ENDPOINT}/{new_user_username}")
    assert get_response.status_code == 200
    assert get_response.json is not None

    user: User = UserSchema().load(get_response.json)

    assert user is not None
    assert user.username == new_user_username
    assert user.email == new_user_email
    assert user.attributes == new_user_attributes
