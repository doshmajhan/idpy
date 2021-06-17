import pytest
from flask import Flask
from saml2.client import Saml2Client

from app import create_app

SP_CONFIG_FILE = "./test/test_sp_config.py"


@pytest.fixture
def app() -> Flask:
    app: Flask = create_app("testing")
    return app


@pytest.fixture
def saml_client() -> Saml2Client:
    sp = Saml2Client(config_file=SP_CONFIG_FILE)
    return sp
