from odm.model import Model
from odm.field import Field
from odm.validations import is_required, is_string, is_boolean, is_list, \
    is_one_of
import rethinkdb as r
from flask import g
from modules.content import get as _


class Notice(Model):
    tablename = 'notices'

    user_id = Field(
        validations=(is_required, is_string,)
    )
    kind = Field(
        validations=(is_required, is_string, (
            is_one_of,
            'new_proposal'
        ))
    )
    data = Field()
    # `data` stores other types of information about the notice
    # ... such as IDs to entities, users...
    read = Field(
        validations=(is_boolean,),
        default=False
    )
    tags = Field(
        validations=(is_list,),
        default=[]
    )

    @classmethod
    def list(cls, user_id=None, limit=10, skip=0, read=None, tag=None,
             kind=None, **params):
        """
        Get a list of models matching the provided arguments.
        Also adds pagination capabilities.
        Returns empty array when no models match.
        """
        query = cls.get_table() \
                   .order_by(r.desc('created')) \
                   .filter(r.row['user_id'] == user_id) \
                   .filter(r.row['kind'] == kind
                           if kind is not None else True) \
                   .filter(r.row['tags'].contains(tag)
                           if tag is not None else True) \
                   .filter(r.row['read'] == read
                           if read is not None else True) \
                   .skip(skip) \
                   .limit(limit)
        fields_list = query.run(g.db_conn)
        return [cls(fields) for fields in fields_list]

    def mark_as_read(self):
        """Marks the notice as read."""
        self.read = True
        return self.save()

    def mark_as_unread(self):
        """Marks the notice as unread."""
        self.read = False
        return self.save()

    def get_body(self):
        """Get the copy associated with this notice."""
        return _('notice', self.kind).format(**self.data or {})
