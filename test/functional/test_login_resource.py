"""
Tests our login is returned
"""
from urllib.parse import quote

import pytest
from flask import Flask
from saml2 import BINDING_HTTP_POST
from saml2.client import Saml2Client
from saml2.s_utils import deflate_and_base64_encode

BASE: str = "http://localhost:8080"
SSO_ENDPOINT: str = "/sso"
RELAY_STATE: str = f"{BASE}/relay"  # TODO maybe put in config?
DESTINATION: str = f"{BASE}{SSO_ENDPOINT}"  # TODO get this from config
SP_ENTITY_ID: str = f"{BASE}/sp"
USERNAME = "dosh@test.com"


@pytest.fixture
def authn_request(saml_client: Saml2Client) -> str:
    req_id, authn_req = saml_client.create_authn_request(
        destination=DESTINATION,
        binding=BINDING_HTTP_POST,
    )  # type: str, str

    return deflate_and_base64_encode(authn_req)


def test_login_page_is_returned(
    client: Flask, saml_client: Saml2Client, authn_request: str
):
    response = client.get(
        f"/login?SAMLRequest={quote(authn_request)}&RelayState={quote(RELAY_STATE)}"
    )
    assert response.status_code == 200
    assert b"Login" in response.data
