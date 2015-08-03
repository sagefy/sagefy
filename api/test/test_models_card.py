from models.card import Card
import pytest

xfail = pytest.mark.xfail


def test_entity_id(db_conn, cards_table):
    """
    Expect a card to require an entity_id.
    """

    card, errors = Card.insert({
        'previous_id': 'TJKL35',
        'language': 'en',
        'unit_id': 'RUF531',
        'name': 'What is?',
        'kind': 'video'
    })
    assert len(errors) == 0
    assert card['entity_id']


def test_previous_version_id(db_conn, cards_table):
    """
    Expect a card to allow a previous version id.
    """

    card, errors = Card.insert({
        'language': 'en',
        'unit_id': 'RUF531',
        'name': 'What is?',
        'kind': 'video'
    })
    assert len(errors) == 0
    card['previous_id'] = 'TJKL35'
    card, errors = card.save()
    assert len(errors) == 0


def test_language(db_conn, cards_table):
    """
    Expect a card to require a language.
    """

    card, errors = Card.insert({
        'previous_id': 'TJKL35',
        'unit_id': 'RUF531',
        'name': 'What is?',
        'kind': 'video'
    })
    assert len(errors) == 0
    card['language'] = 'en'


def test_unit_id(db_conn, cards_table):
    """
    Expect a card to require a unit id.
    """

    card, errors = Card.insert({
        'previous_id': 'TJKL35',
        'language': 'en',
        'name': 'What is?',
        'kind': 'video'
    })
    assert len(errors) == 1
    card['unit_id'] = 'RUF531A'
    card, errors = card.save()
    assert len(errors) == 0


def test_name(db_conn, cards_table):
    """
    Expect a card to require a name.
    """

    card, errors = Card.insert({
        'previous_id': 'TJKL35',
        'language': 'en',
        'unit_id': 'RUF531',
        'kind': 'video'
    })
    assert len(errors) == 1
    card['name'] = 'What is?'
    card, errors = card.save()
    assert len(errors) == 0


def test_status(db_conn, cards_table):
    """
    Expect a card version status to be a string.
    """

    card, errors = Card.insert({
        'previous_id': 'TJKL35',
        'language': 'en',
        'unit_id': 'RUF531',
        'name': 'What is?',
        'kind': 'video'
    })
    assert len(errors) == 0
    assert card['status'] == 'pending'
    card['status'] = 'accepted'
    card, errors = card.save()
    assert len(errors) == 0


def test_tags(db_conn, cards_table):
    """
    Expect a card to allow tags.
    """

    card, errors = Card.insert({
        'previous_id': 'TJKL35',
        'language': 'en',
        'unit_id': 'RUF531',
        'name': 'What is?',
        'kind': 'video'
    })
    assert len(errors) == 0
    card['tags'] = ['B', 'A']
    card, errors = card.save()
    assert len(errors) == 0


def test_kind(db_conn, cards_table):
    """
    Expect a card to have a kind.
    """

    card, errors = Card.insert({
        'previous_id': 'TJKL35',
        'language': 'en',
        'unit_id': 'RUF531',
        'name': 'What is?',
    })
    assert len(errors) == 1
    card['kind'] = 'video'
    card, errors = card.save()
    assert len(errors) == 0


@xfail
def test_validate_response(db_conn, cards_table):
    """
    Expect to check if a given response is valid for the card kind.
    """

    assert False
