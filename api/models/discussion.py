from app import db
from datetime import datetime


class DiscussionThread(db.Model):
    __tablename__ = 'discussions_threads'

    id = db.Column(db.String(64), primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    modified = db.Column(db.DateTime, onupdate=datetime.utcnow())
    kind_id = db.Column(db.String(64))
    kind_tablename = db.Column(db.String(64))
    name = db.Column(db.String(256))


class DiscussionMessage(db.Model):
    __tablename__ = 'discussions_messages'

    id = db.Column(db.String(64), primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    modified = db.Column(db.DateTime, onupdate=datetime.utcnow())
    user_id = db.Column(
        db.String(64),
        db.ForeignKey('users.id'),
    )
    thread_id = db.Column(
        db.String(64),
        db.ForeignKey('discussions_threads.id'),
    )
    body = db.Column(db.Text)
    replies_to_id = db.Column(
        db.String(64),
        db.ForeignKey('discussions_messages.id'),
    )
