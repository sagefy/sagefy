from app import db
from datetime import datetime


class Goal(db.Model):
    __tablename__ = 'goals'

    id = db.Column(db.String(64), primary_key=True)
    language = db.Column(db.String(2))


class GoalVersion(db.Model):
    __tablename__ = 'goals_versions'

    id = db.Column(db.String(64), primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    modified = db.Column(db.DateTime, onupdate=datetime.utcnow())
    goal_id = db.Column(
        db.String(64),
        db.ForeignKey('goals.id'),
    )
    body = db.Column(db.Text)
    canonical = db.Column(db.Boolean, default=False)
