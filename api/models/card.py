from modules.model import Model
from modules.validations import is_required, is_list, is_string, is_one_of
from models.mixins.entity import EntityMixin
from models.card_parameters import CardParameters


# TODO@ On set accepted, index (or delete) in Elasticsearch with entity_id
class Card(EntityMixin, Model):
    """
    Cards are the smallest entity in the Sagefy data structure system.
    A card represents a single learner activity.
    A card could present information, ask the learner to answer a question,
    collaborate with a small group to tackle a challenge,
    or create other cards.
    """
    tablename = 'cards'

    parametersCls = CardParameters

    schema = dict(EntityMixin.schema.copy(), **{
        'unit_id': {
            'validate': (is_required, is_string,)  # TODO@ is valid id?
        },
        'require_ids': {
            'validate': (is_list,),  # TODO@ is valid ids?
            'default': []
        },
        'kind': {
            'validate': (is_required, is_string,
                         (is_one_of, 'video', 'page', 'audio', 'slideshow',
                                     'choice', 'number', 'match', 'formula',
                                     'writing', 'upload', 'embed'))
        }
    })

    def validate(self):
        errors = super().validate()
        if not errors:
            errors += self.ensure_no_cycles()
        return errors

    def ensure_no_cycles(self):
        """
        TODO@ Ensure no require cycles form.
        """

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
