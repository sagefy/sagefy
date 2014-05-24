from app import db
from datetime import datetime


class Component(db.Model):
    __tablename__ = 'components'

    id = db.Column(db.String(64), primary_key=True)
    language = db.Column(db.String(2))


class ComponentVersion(db.Model):
    __tablename__ = 'components_versions'

    id = db.Column(db.String(64), primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    modified = db.Column(db.DateTime, onupdate=datetime.utcnow())
    component_id = db.Column(
        db.String(64),
        db.ForeignKey('components.id'),
    )
    component_kind = db.Column(db.Enum('component', 'integration', name='e1'))
    name = db.Column(db.String(256))
    body = db.Column(db.Text)
    canonical = db.Column(db.Boolean, default=False)


components_versions_prerequisites = db.Table(
    'components_versions_prerequisites',
    db.Column(
        'version_id',
        db.String(64),
        db.ForeignKey('components_versions.id'),
    ),
    db.Column(
        'prerequisite_id',
        db.String(64),
        db.ForeignKey('components.id'),
    ),
)

components_objectives = db.Table(
    'components_objectives',
    db.Column(
        'version_id',
        db.String(64),
        db.ForeignKey('components_versions.id'),
    ),
    db.Column(
        'objective_id',
        db.String(64),
        db.ForeignKey('objectives.id'),
    ),
    db.Column('ordinal', db.Integer),
)
