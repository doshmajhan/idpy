from typing import List

from flask import Flask
from saml2 import BINDING_HTTP_REDIRECT
from saml2.client import Saml2Client
from saml2.mdstore import MetadataStore

BASE = "http://localhost:8080"
METADATA_ENDPOINT = "/metadata"
IDP_ENTITY_IDP = "http://localhost:8080/test-idp"


def test_get_idp_metadata(client: Flask, saml_client: Saml2Client):
    response = client.get(f"{METADATA_ENDPOINT}")

    assert response.status_code == 200

    # Load IDP metadata string
    metadata_store: MetadataStore = saml_client.metadata
    metadata_store.load("inline", response.data.decode("unicode_escape")[1:-2])

    # Attempt to load IDP from metadata
    idp: List[dict] = metadata_store.single_sign_on_service(
        IDP_ENTITY_IDP, binding=BINDING_HTTP_REDIRECT
    )
    assert idp is not None
    assert len(idp) == 1
