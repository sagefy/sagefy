import rethinkdb as r
from flask import g
import re


def required(doc, name, field):
    """
    Given a doc and field, ensure the field is present on the model.
    """
    if field.get() is None:
        return 'Required.'


def unique(doc, name, field):
    """
    Ensure the given doc field is unique.
    """
    other = list(
        doc.table
           .filter({name: field.get()})
           .filter(r.row['id'] != doc.id.get())
           .run(g.db_conn)
    )
    if other:
        return 'Must be unique.'


def boolean(doc, name, field):
    """
    Ensure the given doc field is a boolean.
    """
    if not isinstance(field.get(), bool):
        return 'Must be true or false.'


def email(doc, name, field):
    """
    Ensure the given field is formatted as an email
    """
    if not re.match(r'\S+@\S+\.\S+', field.get()):
        return 'Must be an email.'


def minlength(doc, name, field, params):
    """
    Ensure the given field is a minimum length.
    """
    ln = params[0]
    if len(field.get()) < ln:
        return 'Must be at least %s characters.' % ln
