from app import db
from passlib.hash import bcrypt
from sqlalchemy.orm import validates
from datetime import datetime
from modules.util import uniqid


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(64), primary_key=True)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)
    username = db.Column(db.String(256))  # Ensure unique
    email = db.Column(db.String(256))  # Ensure unique
    password = db.Column(db.String(256))  # Use `set_password` instead

    def __init__(self, params):
        """
        Given a username, email, and password, create a new user.
        """

        self.id = uniqid()
        self.created = self.modified = datetime.utcnow()
        self.username = params.get('username')
        self.email = params.get('email')
        self.set_password(params.get('password'))
        self.commit()

    def set_password(self, value):
        """
        Encrypt the password with Bcrypt before storing to the database.
        """

        assert self.validate_password('password', value)
        self.password = bcrypt.encrypt(value)

    @validates('username')
    def validate_username(self, key, username):
        """
        A username is required.
        A username must be unique.
        """

        assert username, "A username is required."
        assert not User.query.filter_by(username=username).first(), \
            "There's already an account with that username."
        return username

    @validates('email')
    def validate_email(self, key, email):
        """
        An email is required.
        An email address must contain `@` and `.`.
        An email address must be unique.
        """

        assert email and '@' in email and '.' in email, \
            "A valid email address is required."
        assert not User.query.filter_by(email=email).first(), \
            "There's already an account with this email address."
        return email

    def validate_password(self, key, password):
        """
        A password is required.
        A password must be 8 characters or longer.
        A password cannot contain the username.
        A password cannot contain the email.

        Notice: Not using SQLAlchemy >>> Called by set_password directly
        """

        assert password, "A password is required."
        assert len(password) >= 8, "A password must be 8 characters or longer."
        assert self.username not in password, \
            "A password cannot contain username."
        assert self.email not in password, \
            "A password cannot contain email."
        return password

    def to_dict(self):
        """
        Returns self in preparation for JSON response.
        Do not include sensitive fields.
        """

        public_fields = [
            'id',
            'created',
            'username',
        ]

        return {field: getattr(self, field, None) for field in public_fields}

    def to_dict_secure(self):
        """
        Returns self in preparation for JSON response.
        Assumes user owns data.
        May include some sensitive fields.
        """

        my_fields = [
            'id',
            'created',
            'modified',
            'username',
            'email',
        ]

        return {field: getattr(self, field, None) for field in my_fields}

    def is_authenticated(self):
        """
        For Flask-Login.
        Returns True if the user is authenticated,
        i.e. they have provided valid credentials.
        (Only authenticated users will fulfill the criteria of login_required.)
        """

        return True

    def is_active(self):
        """
        For Flask-Login.
        Returns True if this is an active user - in addition to being
        authenticated, they also have activated their account,
        not been suspended, or any condition your application has
        for rejecting an account.
        Inactive accounts may not log in (without being forced of course).
        """

        return True

    def is_anonymous(self):
        """
        For Flask-Login.
        Returns True if this is an anonymous user.
        (Actual users should return False instead.)
        """

        return False

    def get_id(self):
        """
        For Flask-Login.
        Returns a unicode that uniquely identifies this user, and can be used
        to load the user from the user_loader callback. Note that this
        must be a unicode - if the ID is natively an int or some other type,
        you will need to convert it to unicode.
        """

        return unicode(self.id)

    @staticmethod
    def get_by_id(id):
        """
        Given an ID, return a matching user when available.
        """

        # TODO: Redis cache
        return User.query.filter_by(id=id).first()

    # @staticmethod
    # def get_by_email(email):
    #     """
    #     Given an email address, return a matching user when available.
    #     """

    #     # TODO: Redis cache
    #     return User.query.filter_by(email=email).first()

    # @staticmethod
    # def get_by_username(username):
    #     """
    #     Given a username, return a matching user when available.
    #     """

    #     # TODO: Redis cache
    #     return User.query.filter_by(username=username).first()

    # @staticmethod
    # def get_by_token(token):
    #     """
    #     Given a password creation token,
    #     find and validate the corresponding user.
    #     """

    #     # TODO: id = token.split('--')[0]
    #     # user = User.get_by_id(id)
    #     # TODO: if token matches, return user
    #     return False

    # def is_password_valid(self, password):
    #     """
    #     Given a password, test to see if it matches
    #     what's stored in the database.
    #     """

    #     # TODO: Verify this works correctly

    #     try:
    #         result = bcrypt.verify(password, self.password)
    #     except:
    #         result = False

    #     return result

    # def send_password_token(self):
    #     """

    #     """

    #     # token = '%s--%s' % (self.id, uniqid())
    #     # TODO: send token to redis
    #     # TODO: send user an email
    #     return False

    # def update(self, params):
    #     """

    #     """

    #     # TODO: Improve and validate method

    #     for field in ['email', 'username']:
    #         val = getattr(params, field)
    #         if val:
    #             setattr(self, field, val)

    #     return self.commit()

    def commit(self):
        """
        Commits user to the database.
        Sort of defeats the purpose of SQLAlchemy.
        """

        # TODO: Clear Redis caches

        try:
            db.session.add(self)
            db.session.commit()
            return self
        except:
            db.session.rollback()
            return False
