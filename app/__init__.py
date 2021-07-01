from flask import Flask
from flask_restful import Api
from saml2 import saml, samlp
from saml2.config import IdPConfig
from saml2.mdstore import MetadataStore
from saml2.server import Server

from app.config import config
from app.database import db
from app.idp_config_resource import IdpConfigResource
from app.index import Index
from app.login import Login
from app.metadata import IdpMetadataResource, SpMetadataListResource, SpMetadataResource
from app.schemas import ma
from app.sso import SsoResource
from app.users import UsersListResource, UsersResource

# TODO error handling for if config file doesn't exist


def create_app(config_name="default") -> Flask:
    # Initialize flask app with config
    app: Flask = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize SQLAlchemy db with Flask app
    db.init_app(app)

    # Initialize Marshmallow with Flask app
    ma.init_app(app)

    # Create flask-restful API with Flask app
    api: Api = Api(app)

    # Load our IDP config and create the core IDP server
    idp_config = IdPConfig()
    idp_config.load_file(app.config["IDP_CONFIG"])
    metadata_store: MetadataStore = MetadataStore([saml, samlp], None, idp_config)
    idp_config.metadata = metadata_store

    idp: Server = Server(config=idp_config)

    # Add all API resources
    api.add_resource(Index, "/")
    api.add_resource(Login, "/login")
    api.add_resource(IdpConfigResource, "/config", resource_class_args=[idp])
    api.add_resource(SsoResource, "/sso", resource_class_args=[idp])
    api.add_resource(IdpMetadataResource, "/metadata", resource_class_args=[idp])
    api.add_resource(SpMetadataListResource, "/metadata/sp", resource_class_args=[idp])
    api.add_resource(
        SpMetadataResource,
        "/metadata/sp/<string:sp_entity_id>",
        resource_class_args=[idp],
    )
    api.add_resource(UsersListResource, "/users")
    api.add_resource(UsersResource, "/users/<string:username>")

    # Create db tables
    with app.app_context():
        db.create_all()

    # Add default headers to every response
    @app.after_request
    def add_header(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        return response

    return app
