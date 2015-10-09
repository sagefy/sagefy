from models.card import Card
from modules.validations import is_required, is_string, is_one_of


class VideoCard(Card):
    schema = dict(Card.schema.copy(), **{
        'site': {
            'validate': (is_required, is_string, (
                is_one_of, 'youtube', 'vimeo'),),
        },
        'video_id': {
            'validate': (is_required, is_string,),
        }
    })

    def __init__(self, fields=None):
        """
        Create a new video card instance.
        """

        super().__init__(fields)
        self['kind'] = 'video'

    def validate_response(self, body):
        """
        Ensure the given response body is valid, given the card information.
        """

        return [{'message': 'No response is valid.'}]
