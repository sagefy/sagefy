import rethinkdb as r
from flask import g


class EntityMixin(object):

    @classmethod
    def get_latest_canonical(cls, entity_id):
        """
        Get the latest canonical version of the card.
        """

        if not entity_id:
            return

        # TODO this query should have an index in card, unit, set
        query = (cls.table
                    .filter(r.row['entity_id'] == entity_id)
                    .order_by(r.desc('created'))
                    .limit(1))
        fields = list(query.run(g.db_conn))[0]

        if fields:
            return cls(fields)
