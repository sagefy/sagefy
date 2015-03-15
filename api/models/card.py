from modules.model import Model
from modules.validations import is_required, is_language, is_boolean, \
    is_list, is_string, is_one_of
from modules.util import uniqid
from models.mixins.entity import EntityMixin


class Card(EntityMixin, Model):
    """
    Cards are the smallest entity in the Sagefy data structure system.
    A card represents a single learner activity.
    A card could present information, ask the learner to answer a question,
    collaborate with a small group to tackle a challenge,
    or create other cards.
    """
    tablename = 'cards'

    """
    The model represents a **version** of a card, not a card itself.
    The `entity_id` attribute is what refers to a particular card.
    The `id` attribute refers to a specific version of the card.
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
        'unit_id': {
            'validate': (is_required, is_string,)  # TODO@ is valid id?
        },
        'name': {
            'validate': (is_required, is_string,)
        },
        'canonical': {
            'validate': (is_boolean,),
            'default': False
        },
        'available': {
            'validate': (is_boolean,),
            'default': True
        },
        'tags': {
            'validate': (is_list,),
            'default': []
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

    # TODO@ On set canonical, index (or delete) in Elasticsearch with entity_id
