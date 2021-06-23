"""
Tests our sso functionality
"""
from typing import List
from urllib.parse import quote

import pytest
from bs4 import BeautifulSoup
from flask import Flask
from saml2 import BINDING_HTTP_POST
from saml2.client import Saml2Client
from saml2.md import EntityDescriptor
from saml2.metadata import entity_descriptor, metadata_tostring_fix
from saml2.request import AuthnRequest
from saml2.response import AuthnResponse
from saml2.s_utils import deflate_and_base64_encode

NAME_SPACE_PAIR: dict = {"xs": "http://www.w3.org/2001/XMLSchema"}
BASE: str = "http://localhost:8080"
SSO_ENDPOINT: str = "/sso"
SP_METADATA_ENDPOINT: str = "/metadata/sp"
RELAY_STATE: str = f"{BASE}/relay"  # TODO maybe put in config?
DESTINATION: str = f"{BASE}{SSO_ENDPOINT}"  # TODO get this from config


@pytest.fixture(autouse=True)
def upload_sp_metadata(client: Flask, saml_client: Saml2Client):
    entity_id: str = "foo"
    eid: EntityDescriptor = entity_descriptor(saml_client.config)
    xml_doc: str = metadata_tostring_fix(eid, NAME_SPACE_PAIR)
    response = client.put(
        f"{SP_METADATA_ENDPOINT}/{entity_id}", data={"metadata": xml_doc}
    )

    assert response.status_code == 201


@pytest.fixture
def authn_request(saml_client: Saml2Client) -> str:
    req_id, authn_req = saml_client.create_authn_request(
        destination=DESTINATION,
        binding=BINDING_HTTP_POST,
    )  # type: str, str

    return deflate_and_base64_encode(authn_req)


@pytest.fixture
def authn_request_unsigned(saml_client: Saml2Client) -> AuthnRequest:
    req_id, authn_req = saml_client.create_authn_request(
        destination=DESTINATION,
        binding=BINDING_HTTP_POST,
        sign=False,
    )  # type: str, AuthnRequest

    return authn_req


def test_sso_with_valid_parameters(
    client: Flask, saml_client: Saml2Client, authn_request: str
):
    response = client.get(
        f"{SSO_ENDPOINT}?SAMLRequest={quote(authn_request)}&RelayState={quote(RELAY_STATE)}"
    )

    assert response.status_code == 200

    html = BeautifulSoup(response.data, "html.parser")
    inputs: List = html.find_all(name="input")
    saml_response_encoded: str = inputs[0]["value"][2:-3]
    relay_state: str = inputs[1]["value"][2:-3]
    assert saml_response_encoded is not None
    assert relay_state is not None
    authn_response: AuthnResponse = saml_client.parse_authn_request_response(
        saml_response_encoded, BINDING_HTTP_POST
    )
    assert authn_response is not None


def test_sso_returns_bad_request_with_no_saml_request(client: Flask):
    response = client.get(f"{SSO_ENDPOINT}?RelayState={RELAY_STATE}")
    assert response.status_code == 400
    assert "message" in response.json
    assert response.json["message"] == {
        "SAMLRequest": "Missing required parameter in the JSON body or the post body or the query string"
    }


def test_sso_returns_bad_request_with_no_relay_state(client: Flask, authn_request: str):
    response = client.get(f"{SSO_ENDPOINT}?SAMLRequest={authn_request}")
    assert response.status_code == 400
    assert "message" in response.json
    assert response.json["message"] == {
        "RelayState": "Missing required parameter in the JSON body or the post body or the query string"
    }
