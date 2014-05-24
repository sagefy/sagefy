from app import db
from datetime import datetime


class Module(db.Model):
    __tablename__ = 'modules'

    id = db.Column(db.String(64), primary_key=True)
    language = db.Column(db.String(2))


class ModuleVersion(db.Model):
    __tablename__ = 'modules_versions'

    id = db.Column(db.String(64), primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    modified = db.Column(db.DateTime, onupdate=datetime.utcnow())
    module_id = db.Column(
        db.String(64),
        db.ForeignKey('modules.id'),
    )
    name = db.Column(db.String(256))
    body = db.Column(db.Text)
    canonical = db.Column(db.Boolean, default=False)


modules_versions_modules = db.Table(
    'modules_versions_modules',
    db.Column(
        'version_id',
        db.String(64),
        db.ForeignKey('modules_versions.id'),
    ),
    db.Column(
        'child_id',
        db.String(64),
        db.ForeignKey('modules.id'),
    ),
)


modules_versions_components = db.Table(
    'modules_versions_components',
    db.Column(
        'version_id',
        db.String(64),
        db.ForeignKey('modules_versions.id'),
    ),
    db.Column(
        'component_id',
        db.String(64),
        db.ForeignKey('components.id'),
    ),
)
