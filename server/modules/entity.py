"""
Facades for working with entities (card, unit, set).
"""

from models.card import Card
from models.unit import Unit
from models.set import Set

# from models.cards.audio_card import AudioCard
from models.cards.choice_card import ChoiceCard
# from models.cards.embed_card import EmbedCard
# from models.cards.formula_card import FormulaCard
# from models.cards.match_card import MatchCard
# from models.cards.number_card import NumberCard
# from models.cards.page_card import PageCard
# from models.cards.slideshow_card import SlideshowCard
# from models.cards.upload_card import UploadCard
from models.cards.video_card import VideoCard
# from models.cards.writing_card import WritingCard

from modules.util import omit


card_map = {
    # 'audio': AudioCard,
    'choice': ChoiceCard,
    # 'embed': EmbedCard,
    # 'formula': FormulaCard,
    # 'match': MatchCard,
    # 'number': NumberCard,
    # 'page': PageCard,
    # 'slideshow': SlideshowCard,
    # 'upload': UploadCard,
    'video': VideoCard,
    # 'writing': WritingCard,
}


def get_latest_accepted(db_conn, kind, entity_id):
    """
    Given a kind and an entity_id, pull the latest accepted
    version out of the database.
    """

    if kind == 'card':
        card = Card.get_latest_accepted(db_conn, entity_id)
        return flip_card_into_kind(card)
    elif kind == 'unit':
        return Unit.get_latest_accepted(db_conn, entity_id)
    elif kind == 'set':
        return Set.get_latest_accepted(db_conn, entity_id)


def get_version(db_conn, kind, id_):
    if kind == 'card':
        card = Card.get(db_conn, id=id_)
        return flip_card_into_kind(card)
    elif kind == 'unit':
        return Unit.get(db_conn, id=id_)
    elif kind == 'set':
        return Set.get(db_conn, id=id_)


def get_kind(data):
    """
    Given the JSON data, figure out what kind of entity lies within.
    """

    kinds = []

    if 'card' in data or 'cards' in data:
        kinds.append('card')
    elif 'unit' in data or 'units' in data:
        kinds.append('unit')
    elif 'set' in data or 'set' in data:
        kinds.append('set')

    if len(kinds) == 0:
        return None
    if len(kinds) == 1:
        return kinds[0]

    return kinds


def instance_new_entity(data):
    """
    Given a kind and some json, call insert on that kind
    and return the results.
    A little safer.
    """

    fields = ('id', 'created', 'modified',
              'entity_id', 'previous_id', 'status', 'available')
    if 'card' in data:
        kind = data['card'].get('kind')
        if kind in card_map:
            return card_map[kind](omit(data['card'], fields))
    elif 'unit' in data:
        return Unit(omit(data['unit'], fields))
    elif 'set' in data:
        return Set(omit(data['set'], fields))


def get_card_by_kind(db_conn, card_id):
    """
    Given a card data, return a new card model to replace it by kind.
    """

    card = Card.get_latest_accepted(db_conn, card_id)
    return flip_card_into_kind(card)


def flip_card_into_kind(card):
    """
    Given a general card model (before removing extra fields),
    return a card model in its kind.
    """

    if not card:
        return None
    kind = card.data.get('kind')
    if kind in card_map:
        return card_map[kind](card.data)


def flush_entities(db_conn, descs):
    """
    Given a list of kinds and entity_ids,
    return a list filled out with entities.
    """

    output = []

    for desc in descs:
        if desc['kind'] == 'card':
            card = Card.get_latest_accepted(db_conn, entity_id=desc['id'])
            card = flip_card_into_kind(card)
            if card:
                output.append(card)
        elif desc['kind'] == 'unit':
            output.append(Unit.get_latest_accepted(
                db_conn,
                entity_id=desc['id']
            ))
        elif desc['kind'] == 'set':
            output.append(Set.get_latest_accepted(
                db_conn,
                entity_id=desc['id']
            ))
        else:
            output.append(None)

    return output
