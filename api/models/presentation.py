from app import db
from datetime import datetime


class Presentation(db.Model):
    __tablename__ = 'presentations'

    id = db.Column(db.String(64), primary_key=True)
    language = db.Column(db.String(2))


class PresentationVersion(db.Model):
    __tablename__ = 'presentations_versions'

    id = db.Column(db.String(64), primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    modified = db.Column(db.DateTime, onupdate=datetime.utcnow())
    presentation_id = db.Column(
        db.String(64),
        db.ForeignKey('presentations.id'),
    )
    kind_tablename = db.Column(db.String(64))
    objective_id = db.Column(
        db.String(64),
        db.ForeignKey('objectives.id'),
    )
    canonical = db.Column(db.Boolean, default=False)


class PresentationVersionVideo(db.Model):
    __tablename__ = 'presentations_versions_videos'

    version_id = db.Column(
        db.String(64),
        db.ForeignKey('presentations_versions.id'),
        primary_key=True,
    )
    duration = db.Column(db.Interval)
    url = db.Column(db.String(2048))


presentations_versions_categories = db.Table(
    'presentations_versions_categories',
    db.Column(
        'version_id',
        db.String(64),
        db.ForeignKey('presentations_versions.id'),
    ),
    db.Column(
        'category_id',
        db.String(64),
        db.ForeignKey('categories.id'),
    ),
)
