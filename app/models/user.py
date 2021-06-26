from app.database import db


class User(db.Model):
    """
    User SQLAlchemy model

    Represents a user in the IDP with their email, username and other attributes
    """

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self) -> str:
        return f"<User {self.id}|{self.username}|{self.email}>"
