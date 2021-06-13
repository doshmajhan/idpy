from flask_restful import Resource, reqparse
from saml2.server import Server


class SSO(Resource):
    def __init__(self, idp: Server):
        self.idp = idp

    def get(self) -> str:
        parser = reqparse.RequestParser()
        parser.add_argument("SAMLRequest", type=str, required=True)
        parser.add_argument("RelayState", type=str, required=True)
        parser.add_argument("SigAlg", type=str)
        parser.add_argument("Signature", type=str)
        args = parser.parse_args()
        # authn_request: AuthnRequest = self.idp.parse_authn_request(
        #    args["SAMLRequest"], BINDING_HTTP_REDIRECT
        # )
        # print(authn_request.binding)
        return args["SAMLRequest"]
