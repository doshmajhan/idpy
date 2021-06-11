from flask import Flask

from app.config import config


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    from app.views import index

    app.register_blueprint(index)

    return app
