from odm.model import Model, Field
from odm.validations import is_required, is_boolean, is_string, is_list
import rethinkdb as r
from flask import g


class Notice(Model):
    tablename = 'notices'

    user_id = Field(
        validations=(is_required, is_string,)
    )
    body = Field(
        validations=(is_required, is_string,)
    )
    read = Field(
        validations=(is_boolean,),
        default=False
    )
    tags = Field(
        validations=(is_list,),
        default=[]
    )

    @classmethod
    def list(Cls, user_id=None, limit=10, skip=0, read=None, tag=None,
             **params):
        """
        Get a list of models matching the provided arguments.
        Also adds pagination capabilities.
        Returns empty array when no models match.
        """
        query = Cls.get_table() \
                   .order_by(r.desc('created')) \
                   .filter(r.row['user_id'] == user_id) \
                   .filter(r.row['tags'].contains(tag)
                           if tag is not None else True) \
                   .filter(r.row['read'] == read
                           if read is not None else True) \
                   .skip(skip) \
                   .limit(limit)
        fields_list = query.run(g.db_conn)
        return [Cls(fields) for fields in fields_list]

    def mark_as_read(self):
        """Marks the notice as read."""
        self.read = True
        return self.save()
