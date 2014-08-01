from app import db
from datetime import datetime


class Unit(db.Model):
    __tablename__ = 'units'

    id = db.Column(db.String(64), primary_key=True)
    language = db.Column(db.String(2))


class UnitVersion(db.Model):
    __tablename__ = 'units_versions'

    id = db.Column(db.String(64), primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    modified = db.Column(db.DateTime, onupdate=datetime.utcnow())
    unit_id = db.Column(
        db.String(64),
        db.ForeignKey('units.id'),
    )
    name = db.Column(db.String(256))
    body = db.Column(db.Text)
    canonical = db.Column(db.Boolean, default=False)


units_versions_prerequisites = db.Table(
    'units_versions_prerequisites',
    db.Column(
        'version_id',
        db.String(64),
        db.ForeignKey('units_versions.id'),
    ),
    db.Column(
        'prerequisite_id',
        db.String(64),
        db.ForeignKey('units.id'),
    ),
)

units_goals = db.Table(
    'units_goals',
    db.Column(
        'version_id',
        db.String(64),
        db.ForeignKey('units_versions.id'),
    ),
    db.Column(
        'goal_id',
        db.String(64),
        db.ForeignKey('goals.id'),
    ),
    db.Column('ordinal', db.Integer),
)
