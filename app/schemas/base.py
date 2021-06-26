from marshmallow import EXCLUDE
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemyAutoSchemaOpts

from app.database import db


class BaseOpts(SQLAlchemyAutoSchemaOpts):
    def __init__(self, meta, ordered=False):
        if not hasattr(meta, "sqla_session"):
            meta.sqla_session = db.session

        if not hasattr(meta, "unknown"):
            meta.unknown = EXCLUDE

        super(BaseOpts, self).__init__(meta, ordered=ordered)


class BaseSchema(SQLAlchemyAutoSchema):
    OPTIONS_CLASS = BaseOpts
