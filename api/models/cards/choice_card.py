from models.card import Card
from modules.validations import is_required, is_string, is_list


def is_list_of_answers(val):
    """

    """

    # TODO


class ChoiceCard(Card):
    schema = dict(Card.schema.copy(), **{
        'question': {
            'validate': (is_required, is_string,),
        },
        'answers': {
            'validate': (is_required, is_list, is_list_of_answers,),
        }
    })
