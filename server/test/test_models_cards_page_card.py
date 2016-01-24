from models.cards.page_card import PageCard
import pytest

xfail = pytest.mark.xfail


@xfail
def test_page_body(db_conn, cards_table):
    """
    Expect a page card to require a body.
    """

    card, errors = PageCard.insert(db_conn, {
        'unit_id': 'RUF531',
        'name': 'What is?',
    })
    assert len(errors) == 1
    card, errors = card.update(db_conn, {'body': 'Testing 1234'})
    assert len(errors) == 0


@xfail
def test_validate_response(db_conn, cards_table):
    """
    Expect to check if a given response is valid for the card kind.
    """

    assert False
