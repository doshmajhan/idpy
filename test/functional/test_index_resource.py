"""
Tests our homepage is returned
"""


def test_home_page_is_returned(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"hello world" in response.data
