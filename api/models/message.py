from app import db
from datetime import datetime


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.String(64), primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    modified = db.Column(db.DateTime, onupdate=datetime.utcnow())
    kind = db.Column(db.String(64))
    user_id = db.Column(db.String(64), db.ForeignKey('users.id'))
    subject = db.Column(db.Text)
    body = db.Column(db.Text)
    read = db.Column(db.Boolean, default=False)
