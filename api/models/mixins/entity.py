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
                    .filter(r.row['canonical'].eq(True))
                    .order_by(r.desc('created'))
                    .limit(1))

        documents = list(query.run(g.db_conn))
        if not documents:
            return

        fields = documents[0]
        if not fields:
            return

        return cls(fields)

    @classmethod
    def get_versions(cls, entity_id, limit=10, skip=0):
        """
        Get the latest canonical version of the card.
        """

        if not entity_id:
            return

        # TODO this query should have an index in card, unit, set
        query = (cls.table
                    .filter(r.row['entity_id'] == entity_id)
                    .order_by(r.desc('created'))
                    .skip(skip)
                    .limit(limit))

        documents = query.run(g.db_conn)
        return [cls(fields) for fields in documents]
