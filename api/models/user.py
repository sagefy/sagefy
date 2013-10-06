from app import db


class User(db.Model):
    id = db.Column(db.String(64), primary_key=True)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)
