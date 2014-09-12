import rethinkdb as r
from flask import g
from modules.util import uniqid, omit
from odm.field import Field
from odm.document import Document


def update_modified(field):
    return r.now()


class Model(Document):
    """
    Extends the Document to add database-oriented methods.
    """

    id = Field(
        default=uniqid
    )
    created = Field(
        default=r.now(),
    )
    modified = Field(
        default=r.now(),
        transform=update_modified
    )

    def __init__(self, fields=None):
        """
        Creates a new model instance given a set of fields.
        Does not store into the database, call `save` to store into database.
        """
        assert self.tablename, 'You must provide a tablename.'
        self.table = g.db.table(self.tablename)
        Document.__init__(self, fields)

    @classmethod
    def get_table(Cls):
        """
        For classmethods, a way to get the Model database table.
        Returns the table directly.
        """
        assert Cls.tablename, 'You must provide a tablename.'
        return g.db.table(Cls.tablename)

    @classmethod
    def get(Cls, **params):
        """
        Get one model which matches the provided keyword arguments.
        Returns None when there's no matching document.
        """
        fields = None
        if params.get('id'):
            fields = Cls.get_table()\
                        .get(params.get('id'))\
                        .run(g.db_conn)
        else:
            fields = list(Cls.get_table()
                             .filter(params)
                             .limit(1)
                             .run(g.db_conn))
            if len(fields) > 0:
                fields = fields[0]
            else:
                fields = None
        if fields:
            return Cls(fields)

    @classmethod
    def list(Cls, **params):
        """
        Get a list of models matching the provided keyword arguments.
        Returns empty array when no models match.
        """
        fields_list = Cls.get_table()\
                         .filter(params)\
                         .run(g.db_conn)
        return [Cls(fields) for fields in fields_list]

    @classmethod
    def insert(Cls, fields):
        """
        Creates a new model instance.
        Returns model and errors if failed.
        """
        assert isinstance(fields, dict)
        fields = omit(fields, ('id', 'created', 'modified'))
        instance = Cls(fields)
        return instance.save()

    def update(self, fields):
        """
        Update the model in the database.
        Returns model and errors if failed.
        """
        assert isinstance(fields, dict)
        fields = omit(fields, ('id', 'created', 'modified'))
        self.update_fields(fields)
        return self.save()

    def save(self):
        """
        Inserts the model in the database.
        Returns model and errors if failed.
        """
        errors = self.validate()
        if len(errors):
            return self, errors
        errors = self.test_unique()
        if len(errors):
            return self, errors
        db_fields = self.bundle()
        self.id = db_fields['id']
        self.table.insert(db_fields, conflict='update').run(g.db_conn)
        self.sync()
        return self, []

    def sync(self):
        """
        Pull the fields from the database.
        """
        fields = self.table\
                     .get(self.id)\
                     .run(g.db_conn)
        self.update_fields(fields)
        return self

    def delete(self):
        """
        Removes the model from the database.
        """
        self.table\
            .get(self.id)\
            .delete()\
            .run(g.db_conn)
        return self, []

    def test_unique(self):
        """
        Tests all top-level fields marked as unique.
        """
        errors = []
        for name, field in self.get_fields():
            if not field.unique:
                continue
            value = field.__get__(self, None)
            query = self.table \
                        .filter(lambda m: (m[name] == value) &
                                          (m['id'] != self.id))
            entries = list(query.run(g.db_conn))
            if len(entries) > 0:
                errors.append({
                    'name': name,
                    'message': 'Must be unique.',
                })
        return errors
