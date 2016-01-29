from modules.model import Model
from modules.validations import is_required, is_list, is_string, is_one_of
from models.mixins.entity import EntityMixin
import rethinkdb as r


class Card(EntityMixin, Model):
    """
    Cards are the smallest entity in the Sagefy data structure system.
    A card represents a single learner activity.
    A card could present information, ask the learner to answer a question,
    collaborate with a small group to tackle a challenge,
    or create other cards.
    """
    tablename = 'cards'

    schema = dict(EntityMixin.schema.copy(), **{
        'unit_id': {
            'validate': (is_required, is_string,)
        },
        'require_ids': {
            'validate': (is_list,),
            'default': []
        },
        'kind': {
            'validate': (is_required, is_string,
                         (is_one_of, 'video',  # 'page', 'audio', 'slideshow',
                                     'choice',  # 'number', 'match', 'formula',
                                     # 'writing', 'upload', 'embed'
                                     # only video & choice to start
                          ))
        }
    })

    def validate(self, db_conn):
        """

        """

        errors = super().validate(db_conn)
        if not errors:
            errors += self.is_valid_unit(db_conn)
        if not errors:
            errors += self.ensure_requires(db_conn)
        if not errors:
            errors += self.ensure_no_cycles(db_conn)
        return errors

    def is_valid_unit(self, db_conn):
        """

        """

        query = (r.table('units')
                  .filter(r.row['entity_id'] == self['unit_id'])
                  .filter(r.row['status'].eq('accepted'))
                  .limit(1))
        units = query.run(db_conn)
        if not units:
            return [{'name': 'unit_id', 'message': 'Not a valid unit.'}]
        return []

    def ensure_requires(self, db_conn):
        """

        """

        cards = Card.list_by_entity_ids(db_conn, self['require_ids'])
        if len(self['require_ids']) != len(cards):
            return [{'message': 'Didn\'t find all requires.'}]
        return []

    def ensure_no_cycles(self, db_conn):
        """
        Ensure no require cycles form.
        """

        if self.find_requires_cycle(db_conn):
            return [{'message': 'Found a cycle in requires.'}]

        return []

    def validate_response(self, response):
        """
        Ensure the given response is valid, given the card information.
        Returns a list of errors.
        """

        raise Exception("No method implemented.")

    def score_response(self, response):
        """
        Score the given response.
        Returns the score and feedback.
        """

        raise Exception("No method implemented.")

    def has_assessment(self):
        """
        Is this card kind an assessment type?
        """

        return self['kind'] in ('choice', 'number', 'match', 'formula',
                                'writing', 'upload', 'embed')

    def has_asynchronous(self):
        """
        Is this card kind an assessment type?
        """

        return self['kind'] in ('writing', 'upload', 'embed')
