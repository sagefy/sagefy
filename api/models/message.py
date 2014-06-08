from app import db
from datetime import datetime


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.String(64), primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.String(64), db.ForeignKey('users.id'))
    from_user_id = db.Column(db.String(64), db.ForeignKey('users.id'))
    name = db.Column(db.String(256))
    body = db.Column(db.Text)
    read = db.Column(db.Boolean, default=False)
