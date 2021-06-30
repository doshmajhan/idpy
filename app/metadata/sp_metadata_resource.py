from base64 import b64decode
from typing import Dict, List, Tuple, Union

from flask import request
from flask_restful import Resource, abort
from saml2.md import EntityDescriptor
from saml2.mdstore import InMemoryMetaData, MetadataStore
from saml2.server import Server
from sqlalchemy.exc import IntegrityError

from app.database import db
from app.models import SpMetadata
from app.schemas import SpMetadataSchema

SP_DESCRIPTOR: str = "spsso_descriptor"

# Should do something here to verify that the in memory metadata
# store is synced with db metadata store


class SpMetadataResource(Resource):
    def __init__(self, idp: Server):
        self.idp: Server = idp
        self.metadata_store: MetadataStore = self.idp.metadata

    def get(self, sp_entity_id: str) -> SpMetadataSchema:
        if not sp_entity_id:
            abort(400, message="No entity id specified")

        # Entity ID is b64 encoded in request URI, as most Entity IDs are URI's themselves
        decoded_entity_id: str = b64decode(sp_entity_id).decode("utf-8")

        metadata: SpMetadata = SpMetadata.query.filter_by(
            entity_id=decoded_entity_id
        ).first()
        metadata_json: SpMetadataSchema = SpMetadataSchema().dump(metadata)

        if not metadata_json:
            abort(404, message=f"No metadata found with entity id: {sp_entity_id}")

        return metadata_json

    def put(self, sp_entity_id: str) -> Tuple[str, int]:
        if not sp_entity_id:
            abort(400, message="No entity id specified")

        # Entity ID is b64 encoded in request URI, as most Entity IDs are URI's themselves
        decoded_entity_id: str = b64decode(sp_entity_id).decode("utf-8")
        metadata_current: SpMetadata = SpMetadata.query.filter_by(
            entity_id=decoded_entity_id
        ).first()
        if not metadata_current:
            abort(404, message=f"No metadata found with entity id: {decoded_entity_id}")

        metadata_to_update: SpMetadata = SpMetadataSchema().load(request.get_json())

        # Need to update entity id in metadata xml
        metadata_current.entity_id = metadata_to_update.entity_id
        metadata_current.metadata_xml = metadata_to_update.metadata_xml

        metadata_decoded = b64decode(metadata_current.metadata_xml_b64)

        # Check if this actually updates
        self.metadata_store.load("inline", metadata_decoded)
        db.session.commit()

        return f"{decoded_entity_id} updated", 200

    def delete(self, sp_entity_id: str) -> Tuple[str, int]:
        if not sp_entity_id:
            abort(400, message="No entity id specified")

        # Entity ID is b64 encoded in request URI, as most Entity IDs are URI's themselves
        decoded_entity_id: str = b64decode(sp_entity_id).decode("utf-8")

        metadata_to_delete: SpMetadata = SpMetadata.query.filter_by(
            entity_id=decoded_entity_id
        ).first()
        if not metadata_to_delete:
            abort(404, message=f"No metadata found with entity id: {decoded_entity_id}")

        for md in self.metadata_store.metadata.values():
            del md[decoded_entity_id]

        db.session.delete(metadata_to_delete)
        db.session.commit()
        return f"{decoded_entity_id} deleted", 200


class SpMetadataListResource(Resource):
    def __init__(self, idp: Server):
        self.idp: Server = idp
        self.metadata_store: MetadataStore = self.idp.metadata

    def get(self) -> List[SpMetadataSchema]:
        metadata_list: List[SpMetadata] = SpMetadata.query.all()

        metadata_list_json: List[SpMetadataSchema] = [
            SpMetadataSchema().dump(metadata) for metadata in metadata_list
        ]

        return metadata_list_json

    def post(self) -> Tuple[str, int]:
        metadata: SpMetadata = SpMetadataSchema().load(request.get_json())
        metadata_xml_decoded = b64decode(metadata.metadata_xml_b64)

        try:
            # Add metadata to IDP in-memory metadata store
            self.metadata_store.load("inline", metadata_xml_decoded)
            # Persist metadata to database
            db.session.add(metadata)
            db.session.commit()
            return f"{metadata.entity_id} created", 201
        except IntegrityError:
            abort(
                400,
                message=f"SP Metadata with entity id {metadata.entity_id} already exists!",
            )
            return (
                f"SP Metadata with entity id {metadata.entity_id} already exists!",
                400,
            )  # Add so mypy won't complain

    # Not sure what to do with this yet
    def _get_metadata_from_store(self) -> List[Dict[str, Union[str, EntityDescriptor]]]:
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
