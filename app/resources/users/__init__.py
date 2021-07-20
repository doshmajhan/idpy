from typing import List, Tuple

from flask import request
from flask_restful import Resource, abort
from sqlalchemy.exc import IntegrityError

from app.database import db
from app.models import User
from app.schemas import UserSchema


class UsersResource(Resource):
    def get(self, username: str) -> UserSchema:
        user: User = User.query.filter_by(username=username).first()
        user_json: UserSchema = UserSchema().dump(user)

        if not user_json:
            abort(404, message=f"No user found with username: {username}")

        return user_json

    def put(self, username: str) -> str:
        if not username:
            abort(400, message="No username specified")

        user_current: User = User.query.filter_by(username=username).first()
        if not user_current:
            abort(404, message=f"No user found with username: {username}")

        user_to_update: User = UserSchema().load(request.get_json())

        # Figure out a better way to do this
        user_current.username = user_to_update.username
        user_current.email = user_to_update.email
        user_current.attributes = user_to_update.attributes

        db.session.commit()

        return "User updated"

    def delete(self, username: str) -> str:
        if not username:
            abort(400, message="No username specified")

        user_to_delete: User = User.query.filter_by(username=username).first()
        if not user_to_delete:
            abort(404, message=f"No user found with username: {username}")

        db.session.delete(user_to_delete)
        db.session.commit()

        return "User deleted"


class UsersListResource(Resource):
    def get(self) -> List[UserSchema]:
        users: List[User] = User.query.all()

        users_json: List[UserSchema] = [UserSchema().dump(user) for user in users]

        return users_json

    def post(self) -> Tuple[str, int]:
        user: User = UserSchema().load(request.get_json())

        try:
            db.session.add(user)
            db.session.commit()
            return "User created", 201

        except IntegrityError:
            abort(400, message="User with that username/email already exists!")
            return (
                "User with that username/email already exists!",
                400,
            )  # Add so mypy won't complain
