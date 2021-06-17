"""
Different configs the app can run under
"""
import os
from pathlib import Path

BASEDIR = Path(__file__).parent


def full_path(local_file):
    return os.path.join(BASEDIR, local_file)


class DefaultConfig:
    FLASK_ENV = "default"
    DEBUG = True
    BUNDLE_ERRORS = True
    IDP_CONFIG = full_path("idp_config.py")


class TestingConfig:
    FLASK_ENV = "testing"
    TESTING = True
    BUNDLE_ERRORS = True
    IDP_CONFIG = full_path("../test/test_idp_config.py")


config = {
    "default": DefaultConfig,
    "testing": TestingConfig,
}
