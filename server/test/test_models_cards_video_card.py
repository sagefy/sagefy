from models.cards.video_card import VideoCard
import pytest

xfail = pytest.mark.xfail


def test_site(db_conn, cards_table):
    """
    Expect a video card to require a site.
    """

    card, errors = VideoCard.insert(db_conn, {
        'unit_id': 'RUF531',
        'name': 'What is?',
        'video_id': 'Ajklfjl4',
    })
    assert len(errors) == 1
    card['site'] = 'youtube'
    errors = card.validate(db_conn)
    assert len(errors) == 0


def test_video_id(db_conn, cards_table):
    """
    Expect a video card to require a video_id.
    """

    card, errors = VideoCard.insert(db_conn, {
        'unit_id': 'RUF531',
        'name': 'What is?',
        'site': 'youtube'
    })
    assert len(errors) == 1
    card['video_id'] = 'JFKl94jl'
    errors = card.validate(db_conn)
    assert len(errors) == 0


@xfail
def test_validate_response(db_conn, cards_table):
    """
    Expect to check if a given response is valid for the card kind.
    """

    assert False
