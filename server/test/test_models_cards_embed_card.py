from models.cards.embed_card import EmbedCard
import pytest

xfail = pytest.mark.xfail


@xfail
def test_embed_url(db_conn, cards_table):
    """
    Expect embed card to require URL.
    """

    card, errors = EmbedCard.insert(db_conn, {
        'unit_id': 'RUF531',
        'name': 'What is?',
        'rubric': True,  # TODO
    })
    assert len(errors) == 1
    card, errors = card.update(db_conn, {'url': 'http://google.com'})
    assert len(errors) == 0


@xfail
def test_embed_rubric(db_conn, cards_table):
    """
    Expect embed card to require a rubric.
    """

    card, errors = EmbedCard.insert(db_conn, {
        'unit_id': 'RUF531',
        'name': 'What is?',
        'url': 'http://google.com',
    })
    assert len(errors) == 1
    card, errors = card.update(db_conn, {'rubric': None})
    assert len(errors) == 0


@xfail
def test_validate_response(db_conn, cards_table):
    """
    Expect to check if a given response is valid for the card kind.
    """

    assert False
