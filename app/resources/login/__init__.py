from typing import List

from flask import Response, make_response, render_template
from flask_restful import Resource, reqparse
from flask_restful.reqparse import Namespace, RequestParser

from app.models import User
from app.schemas import UserSchema


class Login(Resource):
    def get(self) -> Response:
        parser: RequestParser = reqparse.RequestParser()
        parser.add_argument("SAMLRequest", type=str, required=True)
        parser.add_argument("RelayState", type=str, required=True)
        parser.add_argument("SigAlg", type=str)
        parser.add_argument("Signature", type=str)

        args: Namespace = parser.parse_args()
        users: List[User] = User.query.all()
        users_json: List[UserSchema] = [UserSchema().dump(user) for user in users]

        return make_response(
            render_template(
                "login.html",
                users=users_json,
                saml_request=args["SAMLRequest"],
                relay_state=args["RelayState"],
                sig_alg=args["SigAlg"],
                signature=args["Signature"],
            ),
            200,
            {"Content-Type": "text/html"},
        )
