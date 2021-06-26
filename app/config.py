"""
Different configs the app can run under
"""
import os
from pathlib import Path

BASEDIR = Path(__file__).parent


def full_path(local_file):
    return os.path.join(BASEDIR, local_file)


class DefaultConfig:
    HOST = "0.0.0.0"
    PORT = 8080
    FLASK_ENV = "default"
    DEBUG = True
    BUNDLE_ERRORS = True
    IDP_CONFIG = full_path("idp_config.py")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{full_path('idpy.db')}"


class TestingConfig:
    HOST = "127.0.0.1"
    PORT = 8080
    FLASK_ENV = "testing"
    TESTING = True
    BUNDLE_ERRORS = True
    IDP_CONFIG = full_path("../test/test_idp_config.py")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{full_path('test-idpy.db')}"


config = {
    "default": DefaultConfig,
    "testing": TestingConfig,
}
