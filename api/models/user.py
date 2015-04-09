from modules.model import Model
from modules.validations import is_required, is_email, is_string, \
    has_min_length, is_one_of
from passlib.hash import bcrypt
from modules.util import uniqid
from modules.content import get as c
import json
from framework.redis import redis
from framework.mail import send_mail


def encrypt_password(value):
    if value and not value.startswith('$2a$'):
        return bcrypt.encrypt(value)


# TODO@ When creating a new user or updating the user's name or email,
#       index in Elasticsearch
# TODO@ When close user, delete in Elasticsearch

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
            'access': ('private',),
        },
        'password': {
            'validate': (is_required, is_string, (has_min_length, 8)),
            'access': (),
            'bundle': encrypt_password,
        },
        'settings': {
            'validate': (is_required,),
            'default': {},
            'embed': {
                'email_frequency': {
                    'validate': (is_required, is_string, (
                        is_one_of, 'immediate', 'daily', 'weekly', 'never',
                    )),
                    'access': ('private',),
                    'default': 'daily',
                },
                'view_sets': {
                    'validate': (is_required, is_string, (
                        is_one_of, 'public', 'private'
                    )),
                    'access': ('private',),
                    'default': 'private',
                },
                'view_follows': {
                    'validate': (is_required, is_string, (
                        is_one_of, 'public', 'private'
                    )),
                    'access': ('private',),
                    'default': 'private',
                },
            }
        }
    })

    def is_password_valid(self, password):
        """
        Take an encrypted password, and verifies it. Returns bool.
        """

        try:
            return bcrypt.verify(password, self['password'])
        except:
            return False

    def get_email_token(self, send_email=True):
        """
        Create an email token for the user to reset their password.
        """

        token = uniqid()
        redis.setex(
            'user_password_token_{id}'.format(id=self['id']),  # key
            60 * 10,  # time
            bcrypt.encrypt(self['id'] + token)  # value
        )
        if send_email:
            send_mail(
                subject='Sagefy - Reset Password',
                recipient=self['email'],
                body=c('user', 'change_password_url').replace(
                    '{url}',
                    '%spassword?id=%s&token=%s' %
                    ('https://sagefy.org/', self['id'], token)
                )
            )
        return token

    def is_valid_token(self, token):
        """
        Ensure the given token is valid.
        """

        key = 'user_password_token_{id}'.format(id=self['id'])
        entoken = redis.get(key)
        redis.delete(key)
        if entoken:
            entoken = entoken.decode()
            return bcrypt.verify(self['id'] + token, entoken)
        return False

    def update_password(self, password):
        """
        Update the user's password.
        """

        self['password'] = password
        self.save()

    def get_learning_context(self):
        """
        Get the learning context of the user.
        """

        key = 'learning_context_{id}'.format(id=self['id'])
        try:
            return json.loads(redis.get(key).decode())
        except:
            return {}

    def set_learning_context(self, **kwargs):
        """
        Update the learning context.
        """

        key = 'learning_context_{id}'.format(id=self['id'])
        try:
            context = json.loads(redis.get(key).decode())
        except:
            context = {}

        for kind in ('card', 'unit', 'set'):
            if kind in kwargs and kwargs[kind] is None:
                del context[kind]

        card, unit, set_ = (kwargs.get('card'), kwargs.get('unit'),
                            kwargs.get('set'))

        if card and 'entity_id' in card:
            context['card'] = {
                'id': card['entity_id'],
            }

        if unit and 'entity_id' in unit:
            context['unit'] = {
                'id': unit['entity_id'],
                'name': unit['name'],
                'body': unit['body'],
            }

        if set_ and 'entity_id' in set_:
            context['set'] = {
                'id': set_['entity_id'],
                'name': set_['name'],
            }

        redis.setex(key, 10 * 60, json.dumps(context))
        return context
