from models.card import Card
from modules.validations import is_required, is_string, is_one_of


class AudioCard(Card):
    schema = dict(Card.schema.copy(), **{
        'site': {
            'validate': (is_required, is_string, (
                is_one_of, 'soundcloud'),),
        },
        'audio_id': {
            'validate': (is_required, is_string,),
        }
    })

    def __init__(self, fields=None):
        """

        """
        super().__init__(fields)
        self['kind'] = 'audio'
