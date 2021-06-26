from flask import Flask
from flask_restful import Api
from saml2 import saml, samlp
from saml2.config import IdPConfig
from saml2.mdstore import MetadataStore
from saml2.server import Server

from app.config import config
from app.database import db
from app.index import Index
from app.login import Login
from app.metadata import IdpMetadata, SpMetadata, SpMetadataList
from app.schemas import ma
from app.sso import SsoResource
from app.users import UsersResource

# TODO error handling for if config file doesn't exist


def create_app(config_name="default") -> Flask:
    app: Flask = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    ma.init_app(app)
    api: Api = Api(app)

    idp_config = IdPConfig()
    idp_config.load_file(app.config["IDP_CONFIG"])
    metadata_store: MetadataStore = MetadataStore([saml, samlp], None, idp_config)
    idp_config.metadata = metadata_store

    idp: Server = Server(config=idp_config)

    api.add_resource(Index, "/")
    api.add_resource(Login, "/login")
    api.add_resource(SsoResource, "/sso", resource_class_args=[idp])
    api.add_resource(IdpMetadata, "/metadata", resource_class_args=[idp])
    api.add_resource(
        SpMetadata,
        "/metadata/sp/<string:sp_entity_id>",
        resource_class_args=[idp],
    )
    api.add_resource(
        SpMetadataList,
        "/metadata/sp",
        resource_class_args=[idp],
    )
    api.add_resource(UsersResource, "/users", "/users/<string:username>")

    with app.app_context():
        db.create_all()

    return app
