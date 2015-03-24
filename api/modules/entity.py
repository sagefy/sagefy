"""
Facades for working with entities (card, unit, set).
"""

from models.card import Card
from models.unit import Unit
from models.set import Set

from models.cards.audio_card import AudioCard
from models.cards.choice_card import ChoiceCard
from models.cards.embed_card import EmbedCard
from models.cards.formula_card import FormulaCard
from models.cards.match_card import MatchCard
from models.cards.number_card import NumberCard
from models.cards.page_card import PageCard
from models.cards.slideshow_card import SlideshowCard
from models.cards.upload_card import UploadCard
from models.cards.video_card import VideoCard
from models.cards.writing_card import WritingCard


def get_latest_canonical(kind, entity_id):
    """
    Given a kind and an entity_id, pull the latest canonical
    version out of the database.
    """

    if kind == 'card':
        return Card.get_latest_canonical(entity_id)
    elif kind == 'unit':
        return Unit.get_latest_canonical(entity_id)
    elif kind == 'set':
        return Set.get_latest_canonical(entity_id)


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


def create_entity(data):
    """
    Given a kind and some json, call insert on that kind
    and return the results.
    """

    if 'card' in data:
        return Card.insert(data['card'])
    elif 'unit' in data:
        return Unit.insert(data['unit'])
    elif 'set' in data:
        return Set.insert(data['set'])

    return None, []


def get_card_by_kind(card_id):
    """
    Given a card data, return a new card model to replace it by kind.
    """

    card = Card.get_latest_canonical(card_id)
    if not card:
        return

    data, kind = card.data, card.data.get('kind')

    map = {
        'audio': AudioCard,
        'choice': ChoiceCard,
        'embed': EmbedCard,
        'formula': FormulaCard,
        'match': MatchCard,
        'number': NumberCard,
        'page': PageCard,
        'slideshow': SlideshowCard,
        'upload': UploadCard,
        'video': VideoCard,
        'writing': WritingCard,
    }

    if kind in map:
        return map[kind](data)
