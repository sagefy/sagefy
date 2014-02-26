from app import db
from passlib.hash import bcrypt
from sqlalchemy.orm import validates
from datetime import datetime
from modules.util import uniqid
import re
from modules.most_common_passwords import most_common_passwords


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(64), primary_key=True)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)
    username = db.Column(db.String(256))  # Ensure unique
    email = db.Column(db.String(256))  # Ensure unique
    password = db.Column(db.String(256))
    # TODO: Notification settings
    # TODO: Message settings

    def __init__(self, params):
        """
        Given a username, email, and password,
        create a new user.
        """

        self.id = uniqid()
        self.created = self.modified = datetime.utcnow()
        self.username = params['username']
        self.email = params['email']
        self.password = params['password']

    @property
    def password(self):
        """
        Just pretend I don't exist.
        """
        return self.password

    @password.setter
    def password(self, value):
        """
        Encrypt the password with BCrypt before storing to the database
        """
        self.password = bcrypt.encrypt(value)

    @validates('username')
    def validate_username(self, key, username):
        """
        A username must be unique.
        """

        assert not User.query.filter_by(username=username).first(), \
            "There's already an account with that username."
        return username

    @validates('email')
    def validate_email(self, key, email):
        """
        An email address must contain `@` and `.`.
        An email address must be unique.
        """

        assert '@' in email and '.' in email, "Must be an email address"
        assert not User.query.filter_by(email=email).first(), \
            "There's already an account with this email address."
        return email

    @validates('password')
    def validate_password(self, key, password):
        """
        A password must be 8 characters or longer.
        A password must contain a number.
        A password must contain at least one uppercase letter.
        A password cannot contain the username.
        A password cannot contain the email.
        A password must not be one of the most common passwords.
        """

        assert len(password) >= 8, "Password must be 8 characters or longer."
        assert re.search('\d+', password) is not None, \
            "Password must contain a number."
        assert password.lower() != password, \
            "Pasword must contain at least one uppercase letter."
        if self and self.username:
            assert self.username not in password, \
                "Password cannot contain username."
        if self and self.email:
            assert self.email not in password, \
                "Password cannot contain email."
        assert password not in most_common_passwords, \
            "Password cannot be common."
        return password

    def to_dict(self):
        """
        Returns self in preparation for JSON response.
        Do not include sensitive fields.
        """

        d = dict(User)
        del d['password']
        del d['modified']
        del d['email']
        return d

    def to_dict_secure(self):
        """
        Returns self in preparation for JSON response.
        Assumes user owns data.
        May include some sensitive fields.
        """

        d = dict(User)
        del d['password']
        return d
