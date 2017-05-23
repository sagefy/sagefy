import pytest
from database.card import insert_card

xfail = pytest.mark.xfail


def test_entity_id(db_conn, cards_table):
    """
    Expect a card to require an entity_id.
    """

    card, errors = insert_card(db_conn, {
        'user_id': 'abcd1234',
        'previous_id': 'TJKL35',
        'language': 'en',
        'unit_id': 'RUF531',
        'name': 'What is?',
        'kind': 'video',
        'video_id': 'abcd1234',
        'site': 'youtube',
    })
    assert len(errors) == 0
    assert card['entity_id']


def test_previous_version_id(db_conn, cards_table):
    """
    Expect a card to allow a previous version id.
    """

    card, errors = insert_card(db_conn, {
        'user_id': 'abcd1234',
        'language': 'en',
        'unit_id': 'RUF531',
        'name': 'What is?',
        'kind': 'video',
        'video_id': 'abcd1234',
        'site': 'youtube',
    })
    assert len(errors) == 0
    card['previous_id'] = 'TJKL35'
    card, errors = insert_card(db_conn, card)
    assert len(errors) == 0


def test_language(db_conn, cards_table):
    """
    Expect a card to require a language.
    """

    card, errors = insert_card(db_conn, {
        'user_id': 'abcd1234',
        'previous_id': 'TJKL35',
        'unit_id': 'RUF531',
        'name': 'What is?',
        'kind': 'video',
        'video_id': 'abcd1234',
        'site': 'youtube',
    })
    assert len(errors) == 0
    card['language'] = 'en'


def test_unit_id(db_conn, cards_table):
    """
    Expect a card to require a unit id.
    """

    card, errors = insert_card(db_conn, {
        'user_id': 'abcd1234',
        'previous_id': 'TJKL35',
        'language': 'en',
        'name': 'What is?',
        'kind': 'video',
        'video_id': 'abcd1234',
        'site': 'youtube',
    })
    assert len(errors) == 1
    card['unit_id'] = 'RUF531A'
    card, errors = insert_card(db_conn, card)
    assert len(errors) == 0


def test_name(db_conn, cards_table):
    """
    Expect a card to require a name.
    """

    card, errors = insert_card(db_conn, {
        'user_id': 'abcd1234',
        'previous_id': 'TJKL35',
        'language': 'en',
        'unit_id': 'RUF531',
        'kind': 'video',
        'video_id': 'abcd1234',
        'site': 'youtube',
    })
    assert len(errors) == 1
    card['name'] = 'What is?'
    card, errors = insert_card(db_conn, card)
    assert len(errors) == 0


def test_status(db_conn, cards_table):
    """
    Expect a card version status to be a string.
    """

    card, errors = insert_card(db_conn, {
        'user_id': 'abcd1234',
        'previous_id': 'TJKL35',
        'language': 'en',
        'unit_id': 'RUF531',
        'name': 'What is?',
        'kind': 'video',
        'video_id': 'abcd1234',
        'site': 'youtube',
    })
    assert len(errors) == 0
    assert card['status'] == 'pending'
    card['status'] = 'accepted'
    card, errors = insert_card(db_conn, card)
    assert len(errors) == 0


def test_tags(db_conn, cards_table):
    """
    Expect a card to allow tags.
    """

    card, errors = insert_card(db_conn, {
        'user_id': 'abcd1234',
        'previous_id': 'TJKL35',
        'language': 'en',
        'unit_id': 'RUF531',
        'name': 'What is?',
        'kind': 'video',
        'video_id': 'abcd1234',
        'site': 'youtube',
    })
    assert len(errors) == 0
    card['tags'] = ['B', 'A']
    card, errors = insert_card(db_conn, card)
    assert len(errors) == 0


def test_kind(db_conn, cards_table):
    """
    Expect a card to have a kind.
    """

    card, errors = insert_card(db_conn, {
        'user_id': 'abcd1234',
        'previous_id': 'TJKL35',
        'language': 'en',
        'unit_id': 'RUF531',
        'name': 'What is?',
        'video_id': 'abcd1234',
        'site': 'youtube',
    })
    assert len(errors) == 1
    card['kind'] = 'video'
    card, errors = insert_card(db_conn, card)
    assert len(errors) == 0


@xfail
def test_validate_response(db_conn, cards_table):
    """
    Expect to check if a given response is valid for the card kind.
    """

    assert False
