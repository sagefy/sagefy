from models.card import Card


class WritingCard(Card):
    schema = dict(Card.schema.copy(), **{
        # TODO
    })
