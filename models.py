"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"


class User (db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(999), nullable = False)
    last_name = db.Column(db.String(999), nullable = False)
    image_url = db.Column(db.String(800), nullable = False, default = DEFAULT_IMAGE_URL)


    posts = db.relationship("Post", backref="user", 
                            # cascade="all, delete-orphan"
                            )

    @property
    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"


class Post (db.Model):

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(999), nullable = False)
    content = db.Column(db.String(999), nullable = False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable = True)

    @property
    def friendly_date(self):
        """Return nicely-formatted date."""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")


class PostTag(db.Model):
    
    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"),primary_key = True, nullable = False)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"),primary_key = True, nullable = False)

    # direct navigation: postags -> tags & posts
    # tags_and_posts = db.relationship("Tag", secondary = "posts", backref = "post_tags")


class Tag(db.Model):

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship(
        'Post',
        secondary="posts_tags",
        # cascade="all,delete",
        backref="tags",
    )


    

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)



