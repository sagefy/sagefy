from models.cards.formula_card import FormulaCard
import pytest

xfail = pytest.mark.xfail


def test_formula_body(app, cards_table):
    """
    Expect a formula card to require a body.
    """

    card, errors = FormulaCard.insert({
        'unit_id': 'RUF531',
        'name': 'What is?',
        'options': [{
            'value': 'x',
            'correct': True,
            'feedback': 'Bazaaa...'
        }],
        'variables': [{'name': 'x'}],
        'default_incorrect_feedback': 'Boo!',
    })
    assert len(errors) == 1
    card, errors = card.update({'body': 'Testing 1234'})
    assert len(errors) == 0


def test_formula_options(app, cards_table):
    """
    Expect a formula card to require options.
    (value, correct, feedback)
    """

    card, errors = FormulaCard.insert({
        'unit_id': 'RUF531',
        'name': 'What is?',
        'body': 'Testing 1234',
        'variables': [{'name': 'x'}],
        'default_incorrect_feedback': 'Boo!',
    })
    assert len(errors) == 1
    card, errors = card.update({'options': [{
        'value': 'x',
        'correct': True,
        'feedback': 'Bazaaa...'
    }]})
    assert len(errors) == 0


@xfail
def test_formula_variables(app, cards_table):
    """
    Expect a formula card to require variables.
    """

    assert False


def test_formula_range(app, cards_table):
    """
    Expect a formula card to require a range.
    """

    card, errors = FormulaCard.insert({
        'unit_id': 'RUF531',
        'name': 'What is?',
        'body': 'Testing 1234',
        'options': [{
            'value': 'x',
            'correct': True,
            'feedback': 'Bazaaa...'
        }],
        'variables': [{'name': 'x'}],
        'default_incorrect_feedback': 'Boo!',
    })
    assert len(errors) == 0
    card, errors = card.update({'range': 0.1})
    assert len(errors) == 0


def test_formula_default_feedback(app, cards_table):
    """
    Expect a formula card to require default feedback.
    """

    card, errors = FormulaCard.insert({
        'unit_id': 'RUF531',
        'name': 'What is?',
        'body': 'Testing 1234',
        'options': [{
            'value': 'x',
            'correct': True,
            'feedback': 'Bazaaa...'
        }],
        'variables': [{'name': 'x'}],
    })
    assert len(errors) == 1
    card, errors = card.update({'default_incorrect_feedback': 'Boo!'})
    assert len(errors) == 0
