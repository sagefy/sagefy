import rethinkdb as r
from flask import g
import re


def required(doc, name):
    """
    Given a doc and field, ensure the field is present on the model.
    """
    field = getattr(doc, name)
    if field.get() is None:
        return 'Required.'


def unique(doc, name):
    """
    Ensure the given doc field is unique.
    """
    field = getattr(doc, name)
    other = list(
        doc.table
           .filter({name: field.get()})
           .filter(r.row['id'] != doc.id.get())
           .run(g.db_conn)
    )
    if other:
        return 'Must be unique.'


def boolean(doc, name):
    """
    Ensure the given doc field is a boolean.
    """
    field = getattr(doc, name)
    if not isinstance(field.get(), bool):
        return 'Must be true or false.'


def email(doc, name):
    """
    Ensure the given field is formatted as an email
    """
    field = getattr(doc, name)
    if not re.match(r'\S+@\S+\.\S+', field.get()):
        return 'Must be an email.'


def minlength(doc, name, params):
    """
    Ensure the given field is a minimum length.
    """
    field = getattr(doc, name)
    ln = params[0]
    if not field.get() or len(field.get()) < ln:
        return 'Must be at least %s characters.' % ln
