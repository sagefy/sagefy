from models.card import Card


class UploadCard(Card):
    schema = dict(Card.schema.copy(), **{
        # TODO
    })
