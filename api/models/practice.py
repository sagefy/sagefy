from app import db
from datetime import datetime


class Practice(db.Model):
    __tablename__ = 'practices'

    id = db.Column(db.String(64), primary_key=True)
    language = db.Column(db.String(2))


class PracticeVersion(db.Model):
    __tablename__ = 'practices_versions'

    id = db.Column(db.String(64), primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow())
    modified = db.Column(db.DateTime, onupdate=datetime.utcnow())
    practice_id = db.Column(
        db.String(64),
        db.ForeignKey('practices.id'),
    )
    kind_tablename = db.Column(db.String(64))
    objective_id = db.Column(
        db.String(64),
        db.ForeignKey('objectives.id'),
    )
    canonical = db.Column(db.Boolean, default=False)


class PracticeVersionMultipleChoice(db.Model):
    __tablename__ = 'practices_versions_multiple_choice'

    version_id = db.Column(
        db.String(64),
        db.ForeignKey('practices_versions.id'),
        primary_key=True,
    )
    body = db.Column(db.Text)  # question
    attempts_allowed = db.Column(db.Integer, default=1)
    max_choices = db.Column(db.Integer, default=4)
    multiple_correct = db.Column(db.Boolean, default=False)


class PracticeVersionMultipleChoiceAnswerText(db.Model):
    __tablename__ = 'practices_versions_multiple_choice_answer_text'

    id = db.Column(
        db.String(64),
        primary_key=True,
    )
    version_id = db.Column(
        db.String(64),
        db.ForeignKey('practices_versions.id')
    )
    body = db.Column(db.Text)
    correct = db.Column(db.Boolean)
    feedback = db.Column(db.Text)


practices_versions_categories = db.Table(
    'practices_versions_categories',
    db.Column(
        'version_id',
        db.String(64),
        db.ForeignKey('practices_versions.id')
    ),
    db.Column(
        'category_id',
        db.String(64),
        db.ForeignKey('categories.id')
    ),
)
