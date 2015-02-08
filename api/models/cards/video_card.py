from models.card import Card
from modules.validations import is_required, is_string, is_one_of


class VideoCard(Card):
    schema = dict(Card.schema.copy(), **{
        'site': {
            'validate': (is_required, is_string, (
                is_one_of, 'youtube', 'vimeo'),),
        },
        'id': {
            'validate': (is_required, is_string,),
        }
    })
