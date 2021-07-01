from flask_restful import Resource
from saml2.config import Config
from saml2.server import Server


class IdpConfigResource(Resource):
    def __init__(self, idp: Server):
        self.idp: Server = idp

    def get(self) -> str:
        conf: Config = self.idp.config

        return conf
