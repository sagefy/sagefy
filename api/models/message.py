from app import db


class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.String(64), primary_key=True)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)
    message_type = db.Column(db.String(64))
    user_id = db.Column(db.String(64))  # Foreign Key
    object_id = db.Column(db.String(64))  # TODO: Ensure matches
    object_type = db.Column(db.String(64))
    subject = db.Column(db.Text)
    body = db.Column(db.Text)
    action = db.Column(db.String(64))
    action_url = db.Column(db.String(128))
    seen = db.Column(db.Boolean)  # TODO: Default False
