from base64 import b64decode
from typing import Dict, List, Tuple, Union

from flask_restful import Resource, fields, marshal_with, marshal_with_field, reqparse
from flask_restful.reqparse import Namespace, RequestParser
from saml2.md import EntityDescriptor
from saml2.mdstore import InMemoryMetaData, MetadataStore
from saml2.server import Server

SP_DESCRIPTOR: str = "spsso_descriptor"


class EntityDescriptorField(fields.Raw):
    def format(self, value: EntityDescriptor):
        return str(value)


class SpMetadata(Resource):

    sp_metadata_response_fields: dict = {
        "metadata": EntityDescriptorField,
    }

    def __init__(self, idp: Server):
        self.idp: Server = idp
        self.metadata_store: MetadataStore = self.idp.metadata

    @marshal_with(sp_metadata_response_fields)
    def get(
        self, sp_entity_id: str
    ) -> Union[Tuple[str, int], Dict[str, EntityDescriptor]]:
        # Handle decoding errors
        decoded_entity_id: str = b64decode(sp_entity_id).decode("utf-8")
        md: InMemoryMetaData
        for md in self.metadata_store.metadata.values():
            entity_id: str
            entity_desc: dict
            for entity_id, entity_desc in md.items():
                print(entity_id)
                if entity_id == decoded_entity_id and SP_DESCRIPTOR in entity_desc:
                    return {"entity_id": entity_id, "metadata": md.entity_descr}

        return f"Unable to find Service Provider with Entity ID: {sp_entity_id}", 404

    def put(self, sp_entity_id: str) -> Tuple[str, int]:
        print(sp_entity_id)
        parser: RequestParser = reqparse.RequestParser()
        parser.add_argument("metadata", type=str, required=True)
        args: Namespace = parser.parse_args()
        metadata = args["metadata"]

        self.metadata_store.load("inline", metadata)
        return "Created", 201


class SpMetadataList(Resource):

    sp_metadata_response_fields: dict = {
        "entity_id": fields.String,
        "metadata": EntityDescriptorField,
    }

    sp_metadata_list_response = fields.List(fields.Nested(sp_metadata_response_fields))

    def __init__(self, idp: Server):
        self.idp: Server = idp
        self.metadata_store: MetadataStore = self.idp.metadata

    @marshal_with_field(sp_metadata_list_response)
    def get(self) -> List[Dict[str, Union[str, EntityDescriptor]]]:
        sp_metadata_list: List[Dict[str, Union[str, EntityDescriptor]]] = list()
        md: InMemoryMetaData
        for md in self.metadata_store.metadata.values():
            entity_id: str
            entity_desc: dict
            for entity_id, entity_desc in md.items():
                if SP_DESCRIPTOR in entity_desc:
                    sp_metadata_list.append(
                        {"entity_id": entity_id, "metadata": md.entity_descr}
                    )

        return sp_metadata_list
