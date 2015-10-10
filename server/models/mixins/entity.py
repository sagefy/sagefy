import rethinkdb as r
import framework.database as database
from modules.model import Model
from modules.validations import is_required, is_language, is_boolean, \
    is_list, is_string, is_list_of_strings, is_one_of
from modules.util import uniqid
from framework.elasticsearch import es
from modules.util import json_prep


class EntityMixin(object):
    """
    The model represents a **version** of an entity, not an entity itself.
    The `entity_id` attribute is what refers to a particular entity.
    The `id` attribute refers to a specific version of the entity.
    The `previous_id` attribute refers to the version based off.
    """

    schema = dict(Model.schema.copy(), **{
        'entity_id': {
            'validate': (is_required, is_string,),  # TODO@ is valid id?
            'default': uniqid
        },
        'previous_id': {
            'validate': (is_string,),  # TODO@ is valid id?
        },
        'language': {
            'validate': (is_required, is_language,),
            'default': 'en'
        },
        'name': {
            'validate': (is_required, is_string,)
        },
        'status': {
            'validate': (is_required, (
                is_one_of, 'pending', 'blocked', 'accepted', 'declined'
            )),
            'default': 'pending'
        },
        'available': {
            'validate': (is_boolean,),
            'default': True
        },
        'tags': {
            'validate': (is_list, is_list_of_strings),
            'default': []
        },
    })

    def __repr__(self):
        """
        View an easy to read format when debugging.
        """

        return "{class_name}<{entity_id}>".format(
            class_name=self.__class__.__name__,
            entity_id=self['entity_id']
        )

    @classmethod
    def start_accepted_query(cls):
        """

        """

        # TODO this query should have an index in card, unit, set
        # TODO is there a way to avoid the cost of this query?
        return (cls.table
                   .filter(r.row['status'].eq('accepted'))
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

        # TODO this query should have an index in card, unit, set
        query = (cls.start_accepted_query()
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

        query = (cls.start_accepted_query()
                    .filter(lambda entity:
                            r.expr(entity_ids)
                            .contains(entity['entity_id'])))

        docs = query.run(database.db_conn)
        return [cls(fields) for fields in docs]
        # TODO index in unit and set

    @classmethod
    def get_versions(cls, entity_id, limit=10, skip=0, **params):
        """
        Get the latest accepted version of the card.
        """

        if not entity_id:
            return []

        # TODO this query should have an index in card, unit, set
        query = (cls.table
                    .filter(r.row['entity_id'] == entity_id)
                    .order_by(r.desc('created'))
                    .skip(skip)
                    .limit(limit))

        return [cls(fields) for fields in query.run(database.db_conn)]

    @classmethod
    def list_requires(cls, entity_id, limit=10, skip=0, **params):
        """
        Get the same kind of entity that this one requires.
        """

        if not entity_id:
            return []

        entity = cls.get_latest_accepted(entity_id=entity_id)

        # TODO this query should have an index in card and unit
        query = (cls.start_accepted_query()
                    .filter(lambda _: r.expr(entity['requires'])
                                       .contains(_['entity_id']))
                    .order_by(r.desc('created'))
                    .skip(skip)
                    .limit(limit))

        return [cls(fields) for fields in query.run(database.db_conn)]

    @classmethod
    def list_required_by(cls, entity_id, limit=10, skip=0, **params):
        """
        Get the same kind of entity that requires this one.
        """

        if not entity_id:
            return []

        # TODO this query should have an index in card and unit
        query = (cls.start_accepted_query()
                    .filter(r.row['requires'].contains(entity_id))
                    .order_by(r.desc('created'))
                    .skip(skip)
                    .limit(limit))

        return [cls(fields) for fields in query.run(database.db_conn)]

    def fetch_parameters(self):
        """
        Fetches the card's learning analytics parameters.
        """

        # TODO cache in redis

        params = self.parametersCls.get(entity_id=self['entity_id'])
        if params:
            return params
        return self.parametersCls({'entity_id': self['entity_id']})

    def save(self):
        """
        Overwrite save method to add to Elasticsearch.
        """

        doc_type = self.__class__.__name__.lower()

        if 'card' in doc_type:
            doc_type = 'card'

        if self['status'] == 'accepted':
            es.index(
                index='entity',
                doc_type=doc_type,
                body=json_prep(self.deliver()),
                id=self['entity_id'],
            )
        return super().save()
