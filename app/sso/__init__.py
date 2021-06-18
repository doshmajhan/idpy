from typing import List, Tuple

from flask_restful import Resource, reqparse
from flask_restful.reqparse import Namespace, RequestParser
from saml2 import BINDING_HTTP_REDIRECT
from saml2.request import AuthnRequest
from saml2.samlp import Response
from saml2.server import Server


class SSO(Resource):
    def __init__(self, idp: Server):
        self.idp = idp

    def get(self) -> Tuple[str, int, List]:
        parser: RequestParser = reqparse.RequestParser()
        parser.add_argument("SAMLRequest", type=str, required=True)
        parser.add_argument("RelayState", type=str, required=True)
        parser.add_argument("SigAlg", type=str)
        parser.add_argument("Signature", type=str)
        args: Namespace = parser.parse_args()
        authn_request: AuthnRequest = self.idp.parse_authn_request(
            args["SAMLRequest"], BINDING_HTTP_REDIRECT
        )

        response_args: dict = self.idp.response_args(authn_request.message)
        user = "doshmajhan"

        resp: Response = self.idp.create_authn_response(
            {"givenName": "dosh"}, userid=user, sign_assertion=True, **response_args
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
