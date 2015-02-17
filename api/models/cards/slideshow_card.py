from models.card import Card
from modules.validations import is_required, is_string, is_one_of


class SlideshowCard(Card):
    schema = dict(Card.schema.copy(), **{
        'site': {
            'validate': (is_required, is_string, (
                is_one_of, 'slideshare'),),
        },
        'slideshow_id': {
            'validate': (is_required, is_string,),
        }
    })

    def __init__(self, fields=None):
        """

        """
        super().__init__(fields)
        self['kind'] = 'slideshow'
