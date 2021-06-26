import os
from pathlib import Path

import pytest
from flask import Flask
from saml2 import saml, samlp
from saml2.client import Saml2Client
from saml2.config import SPConfig
from saml2.mdstore import MetadataStore

from app import create_app
from app.database import db

SP_CONFIG_FILE = os.path.join(Path(__file__).parent, "test_sp_config.py")
IDP_METADATA_XML = os.path.join(Path(__file__).parent, "metadata/test-idp.xml")


@pytest.fixture
def app() -> Flask:
    app: Flask = create_app("testing")
    return app


@pytest.fixture
def saml_client() -> Saml2Client:
    # Load config file
    sp_config: SPConfig = SPConfig()
    sp_config.load_file(SP_CONFIG_FILE)

    # Create metadata store and then add IDP metadata to SP config
    # so that we can verify the signature of the IDP
    metadata_store: MetadataStore = MetadataStore([saml, samlp], None, sp_config)
    metadata_store.load("local", IDP_METADATA_XML)

    sp_config.metadata = metadata_store
    sp: Saml2Client = Saml2Client(config=sp_config)
    return sp


@pytest.fixture(autouse=True)
def clear_database():
    # let tests run, drop afterwards
    yield
    db.drop_all()
