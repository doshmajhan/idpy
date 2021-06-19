from flask import Flask
from flask_restful import Api
from saml2.server import Server

from app.config import config
from app.index import Index
from app.login import Login
from app.metadata import Metadata
from app.sso import SSO


def create_app(config_name="default") -> Flask:
    app: Flask = Flask(__name__)
    app.config.from_object(config[config_name])
    api: Api = Api(app)

    idp: Server = Server(config_file=app.config["IDP_CONFIG"])

    api.add_resource(Index, "/")
    api.add_resource(Login, "/login")
    api.add_resource(SSO, "/sso", resource_class_args=[idp])
    api.add_resource(Metadata, "/metadata", resource_class_args=[idp])

    return app
