from base64 import b64decode, b64encode
from typing import Dict, List

from flask import Flask
from saml2.client import Saml2Client
from saml2.md import EntityDescriptor, entity_descriptor_from_string
from saml2.metadata import entity_descriptor, metadata_tostring_fix

from app.models import SpMetadata
from app.schemas import SpMetadataSchema

BASE: str = "http://localhost:8080"
NAME_SPACE_PAIR: dict = {"xs": "http://www.w3.org/2001/XMLSchema"}
SP_METADATA_ENDPOINT: str = "/metadata/sp"
SP_ENTITY_ID: str = f"{BASE}/sp"


# Change this to just insert into DB
def upload_sp_metadata(client: Flask, saml_client: Saml2Client):
    eid: EntityDescriptor = entity_descriptor(saml_client.config)
    xml_doc: str = metadata_tostring_fix(eid, NAME_SPACE_PAIR)
    xml_b64 = b64encode(xml_doc)
    sp_metadata = SpMetadata(entity_id=SP_ENTITY_ID, metadata_xml_b64=xml_b64)
    sp_metadata_json = SpMetadataSchema().dump(sp_metadata)
    response = client.post(SP_METADATA_ENDPOINT, json=sp_metadata_json)

    return response


def test_get_sp_metadata_list(client: Flask, saml_client: Saml2Client):
    # First assert that an empty list is returned
    response = client.get(SP_METADATA_ENDPOINT)

    assert response.status_code == 200
    metadata_list: List[Dict[str, str]] = response.json
    assert len(metadata_list) == 0

    # Upload metadata and assert its returned
    upload_response = upload_sp_metadata(client, saml_client)
    assert upload_response.status_code == 201

    response = client.get(SP_METADATA_ENDPOINT)

    assert response.status_code == 200
    metadata_list: List[SpMetadata] = [
        SpMetadataSchema().load(sp_metadata) for sp_metadata in response.json
    ]
    assert len(metadata_list) == 1

    metadata: SpMetadata = metadata_list[0]
    assert metadata.entity_id == SP_ENTITY_ID

    metadata_xml_decoded = b64decode(metadata.metadata_xml_b64)
    entity: EntityDescriptor = entity_descriptor_from_string(metadata_xml_decoded)
    assert entity is not None
    assert entity.entity_id == SP_ENTITY_ID
