"""
Different configs the app can run under
"""


class DefaultConfig:
    FLASK_ENV = "default"
    DEBUG = True


class TestingConfig:
    FLASK_ENV = "testing"
    TESTING = True


config = {
    "default": DefaultConfig,
    "testing": TestingConfig,
}
