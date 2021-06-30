from app.models import SpMetadata

from ..schemas import BaseSchema


class SpMetadataSchema(BaseSchema):
    """
    SpMetadata Marshmallow Schema

    Marshmallow schema used for loading/dumping SP Metadata
    """

    class Meta:
        model = SpMetadata
        load_instance = True
