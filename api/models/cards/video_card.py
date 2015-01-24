from models.card import Card


class VideoCard(Card):
    schema = dict(Card.schema.copy(), **{
        'site': {
            # TODO
        },
        'id': {
            # TODO
        }
    })
