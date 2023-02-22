"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


    
class User (db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.String(999), nullable = False)
    last_name = db.Column(db.String(999), nullable = False)
    image_url = db.Column(db.String(800), nullable = False)

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

