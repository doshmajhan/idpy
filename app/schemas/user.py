from marshmallow_sqlalchemy import field_for

from app.models import User

from ..schemas import BaseSchema


class UserSchema(BaseSchema):
    """
    User Marshmallow Schema

    Marshmallow schema used for loading/dumping Users
    """

    class Meta:
        model = User
        load_instance = True

    id = field_for(User, "id", allow_none=True)
