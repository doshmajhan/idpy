from flask_restful import Resource
from saml2.server import Server


class Metadata(Resource):
    def __init__(self, idp: Server):
        self.idp = idp

    def get(self):
        pass
