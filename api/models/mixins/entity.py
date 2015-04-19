import rethinkdb as r
import framework.database as database


class EntityMixin(object):

    @classmethod
    def start_accepteds_query(cls):
        """

        """

        # TODO@ this query should have an index in card, unit, set
        # TODO is there a way to avoid the cost of this query?
        return (cls.table
                   .filter(r.row['accepted'].eq(True))
                   .group('entity_id')
                   .max('created')
                   .default(None)
                   .ungroup()
                   .map(r.row['reduction']))

    @classmethod
    def get_latest_accepted(cls, entity_id):
        """
        Get the latest accepted version of the card.
        """

        if not entity_id:
            return

        # TODO@ this query should have an index in card, unit, set
        query = (cls.start_accepteds_query()
                    .filter(r.row['entity_id'] == entity_id)
                    .limit(1))

        documents = list(query.run(database.db_conn))

        if len(documents) > 0:
            return cls(documents[0])

    @classmethod
    def list_by_entity_ids(cls, entity_ids):
        """
        Get a list of entities by a list of entity IDs.
        """

        if not entity_ids:
            return []

        query = (cls.start_accepteds_query()
                    .filter(lambda entity:
                            r.expr(entity_ids)
                            .contains(entity['entity_id'])))

        docs = query.run(database.db_conn)
        return [cls(fields) for fields in docs]
        # TODO@ index in unit and set

    @classmethod
    def get_versions(cls, entity_id, limit=10, skip=0):
        """
        Get the latest accepted version of the card.
        """

        if not entity_id:
            return []

        # TODO@ this query should have an index in card, unit, set
        query = (cls.table
                    .filter(r.row['entity_id'] == entity_id)
                    .order_by(r.desc('created'))
                    .skip(skip)
                    .limit(limit))

        return [cls(fields) for fields in query.run(database.db_conn)]

    @classmethod
    def list_requires(cls, entity_id, limit=10, skip=0):
        """
        Get the same kind of entity that this one requires.
        """

        if not entity_id:
            return []

        entity = cls.get_latest_accepted(entity_id=entity_id)

        # TODO@ this query should have an index in card and unit
        query = (cls.start_accepteds_query()
                    .filter(lambda _: r.expr(entity['requires'])
                                       .contains(_['entity_id'])))

        return [cls(fields) for fields in query.run(database.db_conn)]

    @classmethod
    def list_required_by(cls, entity_id, limit=10, skip=0):
        """
        Get the same kind of entity that requires this one.
        """

        if not entity_id:
            return []

        # TODO@ this query should have an index in card and unit
        query = (cls.start_accepteds_query()
                    .filter(r.row['requires'].contains(entity_id)))

        return [cls(fields) for fields in query.run(database.db_conn)]
