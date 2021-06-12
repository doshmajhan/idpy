from flask import Flask
from flask_restful import Api

from app.config import config


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    api = Api(app)

    from app.index import Index
    from app.login import Login
    from app.sso import SSO

    api.add_resource(Index, "/")
    api.add_resource(Login, "/login")
    api.add_resource(SSO, "/sso")

    return app
