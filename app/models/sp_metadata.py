from app.database import db


class SpMetadata(db.Model):
    """
    SP Metadata SQLAlchemy model

    Represents the metadata for a Service Provider the IDP will communicate with
    """

    entity_id = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)
    metadata_xml_b64 = db.Column(db.String(), nullable=False)

    def __repr__(self) -> str:
        return f"<SpMetadata {self.entity_id}>"
