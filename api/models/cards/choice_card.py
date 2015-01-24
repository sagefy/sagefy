from models.card import Card


class ChoiceCard(Card):
    schema = dict(Card.schema.copy(), **{
        # TODO
        'question': {

        },
        'answers': {

        }
    })
