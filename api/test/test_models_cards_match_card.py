from models.cards.match_card import MatchCard
import pytest

xfail = pytest.mark.xfail


def test_match_body(cards_table):
    """
    Expect a match card require a body.
    """

    card, errors = MatchCard.insert({
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
    card, errors = card.update({'body': 'Testing 1234'})
    assert len(errors) == 0


def test_match_options(cards_table):
    """
    Expect a match card require a options.
    (value correct feedback)
    """

    card, errors = MatchCard.insert({
        'unit_id': 'RUF531',
        'name': 'What is?',
        'body': 'Testing 1234',
        'default_incorrect_feedback': 'Boo!',
    })
    assert len(errors) == 1
    card, errors = card.update({'options': [{
        'value': 'abadaba',
        'correct': True,
        'feedback': 'Bazaaa...'
    }]})
    assert len(errors) == 0


def test_match_default_feedback(cards_table):
    """
    Expect a match card require a default feedback.
    """

    card, errors = MatchCard.insert({
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
    card, errors = card.update({'default_incorrect_feedback': 'Boo!'})
    assert len(errors) == 0


def test_match_casing(cards_table):
    """
    Expect a match card to allow case sensitivity.
    """

    card, errors = MatchCard.insert({
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
    card, errors = card.update({'case_sensitive': True})
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
