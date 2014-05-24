from app import db
from datetime import datetime


class Objective(db.Model):
    __tablename__ = 'objectives'

    id = db.Column(db.String(64), primary_key=True)
    language = db.Column(db.String(2))


class ObjectiveVersion(db.Model):
    __tablename__ = 'objectives_versions'

    id = db.Column(db.String(64), primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    modified = db.Column(db.DateTime, onupdate=datetime.utcnow())
    objective_id = db.Column(
        db.String(64),
        db.ForeignKey('objectives.id'),
    )
    body = db.Column(db.Text)
    canonical = db.Column(db.Boolean, default=False)
