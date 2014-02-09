from app import db


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.String(64), primary_key=True)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)
    message_type = db.Column(db.String(64))
    user_id = db.Column(db.String(64))  # Foreign Key
    subject = db.Column(db.Text)
    body = db.Column(db.Text)
    read = db.Column(db.Boolean)  # TODO: Default False
