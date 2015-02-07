from modules.model import Model
from modules.validations import is_required, is_email, is_string, \
    has_min_length, is_one_of
from passlib.hash import bcrypt
from flask import url_for, current_app as app, request
from flask.ext.login import current_user
from modules.util import uniqid
from modules.content import get as c


def encrypt_password(value):
    if value and not value.startswith('$2a$'):
        return bcrypt.encrypt(value)


class User(Model):
    tablename = 'users'

    schema = dict(Model.schema.copy(), **{
        'name': {
            'validate': (is_required, is_string,),
            'unique': True,
        },
        'email': {
            'validate': (is_required, is_email,),
            'unique': True,
            'access': 'private'
        },
        'password': {
            'validate': (is_required, is_string, (has_min_length, 8)),
            'access': False,
            'bundle': encrypt_password,
        },
        'email_frequency': {
            'validate': (is_required, is_string, (
                is_one_of, 'immediate', 'daily', 'weekly', 'never',
            )),
            'access': 'private',
            'default': 'daily'
        }
    })

    def is_password_valid(self, password):
        """Take an encrypted password, and verifies it. Returns bool."""
        try:
            return bcrypt.verify(password, self['password'])
        except:
            return False

    def is_current_user(self):
        """Return True if the user is the one logged in."""
        return (current_user.is_authenticated() and
                self['id'] == current_user['id'])

    def get_url(self):
        """Where to get the user's data."""
        return url_for('user.get_user', user_id=self['id'])

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
        return self['id']

    def get_email_token(self, send_email=True):
        """Create an email token for the user to reset their password."""
        token = uniqid()
        app.redis.setex(
            'user_password_token_%s' % self['id'],  # key
            60 * 10,  # time
            bcrypt.encrypt(self['id'] + token)  # value
        )
        if send_email:
            app.mail.send_message(
                subject='Sagefy - Reset Password',
                recipients=[self['email']],
                body=c('user', 'change_password_url').replace(
                    '{url}',
                    '%spassword?id=%s&token=%s' %
                    (request.url_root, self['id'], token)
                )
            )
        return token

    def is_valid_token(self, token):
        """Ensure the given token is valid."""
        key = 'user_password_token_%s' % self['id']
        entoken = app.redis.get(key)
        app.redis.delete(key)
        if entoken:
            return bcrypt.verify(self['id'] + token, entoken)
        return False

    def update_password(self, password):
        """Update the user's password."""
        self['password'] = password
        self.save()

    # TODO When creating a new user or updating the user's name or email,
    #      index in Elasticsearch
    # TODO When close user, delete in Elasticsearch
