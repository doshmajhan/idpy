from flask import Flask
from flask_restful import Api
from saml2.server import Server

from app.config import config


def create_app(config_name="default") -> Flask:
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    api = Api(app)

    from app.index import Index
    from app.login import Login
    from app.sso import SSO

    idp = Server(app.config["IDP_CONFIG"])

    api.add_resource(Index, "/")
    api.add_resource(Login, "/login")
    api.add_resource(SSO, "/sso", resource_class_args=[idp])

    return app
