from models.cards.number_card import NumberCard
import pytest

xfail = pytest.mark.xfail


def test_number_body(app, cards_table):
    """
    Expect a number card to require a body.
    """

    card, errors = NumberCard.insert({
        'unit_id': 'RUF531',
        'name': 'What is?',
        'options': [{
            'value': 42,
            'correct': True,
            'feedback': 'Bazaaa...'
        }],
        'default_incorrect_feedback': 'Boo!',
    })
    assert len(errors) == 1
    card, errors = card.update({'body': 'Testing 1234'})
    assert len(errors) == 0


def test_number_options(app, cards_table):
    """
    Expect a number card to require a options.
    (value correct feedback)
    """

    card, errors = NumberCard.insert({
        'unit_id': 'RUF531',
        'name': 'What is?',
        'body': 'Testing 1234',
        'default_incorrect_feedback': 'Boo!',
    })
    assert len(errors) == 1
    card, errors = card.update({'options': [{
        'value': 42,
        'correct': True,
        'feedback': 'Bazaaa...'
    }]})
    assert len(errors) == 0


def test_number_range(app, cards_table):
    """
    Expect a number card to allow a range.
    """

    card, errors = NumberCard.insert({
        'unit_id': 'RUF531',
        'name': 'What is?',
        'body': 'Testing 1234',
        'options': [{
            'value': 42,
            'correct': True,
            'feedback': 'Bazaaa...'
        }],
        'default_incorrect_feedback': 'Boo!',
    })
    assert len(errors) == 0
    card, errors = card.update({'range': 0.1})
    assert len(errors) == 0


def test_number_default_feedback(app, cards_table):
    """
    Expect a number card to require default feedback.
    """

    card, errors = NumberCard.insert({
        'unit_id': 'RUF531',
        'name': 'What is?',
        'body': 'Testing 1234',
        'options': [{
            'value': 42,
            'correct': True,
            'feedback': 'Bazaaa...'
        }],
    })
    assert len(errors) == 1
    card, errors = card.update({'default_incorrect_feedback': 'Boo!'})
    assert len(errors) == 0


@xfail
def test_is_valid_response(app, db_conn, cards_table):
    """
    Expect to check if a given response is valid for the card kind.
    """

    assert False
