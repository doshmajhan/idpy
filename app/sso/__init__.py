from flask_restful import Resource, reqparse


class SSO(Resource):
    def get(self) -> str:
        parser = reqparse.RequestParser()
        parser.add_argument("SAMLRequest", type=str, required=True)
        parser.add_argument("RelayState", type=str, required=True)
        parser.add_argument("SigAlg", type=str, required=True)
        parser.add_argument("Signature", type=str, required=True)
        args = parser.parse_args()
        return args["SAMLRequest"]
