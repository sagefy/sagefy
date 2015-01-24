from models.card import Card


class MatchCard(Card):
    schema = dict(Card.schema.copy(), **{
        # TODO
    })
