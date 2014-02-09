from app import db


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.String(64), primary_key=True)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)
    notification_type = db.Column(db.String(64))
    user_id = db.Column(db.String(64))  # TODO: Foreign Key
    subject = db.Column(db.Text)
    body = db.Column(db.Text)
    read = db.Column(db.Boolean)  # TODO: Default False
