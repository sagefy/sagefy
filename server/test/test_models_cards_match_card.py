from models.cards.match_card import MatchCard
import pytest

xfail = pytest.mark.xfail


@xfail
def test_match_body(db_conn, cards_table):
    """
    Expect a match card require a body.
    """

    card, errors = MatchCard.insert(db_conn, {
        'unit_id': 'RUF531',
        'name': 'What is?',
        'options': [{
            'value': 'abadaba',
            'correct': True,
            'feedback': 'Bazaaa...'
        }],
        'default_incorrect_feedback': 'Boo!',
    })
    assert len(errors) == 1
    card, errors = card.update(db_conn, {'body': 'Testing 1234'})
    assert len(errors) == 0


@xfail
def test_match_options(db_conn, cards_table):
    """
    Expect a match card require a options.
    (value correct feedback)
    """

    card, errors = MatchCard.insert(db_conn, {
        'unit_id': 'RUF531',
        'name': 'What is?',
        'body': 'Testing 1234',
        'default_incorrect_feedback': 'Boo!',
    })
    assert len(errors) == 1
    card, errors = card.update(db_conn, {'options': [{
        'value': 'abadaba',
        'correct': True,
        'feedback': 'Bazaaa...'
    }]})
    assert len(errors) == 0


@xfail
def test_match_default_feedback(db_conn, cards_table):
    """
    Expect a match card require a default feedback.
    """

    card, errors = MatchCard.insert(db_conn, {
        'unit_id': 'RUF531',
        'name': 'What is?',
        'body': 'Testing 1234',
        'options': [{
            'value': 'abadaba',
            'correct': True,
            'feedback': 'Bazaaa...'
        }]
    })
    assert len(errors) == 1
    card, errors = card.update(db_conn, {'default_incorrect_feedback': 'Boo!'})
    assert len(errors) == 0


@xfail
def test_match_casing(db_conn, cards_table):
    """
    Expect a match card to allow case sensitivity.
    """

    card, errors = MatchCard.insert(db_conn, {
        'unit_id': 'RUF531',
        'name': 'What is?',
        'body': 'Testing 1234',
        'options': [{
            'value': 'abadaba',
            'correct': True,
            'feedback': 'Bazaaa...'
        }],
        'default_incorrect_feedback': 'Boo!',
    })
    assert len(errors) == 0
    card, errors = card.update(db_conn, {'case_sensitive': True})
    assert len(errors) == 0


@xfail
def test_validate_response(db_conn, cards_table):
    """
    Expect to check if a given response is valid for the card kind.
    """

    assert False


@xfail
def test_score_response(db_conn, cards_table):
    """
    Expect to score if a given response is correct for the card kind.
    """

    assert False
