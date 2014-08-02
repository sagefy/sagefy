# from modules.model import Model
# from datetime import datetime


# class Set(db.Model):
#     __tablename__ = 'sets'

#     id = db.Column(db.String(64), primary_key=True)
#     language = db.Column(db.String(2))


# class SetVersion(db.Model):
#     __tablename__ = 'sets_versions'

#     id = db.Column(db.String(64), primary_key=True)
#     created = db.Column(db.DateTime, default=datetime.utcnow())
#     modified = db.Column(db.DateTime, onupdate=datetime.utcnow())
#     set_id = db.Column(
#         db.String(64),
#         db.ForeignKey('sets.id'),
#     )
#     name = db.Column(db.String(256))
#     body = db.Column(db.Text)
#     canonical = db.Column(db.Boolean, default=False)


# sets_versions_sets = db.Table(
#     'sets_versions_sets',
#     db.Column(
#         'version_id',
#         db.String(64),
#         db.ForeignKey('sets_versions.id'),
#     ),
#     db.Column(
#         'child_id',
#         db.String(64),
#         db.ForeignKey('sets.id'),
#     ),
# )


# sets_versions_components = db.Table(
#     'sets_versions_components',
#     db.Column(
#         'version_id',
#         db.String(64),
#         db.ForeignKey('sets_versions.id'),
#     ),
#     db.Column(
#         'unit_id',
#         db.String(64),
#         db.ForeignKey('units.id'),
#     ),
# )
