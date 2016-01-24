from models.cards.slideshow_card import SlideshowCard
import pytest

xfail = pytest.mark.xfail


@xfail
def test_slideshow_site(db_conn, cards_table):
    """
    Expect a slideshow card to require a site.
    """

    card, errors = SlideshowCard.insert(db_conn, {
        'unit_id': 'RUF531',
        'name': 'What is?',
        'slideshow_id': 'JKLfjkld950',
    })
    assert len(errors) == 1
    card, errors = card.update(db_conn, {'site': 'slideshare'})
    assert len(errors) == 0


@xfail
def test_slideshow_id(db_conn, cards_table):
    """
    Expect a slideshow card to require a slideshow_id.
    """

    card, errors = SlideshowCard.insert(db_conn, {
        'unit_id': 'RUF531',
        'name': 'What is?',
        'site': 'slideshare',
    })
    assert len(errors) == 1
    card, errors = card.update(db_conn, {'slideshow_id': 'JofO48J'})
    assert len(errors) == 0


@xfail
def test_validate_response(db_conn, cards_table):
    """
    Expect to check if a given response is valid for the card kind.
    """

    assert False
