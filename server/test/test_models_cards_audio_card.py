from models.cards.audio_card import AudioCard
import pytest

xfail = pytest.mark.xfail


@xfail
def test_audio_site(cards_table, db_conn):
    """
    Expect an audio card to require site.
    """

    card, errors = AudioCard.insert(db_conn, {
        'unit_id': 'RUF531',
        'name': 'What is?',
        'audio_id': 'AJkl78',
    })
    assert len(errors) == 1
    card, errors = card.update(db_conn, {'site': 'soundcloud'})
    assert len(errors) == 0


@xfail
def test_audio_audio_id(cards_table, db_conn):
    """
    Expect an audio card to require audio_id.
    """

    card, errors = AudioCard.insert(db_conn, {
        'unit_id': 'RUF531',
        'name': 'What is?',
        'site': 'soundcloud',
    })
    assert len(errors) == 1
    card, errors = card.update(db_conn, {'audio_id': 'JKfoej89'})
    assert len(errors) == 0


@xfail
def test_validate_response(db_conn, cards_table):
    """
    Expect to check if a given response is valid for the card kind.
    """

    assert False
