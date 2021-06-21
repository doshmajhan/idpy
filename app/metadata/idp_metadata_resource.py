from flask_restful import Resource
from saml2 import valid_instance
from saml2.config import Config
from saml2.md import EntityDescriptor
from saml2.metadata import (
    entity_descriptor,
    metadata_tostring_fix,
    sign_entity_descriptor,
)
from saml2.server import Server
from saml2.sigver import SecurityContext, security_context

METADATA_VALID_FOR: int = 365 * 24
NAME_SPACE_PAIR: dict = {"xs": "http://www.w3.org/2001/XMLSchema"}


class IdpMetadata(Resource):
    def __init__(self, idp: Server):
        self.idp: Server = idp

    def get(self) -> str:
        conf: Config = self.idp.config
        conf.valid_for = METADATA_VALID_FOR
        security_ctx: SecurityContext = security_context(conf)
        eid: EntityDescriptor = entity_descriptor(conf)
        signed_eid, xml_doc = sign_entity_descriptor(
            eid, None, security_ctx
        )  # type: EntityDescriptor, str

        # add error handling
        valid_instance(signed_eid)

        return metadata_tostring_fix(signed_eid, NAME_SPACE_PAIR, xml_doc)
