from models.cards.formula_card import FormulaCard
import pytest

xfail = pytest.mark.xfail


@xfail
def test_formula_body(db_conn, cards_table):
    """
    Expect a formula card to require a body.
    """

    card, errors = FormulaCard.insert(db_conn, {
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
    card, errors = card.update(db_conn, {'body': 'Testing 1234'})
    assert len(errors) == 0


@xfail
def test_formula_options(db_conn, cards_table):
    """
    Expect a formula card to require options.
    (value, correct, feedback)
    """

    card, errors = FormulaCard.insert(db_conn, {
        'unit_id': 'RUF531',
        'name': 'What is?',
        'body': 'Testing 1234',
        'variables': [{'name': 'x'}],
        'default_incorrect_feedback': 'Boo!',
    })
    assert len(errors) == 1
    card, errors = card.update(db_conn, {'options': [{
        'value': 'x',
        'correct': True,
        'feedback': 'Bazaaa...'
    }]})
    assert len(errors) == 0


@xfail
def test_formula_variables(db_conn, cards_table):
    """
    Expect a formula card to require variables.
    """

    assert False


@xfail
def test_formula_range(db_conn, cards_table):
    """
    Expect a formula card to require a range.
    """

    card, errors = FormulaCard.insert(db_conn, {
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
    card, errors = card.update(db_conn, {'range': 0.1})
    assert len(errors) == 0


@xfail
def test_formula_default_feedback(db_conn, cards_table):
    """
    Expect a formula card to require default feedback.
    """

    card, errors = FormulaCard.insert(db_conn, {
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
    card, errors = card.update(db_conn, {'default_incorrect_feedback': 'Boo!'})
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
