from models.cards.choice_card import ChoiceCard
import pytest

xfail = pytest.mark.xfail


def test_choice_body(cards_table):
    """
    Expect a choice card to require a body (question).
    """

    card, errors = ChoiceCard.insert({
        'unit_id': 'RUF531',
        'name': 'What is?',
        'options': [{
            'value': 'abadaba',
            'correct': True,
            'feedback': 'Bazaaa...'
        }],
    })
    assert len(errors) == 1
    card, errors = card.update({'body': 'Testing 1234'})
    assert len(errors) == 0


def test_choice_options(cards_table):
    """
    Expect a choice card to require a options (answers).
    (value, correct, feedback)
    """

    card, errors = ChoiceCard.insert({
        'unit_id': 'RUF531',
        'name': 'What is?',
        'body': 'Testing 1234',
    })
    assert len(errors) == 1
    card, errors = card.update({'options': [{
        'value': 'abadaba',
        'correct': True,
        'feedback': 'Bazaaa...'
    }]})
    assert len(errors) == 0


def test_choice_order(cards_table):
    """
    Expect a choice card to allow set order.
    """

    card, errors = ChoiceCard.insert({
        'unit_id': 'RUF531',
        'name': 'What is?',
        'body': 'Testing 1234',
        'options': [{
            'value': 'abadaba',
            'correct': True,
            'feedback': 'Bazaaa...'
        }],
    })
    assert len(errors) == 0
    card, errors = card.update({'order': 'set'})
    assert len(errors) == 0


def test_choice_max_opts(cards_table):
    """
    Expect a choice card to allow max options (question).
    """

    card, errors = ChoiceCard.insert({
        'unit_id': 'RUF531',
        'name': 'What is?',
        'body': 'Testing 1234',
        'options': [{
            'value': 'abadaba',
            'correct': True,
            'feedback': 'Bazaaa...'
        }],
    })
    assert len(errors) == 0
    card, errors = card.update({'max_options': 2})
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
