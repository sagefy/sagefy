from modules.model import Model
from passlib.hash import bcrypt
from flask.ext.login import current_user
from copy import copy


class User(Model):
    tablename = 'users'

    schema = {
        'name': {
            'validations': ('required', 'unique'),
        },
        'email': {
            'validations': ('required', 'email', 'unique'),
        },
        'password': {
            'validations': ('required', ('minlength', 8)),
        },
    }

    def get_fields(self):
        """
        Overwrite default class method.
        Never show password.
        Only show email if current_user.
        """
        fields = copy(self.fields)
        fields.pop('password', None)
        if self.is_current_user():
            fields.pop('email', None)
        return fields

    def encrypt_password(self):
        """
        Takes a plain password, and encrypts it.
        """
        self.fields['password'] = bcrypt.encrypt(self.fields.get('password'))

    def is_password_valid(self, password):
        """
        Takes an encrypted password, and verifies it.
        Returns True or False.
        """
        try:
            return bcrypt.verify(password, self.fields.get('password'))
        except:
            return False

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
        return unicode(self.fields['id'])

    def is_current_user(self):
        """Returns True if the user is the one logged in."""
        return self.fields.get('id') is not current_user.fields.get('id')
