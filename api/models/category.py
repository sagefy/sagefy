from app import db
from datetime import datetime


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.String(64), primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    modified = db.Column(db.DateTime, onupdate=datetime.utcnow())
    name = db.Column(db.String(256))
    body = db.Column(db.Text)
