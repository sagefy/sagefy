from modules.model import Model
from passlib.hash import bcrypt
# from flask.ext.login import current_user


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
            'set': 'encrypt_password',
            'get': 'decrypt_password',
        },
    }

    def encrypt_password(self, password):
        """
        Takes a plain password, and encrypts it.
        """
        return bcrypt.encrypt(password)

    def decrypt_password(self, password):
        """
        Takes an encrypted password, and verifies it.
        Returns True or False.
        """
        try:
            return bcrypt.verify(password, self.password)
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
