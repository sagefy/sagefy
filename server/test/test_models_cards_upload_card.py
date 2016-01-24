from models.cards.upload_card import UploadCard
import pytest

xfail = pytest.mark.xfail


@xfail
def test_upload_body(db_conn, cards_table):
    """
    Expect an upload card to require a body.
    """

    card, errors = UploadCard.insert(db_conn, {
        'unit_id': 'RUF531',
        'name': 'What is?',
        'file_extensions': ['jpg'],
        'rubric': True,  # TODO
    })
    assert len(errors) == 1
    card, errors = card.update(db_conn, {'body': 'Testing 1234'})
    assert len(errors) == 0


@xfail
def test_upload_file_extensions(db_conn, cards_table):
    """
    Expect an upload card to require file_extensions.
    """

    card, errors = UploadCard.insert(db_conn, {
        'unit_id': 'RUF531',
        'name': 'What is?',
        'body': 'Testing 1234',
        'rubric': True,  # TODO
    })
    assert len(errors) == 1
    card, errors = card.update(db_conn, {'file_extensions': ['jpg']})
    assert len(errors) == 0


@xfail
def test_upload_rubric(db_conn, cards_table):
    """
    Expect an upload card to require a rubric.
    """

    card, errors = UploadCard.insert(db_conn, {
        'unit_id': 'RUF531',
        'name': 'What is?',
        'body': 'Testing 1234',
        'file_extensions': ['jpg'],
    })
    assert len(errors) == 1
    card, errors = card.update(db_conn, {'rubric': None})
    assert len(errors) == 0


@xfail
def test_validate_response(db_conn, cards_table):
    """
    Expect to check if a given response is valid for the card kind.
    """

    assert False
