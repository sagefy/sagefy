from odm.model import Model, Field
from odm.validations import required, email, minlength
from passlib.hash import bcrypt
from flask.ext.login import current_user


def encrypt_password(field):
    return bcrypt.encrypt(field.get())


def access_email(field):
    return (current_user.is_authenticated() and
            field.get() == current_user.email.get())


class User(Model):
    tablename = 'users'

    name = Field(
        validations=(required,),
        unique=True
    )
    email = Field(
        validations=(required, email,),
        unique=True,
        access=access_email
    )
    password = Field(
        validations=(required, (minlength, 8)),
        access=False,
        before_save=encrypt_password
    )

    def is_password_valid(self, password):
        """Takes an encrypted password, and verifies it. Returns bool."""
        try:
            return bcrypt.verify(password, self.password.get())
        except:
            return False

    def is_current_user(self):
        """Returns True if the user is the one logged in."""
        return (current_user.is_authenticated() and
                self.id.get() == current_user.id.get())

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
        return unicode(self.id.get())
