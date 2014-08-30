from odm.model import Model, Field
from odm.validations import is_required, is_boolean, is_string, is_list
import rethinkdb as r
from flask import g


class Notification(Model):
    tablename = 'notifications'

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
    def list(Cls, user_id=None, limit=10, skip=0, read=None, tag=None):
        """
        Get a list of models matching the provided arguments.
        Also adds pagination capabilities.
        Returns empty array when no models match.
        """
        def _(n):
            return (n['user_id'] == user_id) & \
                   (n['tags'].contains(tag) if tag is not None else True) & \
                   (n['read'] == read if read is not None else True)
        query = Cls.get_table() \
                   .order_by(r.desc('created')) \
                   .filter(_) \
                   .skip(skip)\
                   .limit(limit)
        fields_list = query.run(g.db_conn)
        return [Cls(fields) for fields in fields_list]

    def mark_as_read(self):
        """Marks the notification as read."""
        self.read.set(True)
        return self.save()
