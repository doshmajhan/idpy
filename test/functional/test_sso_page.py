"""
Tests our sso functionality
"""
from urllib.parse import quote

import pytest
from bs4 import BeautifulSoup
from flask import Flask
from saml2 import BINDING_HTTP_POST
from saml2.request import AuthnRequest
from saml2.s_utils import deflate_and_base64_encode

BASE = "http://localhost:8080"
SSO_ENDPOINT = "/sso"
RELAY_STATE = f"{BASE}/relay"  # TODO maybe put in config?
DESTINATION = f"{BASE}{SSO_ENDPOINT}"  # TODO get this from config


# TODO compress and base64 encoded
@pytest.fixture
def authn_request(saml_client) -> str:
    req_id, authn_req = saml_client.create_authn_request(
        destination=DESTINATION,
        binding=BINDING_HTTP_POST,
    )  # type: str, str

    return deflate_and_base64_encode(authn_req)


# TODO compress and base64 encoded
@pytest.fixture
def authn_request_unsigned(saml_client) -> AuthnRequest:
    req_id, authn_req = saml_client.create_authn_request(
        destination=DESTINATION,
        binding=BINDING_HTTP_POST,
        sign=False,
    )  # type: str, AuthnRequest

    return authn_req


def test_sso_with_valid_parameters(client: Flask, authn_request: str):
    response = client.get(
        f"{SSO_ENDPOINT}?SAMLRequest={quote(authn_request)}&RelayState={quote(RELAY_STATE)}"
    )
    html = BeautifulSoup(response.data, "html.parser")
    saml_response: str = html.find("input")["value"]
    assert saml_response is not None
    print(saml_response)
    assert response.status_code == 200


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
