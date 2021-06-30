from base64 import b64encode

import pytest
from flask import Flask
from saml2.client import Saml2Client
from saml2.md import EntityDescriptor
from saml2.metadata import entity_descriptor, metadata_tostring_fix

from app.models import SpMetadata
from app.schemas import SpMetadataSchema

NAME_SPACE_PAIR: dict = {"xs": "http://www.w3.org/2001/XMLSchema"}
BASE: str = "http://localhost:8080"
SP_METADATA_ENDPOINT: str = "/metadata/sp"
IDP_ENTITY_ID: str = f"{BASE}/test-idp"
SP_ENTITY_ID: str = f"{BASE}/sp"
SSO_ENDPOINT: str = "/sso"
RELAY_STATE: str = f"{BASE}/relay"  # TODO maybe put in config?
DESTINATION: str = f"{BASE}{SSO_ENDPOINT}"  # TODO get this from config


@pytest.fixture(autouse=True)
def upload_sp_metadata(client: Flask, saml_client: Saml2Client):
    eid: EntityDescriptor = entity_descriptor(saml_client.config)
    xml_doc: str = metadata_tostring_fix(eid, NAME_SPACE_PAIR)
    xml_b64 = b64encode(xml_doc)
    sp_metadata = SpMetadata(entity_id=SP_ENTITY_ID, metadata_xml_b64=xml_b64)
    sp_metadata_json = SpMetadataSchema().dump(sp_metadata)
    response = client.post(SP_METADATA_ENDPOINT, json=sp_metadata_json)

    assert response.status_code == 201


def test_get_sp_metadata_by_entity_id(client: Flask, saml_client: Saml2Client):
    entity_id_encoded: str = b64encode(SP_ENTITY_ID.encode("ascii")).decode("utf-8")
    response = client.get(f"{SP_METADATA_ENDPOINT}/{entity_id_encoded}")
    assert response.status_code == 200
    sp_metadata: SpMetadata = SpMetadataSchema().load(response.json)
    assert sp_metadata.entity_id == SP_ENTITY_ID


def test_get_sp_metadata_with_entity_id_that_dne_produces_404(client: Flask):
    entity_id_dne: str = b64encode("does-not-exist".encode("ascii")).decode("utf-8")
    response = client.get(f"{SP_METADATA_ENDPOINT}/{entity_id_dne}")
    assert response.status_code == 404


def test_update_metadata_with_new_entity_id():
    pass


def test_delete_metadata(client: Flask):
    entity_id_encoded: str = b64encode(SP_ENTITY_ID.encode("ascii")).decode("utf-8")
    response = client.delete(f"{SP_METADATA_ENDPOINT}/{entity_id_encoded}")
    assert response.status_code == 200

    # Attempt to retrieve after deletion
    get_response = client.get(f"{SP_METADATA_ENDPOINT}/{entity_id_encoded}")
    assert get_response.status_code == 404
