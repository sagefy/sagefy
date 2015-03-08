from models.cards.writing_card import WritingCard
import pytest

xfail = pytest.mark.xfail


def test_writing_body(app, cards_table):
    """
    Expect writing card to require body.
    """

    card, errors = WritingCard.insert({
        'unit_id': 'RUF531',
        'name': 'What is?',
        'rubric': True,  # TODO@
    })
    assert len(errors) == 1
    card, errors = card.update({'body': 'Testing 1234'})
    assert len(errors) == 0


def test_writing_max_char(app, cards_table):
    """
    Expect writing card to allow max char.
    """

    card, errors = WritingCard.insert({
        'unit_id': 'RUF531',
        'name': 'What is?',
        'body': 'Testing 1234',
        'rubric': True,  # TODO@
    })
    assert len(errors) == 0
    card, errors = card.update({'max_characters': 500})
    assert len(errors) == 0


@xfail
def test_writing_rubric(app, cards_table):
    """
    Expect writing card to require a rubric.
    """

    card, errors = WritingCard.insert({
        'unit_id': 'RUF531',
        'name': 'What is?',
        'body': 'Testing 1234',
    })
    assert len(errors) == 1
    card, errors = card.update({'rubric': None})
    assert len(errors) == 0
