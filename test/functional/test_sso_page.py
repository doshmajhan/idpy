"""
Tests our sso functionality
"""

SSO_ENDPOINT = "/sso"


def test_sso_with_valid_parameters(client):
    saml_request = "request"
    relay_state = "relay"
    sig_alg = "SHA1"
    signature = "dosh"

    response = client.get(
        f"{SSO_ENDPOINT}?SAMLRequest={saml_request}&RelayState={relay_state}&SigAlg={sig_alg}&Signature={signature}"
    )
    assert response.status_code == 200
    assert b"request" in response.data


def test_sso_returns_bad_request_with_no_saml_request(client):
    relay_state = "relay"
    sig_alg = "SHA1"
    signature = "dosh"

    response = client.get(
        f"{SSO_ENDPOINT}?RelayState={relay_state}&SigAlg={sig_alg}&Signature={signature}"
    )
    assert response.status_code == 400
    assert "message" in response.json
    assert response.json["message"] == {
        "SAMLRequest": "Missing required parameter in the JSON body or the post body or the query string"
    }


def test_sso_returns_bad_request_with_no_relay_state(client):
    saml_request = "request"
    sig_alg = "SHA1"
    signature = "dosh"

    response = client.get(
        f"{SSO_ENDPOINT}?SAMLRequest={saml_request}&SigAlg={sig_alg}&Signature={signature}"
    )
    assert response.status_code == 400
    assert "message" in response.json
    assert response.json["message"] == {
        "RelayState": "Missing required parameter in the JSON body or the post body or the query string"
    }


def test_sso_returns_bad_request_with_no_sig_alg(client):
    saml_request = "request"
    relay_state = "relay"
    signature = "dosh"

    response = client.get(
        f"{SSO_ENDPOINT}?SAMLRequest={saml_request}&RelayState={relay_state}&Signature={signature}"
    )
    assert response.status_code == 400
    assert "message" in response.json
    assert response.json["message"] == {
        "SigAlg": "Missing required parameter in the JSON body or the post body or the query string"
    }


def test_sso_returns_bad_request_with_no_signature(client):
    saml_request = "request"
    relay_state = "relay"
    sig_alg = "SHA1"

    response = client.get(
        f"{SSO_ENDPOINT}?SAMLRequest={saml_request}&RelayState={relay_state}&SigAlg={sig_alg}"
    )
    assert response.status_code == 400
    assert "message" in response.json
    assert response.json["message"] == {
        "Signature": "Missing required parameter in the JSON body or the post body or the query string"
    }
