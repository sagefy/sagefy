"""
Field type conventions
======================

All models have the following fields:
    id = db.Column(db.String(64), primary_key=True)
    created = db.Column(db.DateTime)
    modified = db.Column(db.DateTime)

All strings are length of base 2.
Shortest string length is 64 unless very specific (e.g. hex color).

Email, Name
    db.Column(db.String(256))

URL
    db.Column(db.String(128))

"""
