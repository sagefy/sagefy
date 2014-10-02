from odm.model import Model, Field
from odm.validations import is_required, is_email, is_string, has_min_length
from passlib.hash import bcrypt
from flask import url_for, current_app as app, request
from flask.ext.login import current_user
from modules.util import uniqid


def encrypt_password(value):
    return bcrypt.encrypt(value)


class User(Model):
    tablename = 'users'

    name = Field(
        validations=(is_string, is_required,),
        unique=True
    )
    email = Field(
        validations=(is_required, is_email,),
        unique=True,
        access='private'
    )
    password = Field(
        validations=(is_required, is_string, (has_min_length, 8)),
        access=False,
        transform=encrypt_password
    )

    def is_password_valid(self, password):
        """Takes an encrypted password, and verifies it. Returns bool."""
        try:
            return bcrypt.verify(password, self.password)
        except:
            return False

    def is_current_user(self):
        """Returns True if the user is the one logged in."""
        return (current_user.is_authenticated() and
                self.id == current_user.id)

    def get_url(self):
        """Where to get the user's data."""
        return url_for('user.get_user', user_id=self.id)

    def is_authenticated(self):
        """For Flask-Login."""
        return True

    def is_active(self):
        """For Flask-Login."""
        return True

    def is_anonymous(self):
        """For Flask-Login."""
        return False

    def get_id(self):
        """For Flask-Login."""
        return self.id

    def get_email_token(self, send_email=True):
        """Creates an email token for the user to reset their password."""
        token = uniqid()
        app.redis.setex(
            'user_password_token_%s' % self.id,  # key
            60 * 10,  # time
            bcrypt.encrypt(self.id + token)  # value
        )
        if send_email:
            app.mail.send_message(
                subject='Sagefy - Reset Password',
                recipients=[self.email],
                body='To change your password, please visit: ' +
                     '%spassword?id=%s&token=%s' %
                     (request.url_root, self.id, token)
            )
        return token

    def is_valid_token(self, token):
        """Ensure the given token is valid."""
        key = 'user_password_token_%s' % self.id
        entoken = app.redis.get(key)
        app.redis.delete(key)
        if entoken:
            return bcrypt.verify(self.id + token, entoken)
        return False

    def update_password(self, password):
        """Updates the user's password."""
        self.password = password
        self.save()
