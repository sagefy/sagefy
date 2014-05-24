from app import db
from datetime import datetime


class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.String(64), primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    user_id = db.Column(db.String(64), db.ForeignKey('users.id'))
    subject = db.Column(db.Text)
    body = db.Column(db.Text)
    read = db.Column(db.Boolean, default=False)


notifications_categories = db.Table(
    'notifications_categories',
    db.Column(
        'notification_id',
        db.String(64),
        db.ForeignKey('notifications.id'),
    ),
    db.Column(
        'category_id',
        db.String(64),
        db.ForeignKey('categories.id'),
    ),
)
