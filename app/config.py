"""
Different configs the app can run under
"""


class DefaultConfig:
    FLASK_ENV = "default"
    DEBUG = True
    BUNDLE_ERRORS = True
    IDP_CONFIG = "./app/idp_config.py"


class TestingConfig:
    FLASK_ENV = "testing"
    TESTING = True
    BUNDLE_ERRORS = True
    IDP_CONFIG = "./app/idp_config.py"


config = {
    "default": DefaultConfig,
    "testing": TestingConfig,
}
