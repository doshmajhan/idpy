from flask_restful import Resource
from saml2.mdstore import MetadataStore
from saml2.server import Server


class Metadata(Resource):
    def __init__(self, idp: Server):
        self.idp: Server = idp
        self.metadata_store: MetadataStore = self.idp.metadata

    def get(self):
        pass
