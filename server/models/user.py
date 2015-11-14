from modules.model import Model
from modules.validations import is_required, is_email, is_string, \
    has_min_length, is_one_of
from passlib.hash import bcrypt
from modules.util import uniqid, pick, compact_dict, json_serial, omit, \
    json_prep
from modules.content import get as c
import json
from framework.redis import redis
from framework.mail import send_mail
from framework.elasticsearch import es
import urllib
import hashlib


def encrypt_password(value):
    if value and not value.startswith('$2a$'):
        return bcrypt.encrypt(value)
    return value


def get_avatar(email, size=24):
    """
    Gets the avatar for the given user.
    """

    if not email:
        return ''

    hash_ = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    params = urllib.parse.urlencode({'d': 'mm', 's': str(size)})
    gravatar_url = "http://www.gravatar.com/avatar/" + hash_ + "?" + params
    return gravatar_url


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
            'access': ('PaSsWoRd',),
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

    def update(self, data):
        """
        Overwrite update method to remove password.
        """

        data = omit(data, ('password',))
        return super().update(data)

    def save(self):
        """
        Overwrite save method to add to Elasticsearch.
        """

        # TODO should we validate the save worked before going to ES?

        data = json_prep(self.deliver())
        data['avatar'] = self.get_avatar()

        es.index(
            index='entity',
            doc_type='user',
            body=data,
            id=self['id'],
        )
        return super().save()

    def delete(self):
        """
        Overwrite delete method to delete in Elasticsearch.
        """

        # TODO should we validate the delete worked before going to ES?

        es.delete(
            index='entity',
            doc_type='user',
            id=self['id'],
        )
        return super().delete()

    def get_avatar(self, size=24):
        """
        Gets the avatar for the given user.
        """

        return get_avatar(self['email'], size)

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
                body=c('change_password_url').replace(
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

    def get_learning_context(self):
        """
        Get the learning context of the user.
        """

        key = 'learning_context_{id}'.format(id=self['id'])
        try:
            context = json.loads(redis.get(key).decode())
        except:
            context = {}
        return context

    def set_learning_context(self, **d):
        """
        Update the learning context of the user.

        Keys: `card`, `unit`, `set`
            `next`: `method` and `path`
        """

        context = self.get_learning_context()
        d = pick(d, ('card', 'unit', 'set', 'next'))
        context.update(d)
        context = compact_dict(context)
        key = 'learning_context_{id}'.format(id=self['id'])
        redis.setex(key, 10 * 60, json.dumps(context, default=json_serial))
        return context
