import rethinkdb as r
from modules.model import Model
from modules.validations import is_required, is_language, is_boolean, \
    is_list, is_string, is_list_of_strings, is_one_of, has_min_length
from modules.util import uniqid
from framework.elasticsearch import es
from modules.util import json_prep
from modules.util import omit, pick


class EntityMixin(object):
    """
    The model represents a **version** of an entity, not an entity itself.
    The `entity_id` attribute is what refers to a particular entity.
    The `id` attribute refers to a specific version of the entity.
    The `previous_id` attribute refers to the version based off.
    """

    schema = dict(Model.schema.copy(), **{
        'entity_id': {
            'validate': (is_required, is_string,),
            'default': uniqid
        },
        'previous_id': {  # TODO-2 is valid id? (set by code)
            'validate': (is_string,),
        },
        'language': {
            'validate': (is_required, is_language,),
            'default': 'en'
        },
        'name': {
            'validate': (is_required, is_string, (has_min_length, 1),)
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
        Begins the query by reducing the table down
        to the latest accepted versions for each.
        """

        # TODO-2 this query should have an index in card, unit, set
        # TODO-2 is there a way to avoid the cost of this query?
        return (cls.table
                   .filter(r.row['status'].eq('accepted'))
                   .group('entity_id')
                   .max('created')
                   .default(None)
                   .ungroup()
                   .map(r.row['reduction']))

    @classmethod
    def get_latest_accepted(cls, db_conn, entity_id):
        """
        Get the latest accepted version of the card.
        """

        if not entity_id:
            return

        # TODO-2 this query should have an index in card, unit, set
        query = (cls.start_accepted_query()
                    .filter(r.row['entity_id'] == entity_id)
                    .limit(1))

        documents = list(query.run(db_conn))

        if len(documents) > 0:
            return cls(documents[0])

    @classmethod
    def list_by_entity_ids(cls, db_conn, entity_ids):
        """
        Get a list of entities by a list of entity IDs.
        """

        if not entity_ids:
            return []

        query = (cls.start_accepted_query()
                    .filter(lambda entity:
                            r.expr(entity_ids)
                            .contains(entity['entity_id'])))

        docs = query.run(db_conn)
        return [cls(fields) for fields in docs]
        # TODO-2 index in unit and set

    @classmethod
    def get_versions(cls, db_conn, entity_id, limit=10, skip=0, **params):
        """
        Get the latest accepted version of the card.
        """

        if not entity_id:
            return []

        # TODO-2 this query should have an index in card, unit, set
        query = (cls.table
                    .filter(r.row['entity_id'] == entity_id)
                    .order_by(r.desc('created'))
                    .skip(skip)
                    .limit(limit))

        return [cls(fields) for fields in query.run(db_conn)]

    @classmethod
    def list_requires(cls, db_conn, entity_id, limit=10, skip=0, **params):
        """
        Get the same kind of entity that this one requires.
        """

        if not entity_id:
            return []

        entity = cls.get_latest_accepted(db_conn, entity_id=entity_id)

        # TODO-2 this query should have an index in card and unit
        query = (cls.start_accepted_query()
                    .filter(lambda _: r.expr(entity['requires'])
                                       .contains(_['entity_id']))
                    .order_by(r.desc('created'))
                    .skip(skip)
                    .limit(limit))

        return [cls(fields) for fields in query.run(db_conn)]

    @classmethod
    def list_required_by(cls, db_conn, entity_id, limit=10, skip=0, **params):
        """
        Get the same kind of entity that requires this one.
        """

        if not entity_id:
            return []

        # TODO-2 this query should have an index in card and unit
        query = (cls.start_accepted_query()
                    .filter(r.row['requires'].contains(entity_id))
                    .order_by(r.desc('created'))
                    .skip(skip)
                    .limit(limit))

        return [cls(fields) for fields in query.run(db_conn)]

    @classmethod
    def insert(cls, db_conn, data):
        """
        When a user creates a new version,
        don't accept certain fields.

        Also, find the previous_id.
        """

        data = omit(data, ('status', 'available'))

        if 'entity_id' in data:
            latest = cls.get_latest_accepted(db_conn, data['entity_id'])
            data['previous_id'] = latest['id']

        return super().insert(db_conn, data)

    def update(self, db_conn, data):
        """
        Only allow changes to the status on update.
        """

        data = pick(data, ('status', 'available'))
        return super().update(db_conn, data)

    def save(self, db_conn):
        """
        Overwrite save method to add to Elasticsearch.
        """

        # TODO-2 should we validate the save worked before going to ES?

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
        return super().save(db_conn)

    def find_requires_cycle(self, db_conn):
        """
        Inspect own requires to see if a cycle is formed.
        """

        seen = set()
        main_id = self['entity_id']
        found = {'cycle': False}

        def _(require_ids):
            if found['cycle']:
                return
            entities = self.__class__.list_by_entity_ids(db_conn, require_ids)
            for entity in entities:
                if entity['entity_id'] == main_id:
                    found['cycle'] = True
                    break
                if entity['entity_id'] not in seen:
                    seen.add(entity['entity_id'])
                    _(entity['require_ids'])

        _(self['require_ids'])

        return found['cycle']
