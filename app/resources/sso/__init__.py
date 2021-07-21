from typing import List, Tuple, Union

import werkzeug
from flask import redirect, url_for
from flask_restful import Resource, reqparse
from flask_restful.reqparse import Namespace, RequestParser
from saml2 import BINDING_HTTP_REDIRECT, NAMEID_FORMAT_EMAILADDRESS
from saml2.authn_context import PASSWORD, AuthnBroker, authn_context_class_ref
from saml2.entity import NameID
from saml2.request import AuthnRequest
from saml2.samlp import Response
from saml2.server import Server


def username_password_authn():
    pass


class SsoResource(Resource):
    def __init__(self, idp: Server):
        self.idp = idp

    def get(self) -> Union[werkzeug.Response, Tuple[str, int, List]]:
        parser: RequestParser = reqparse.RequestParser()
        parser.add_argument("SAMLRequest", type=str, required=True)
        parser.add_argument("RelayState", type=str, required=True)
        parser.add_argument("SigAlg", type=str)
        parser.add_argument("Signature", type=str)
        parser.add_argument("username", type=str)

        args: Namespace = parser.parse_args()
        authn_request: AuthnRequest = self.idp.parse_authn_request(
            args["SAMLRequest"], BINDING_HTTP_REDIRECT
        )

        response_args: dict = self.idp.response_args(authn_request.message)

        # Check if username is there, if not send to /login to select user to login as.
        if not args["username"]:
            return redirect(url_for("login"))

        user = args["username"]

        # Document a wrapper for this
        AUTHN_BROKER = AuthnBroker()
        AUTHN_BROKER.add(
            authn_context_class_ref(PASSWORD),
            username_password_authn,
            10,
            "http://localhost:8080",
        )

        authn: dict = AUTHN_BROKER.get_authn_by_accr(PASSWORD)

        name_id = NameID(format=NAMEID_FORMAT_EMAILADDRESS, text=user)

        # Dict should be attributes
        resp: Response = self.idp.create_authn_response(
            {"givenName": "dosh"},
            userid=user,
            sign_assertion=True,
            authn=authn,
            name_id=name_id,
            **response_args,
        )

        binding_out, destination = self.idp.pick_binding(
            "assertion_consumer_service",
            entity_id=authn_request.message.issuer.text,
            request=authn_request.message,
        )  # type: str, str

        http_args: dict = self.idp.apply_binding(
            binding_out,
            f"{resp}",
            destination,
            args["RelayState"],
            response=True,
        )

        return http_args["data"], 200, http_args["headers"]
