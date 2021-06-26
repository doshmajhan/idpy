# flake8: noqa
from flask_marshmallow import Marshmallow

ma = Marshmallow()

from .base import BaseSchema
from .user import UserSchema
