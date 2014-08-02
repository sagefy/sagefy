# from modules.model import Model
# from datetime import datetime


# class Card(Model):
#     __tablename__ = 'cards'

#     id = db.Column(db.String(64), primary_key=True)
#     language = db.Column(db.String(2))


# class CardVersion(db.Model):
#     __tablename__ = 'cards_versions'

#     id = db.Column(db.String(64), primary_key=True)
#     created = db.Column(db.DateTime, default=datetime.utcnow())
#     modified = db.Column(db.DateTime, onupdate=datetime.utcnow())
#     card_id = db.Column(
#         db.String(64),
#         db.ForeignKey('cards.id'),
#     )
#     kind_tablename = db.Column(db.String(64))
#     unit_id = db.Column(
#         db.String(64),
#         db.ForeignKey('units.id'),
#     )
#     name = db.Column(db.String(256))
#     canonical = db.Column(db.Boolean, default=False)


# class CardVersionVideo(db.Model):
#     __tablename__ = 'cards_versions_videos'

#     version_id = db.Column(
#         db.String(64),
#         db.ForeignKey('cards_versions.id'),
#         primary_key=True,
#     )
#     duration = db.Column(db.Interval)
#     url = db.Column(db.String(2048))


# class CardVersionMultipleChoice(db.Model):
#     __tablename__ = 'cards_versions_multiple_choice'

#     version_id = db.Column(
#         db.String(64),
#         db.ForeignKey('cards_versions.id'),
#         primary_key=True,
#     )
#     body = db.Column(db.Text)  # question
#     attempts_allowed = db.Column(db.Integer, default=1)
#     max_choices = db.Column(db.Integer, default=4)
#     multiple_correct = db.Column(db.Boolean, default=False)


# class CardVersionMultipleChoiceAnswerText(db.Model):
#     __tablename__ = 'cards_versions_multiple_choice_answer_text'

#     id = db.Column(
#         db.String(64),
#         primary_key=True,
#     )
#     version_id = db.Column(
#         db.String(64),
#         db.ForeignKey('cards_versions.id')
#     )
#     body = db.Column(db.Text)
#     correct = db.Column(db.Boolean)
#     feedback = db.Column(db.Text)


# cards_versions_categories = db.Table(
#     'cards_versions_categories',
#     db.Column(
#         'version_id',
#         db.String(64),
#         db.ForeignKey('cards_versions.id'),
#     ),
#     db.Column(
#         'category_id',
#         db.String(64),
#         db.ForeignKey('categories.id'),
#     ),
# )
