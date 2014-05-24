from app import db
from datetime import datetime


class Proposal(db.Model):
    __tablename__ = 'proposals'

    id = db.Column(db.String(64), primary_key=True)
    user_id = db.Column(
        db.String(64),
        db.ForeignKey('users.id'),
    )
    kind_id = db.Column(db.String(64))
    kind_tablename = db.Column(db.String(64))


class ProposalVersion(db.Model):
    __tablename__ = 'proposals_versions'

    id = db.Column(db.String(64), primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    modified = db.Column(db.DateTime, onupdate=datetime.utcnow())
    proposal_id = db.Column(
        db.String(64),
        db.ForeignKey('proposals.id')
    )
    kind_version_id = db.Column(db.String(64))
    action = db.Column(
        db.Enum('create', 'update', 'delete', 'split', 'merge', name='e2')
    )
    decision = db.Column(
        db.Enum('pending', 'blocked', 'accepted', 'declined', name='e3')
    )
    name = db.Column(db.String(256))
    body = db.Column(db.Text)


class Vote(db.Model):
    __tablename__ = 'votes'

    id = db.Column(db.String(64), primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    modified = db.Column(db.DateTime, onupdate=datetime.utcnow())
    user_id = db.Column(
        db.String(64),
        db.ForeignKey('users.id'),
    )
    proposal_version_id = db.Column(
        db.String(64),
        db.ForeignKey('proposals_versions.id')
    )
    action = db.Column(
        db.Enum('agree', 'consent', 'discuss', 'dissent', name='e4')
    )
    body = db.Column(db.Text)
