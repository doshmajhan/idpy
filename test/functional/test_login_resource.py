"""
Tests our login is returned
"""


def test_login_page_is_returned(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b"login" in response.data
