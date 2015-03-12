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

        # TODO@ this query should have an index in card, unit, set
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

        # TODO@ this query should have an index in card, unit, set
        query = (cls.table
                    .filter(r.row['entity_id'] == entity_id)
                    .order_by(r.desc('created'))
                    .skip(skip)
                    .limit(limit))

        return [cls(fields) for fields in query.run(g.db_conn)]

    @classmethod
    def list_requires(cls, entity_id, limit=10, skip=0):
        """
        Get the same kind of entity that this one requires.
        """

        entity = cls.get_latest_canonical(entity_id=entity_id)

        # TODO@ this query should have an index in card and unit
        query = (cls.table
                    .filter(entity['requires'].contains(r.row['requires']))
                    .filter(r.row['canonical'].eq(True))
                    .order_by(r.desc('created'))
                    .distinct(r.row['entity_id'])
                    .skip(skip)
                    .limit(limit))

        return [cls(fields) for fields in query.run(g.db_conn)]

    @classmethod
    def list_required_by(cls, entity_id, limit=10, skip=0):
        """
        Get the same kind of entity that requires this one.
        """

        # TODO@ this query should have an index in card and unit
        query = (cls.table
                    .filter(r.row['requires'].created(entity_id))
                    .filter(r.row['canonical'].eq(True))
                    .order_by(r.desc('created'))
                    .distinct(r.row['entity_id'])
                    .skip(skip)
                    .limit(limit))

        return [cls(fields) for fields in query.run(g.db_conn)]
