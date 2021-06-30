from app.database import db


class User(db.Model):
    """
    User SQLAlchemy model

    Represents a user in the IDP with their email, username and other attributes
    """

    username = db.Column(db.String(80), primary_key=True, unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    attributes = db.Column(db.JSON, nullable=True)

    def __repr__(self) -> str:
        return f"<User {self.username}|{self.email}>"
