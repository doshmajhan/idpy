from base64 import b64encode
from typing import Dict, List

from flask import Flask
from saml2.client import Saml2Client
from saml2.md import EntityDescriptor, entity_descriptor_from_string
from saml2.metadata import entity_descriptor, metadata_tostring_fix

NAME_SPACE_PAIR: dict = {"xs": "http://www.w3.org/2001/XMLSchema"}
BASE: str = "http://localhost:8080"
SP_METADATA_ENDPOINT: str = "/metadata/sp"
IDP_ENTITY_ID: str = f"{BASE}/test-idp"
SP_ENTITY_ID: str = f"{BASE}/sp"
SSO_ENDPOINT: str = "/sso"
RELAY_STATE: str = f"{BASE}/relay"  # TODO maybe put in config?
DESTINATION: str = f"{BASE}{SSO_ENDPOINT}"  # TODO get this from config


def upload_sp_metadata(client: Flask, saml_client: Saml2Client):
    entity_id_encoded: str = b64encode(SP_ENTITY_ID.encode("ascii")).decode("utf-8")
    eid: EntityDescriptor = entity_descriptor(saml_client.config)
    xml_doc: str = metadata_tostring_fix(eid, NAME_SPACE_PAIR)
    response = client.put(
        f"{SP_METADATA_ENDPOINT}/{entity_id_encoded}", data={"metadata": xml_doc}
    )

    return response


def test_get_sp_metadata_by_entity_id(client: Flask, saml_client: Saml2Client):
    upload_response = upload_sp_metadata(client, saml_client)
    assert upload_response.status_code == 201

    entity_id_encoded: str = b64encode(SP_ENTITY_ID.encode("ascii")).decode("utf-8")
    response = client.get(f"{SP_METADATA_ENDPOINT}/{entity_id_encoded}")
    assert response.status_code == 200


def test_get_sp_metadata_with_entity_id_that_dne_produces_404(client: Flask):
    entity_id: str = b64encode("does-not-exist".encode("ascii")).decode("utf-8")
    response = client.get(f"{SP_METADATA_ENDPOINT}/{entity_id}")
    assert response.status_code == 404


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
    metadata_list: List[Dict[str, str]] = response.json
    assert len(metadata_list) == 1

    metadata: Dict[str, str] = metadata_list[0]
    assert metadata["entity_id"] == SP_ENTITY_ID

    entity: EntityDescriptor = entity_descriptor_from_string(metadata["metadata"])
    assert entity is not None
    assert entity.entity_id == SP_ENTITY_ID
