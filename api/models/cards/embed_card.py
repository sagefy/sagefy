from models.card import Card


class EmbedCard(Card):
    schema = dict(Card.schema.copy(), **{
        # TODO
    })
