from app import db
from passlib.hash import bcrypt
from sqlalchemy.dialects import postgresql
from datetime import datetime
from module.util import uniqid


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(64), primary_key=True)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)
    username = db.Column(db.String(256))  # Ensure unique
    email = db.Column(db.String(256))  # Ensure unique
    password = db.Column(db.String(256))
    ip = db.Column(postgresql.ARRAY(postgresql.INET))
    role = db.Column(db.String(64))
    status = db.Column(db.String(64))
    avatar = db.Column(db.String(128))
    # TODO: Notification settings

    def __init__(self, username, email, password):
        """
        Given a username, email, and password,
        create a new user.
        """
        self.id = uniqid()
        self.created = self.modified = datetime.utcnow()
        self.username = username
        self.email = email
        self.password = bcrypt.encrypt(password)
