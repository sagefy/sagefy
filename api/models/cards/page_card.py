from models.card import Card


class PageCard(Card):
    schema = dict(Card.schema.copy(), **{
        # TODO
    })
