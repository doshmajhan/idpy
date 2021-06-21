from base64 import b64encode
from typing import Dict, List

from flask import Flask
from saml2.client import Saml2Client
from saml2.md import EntityDescriptor, entity_descriptor_from_string
from saml2.mdstore import MetadataStore

BASE = "http://localhost:8080"
SP_METADATA_ENDPOINT = "/metadata/sp"
IDP_ENTITY_ID = f"{BASE}/test-idp"
SP_ENTITY_ID = f"{BASE}/sp"


def test_get_sp_metadata_by_entity_id(client: Flask):
    entity_id: str = b64encode(SP_ENTITY_ID.encode("ascii")).decode("utf-8")
    response = client.get(f"{SP_METADATA_ENDPOINT}/{entity_id}")
    assert response.status_code == 200


def test_get_sp_metadata_with_entity_id_that_dne_produces_404(client: Flask):
    entity_id: str = b64encode("does-not-exist".encode("ascii")).decode("utf-8")
    response = client.get(f"{SP_METADATA_ENDPOINT}/{entity_id}")
    assert response.status_code == 404


def test_get_sp_metadata_list(client: Flask):
    response = client.get(SP_METADATA_ENDPOINT)

    assert response.status_code == 200
    metadata_list: List[Dict[str, str]] = response.json
    assert len(metadata_list) == 1

    metadata: Dict[str, str] = metadata_list[0]
    assert metadata["entity_id"] == SP_ENTITY_ID

    entity: EntityDescriptor = entity_descriptor_from_string(metadata["metadata"])
    assert entity is not None
    assert entity.entity_id == SP_ENTITY_ID


def test_upload_metadata(client: Flask, saml_client: Saml2Client):
    entity_id = "foo"
    metadata: MetadataStore = saml_client.metadata
    response = client.put(
        f"{SP_METADATA_ENDPOINT}/{entity_id}", data={"metadata": metadata.dumps()}
    )

    assert response.status_code == 201
