import pytest

xfail = pytest.mark.xfail


@xfail
def test_insert_document(db_conn):
    1/0


@xfail
def test_update_document(db_conn):
    1/0


@xfail
def test_save_document(db_conn):
    1/0


@xfail
def test_get_document(db_conn):
    1/0


@xfail
def test_list_documents(db_conn):
    1/0


@xfail
def test_delete_document(db_conn):
    1/0


@xfail
def test_recurse_embeds(db_conn):
    1/0


@xfail
def test_prepare_document(db_conn):
    1/0


@xfail
def test_tidy_fields(db_conn):
    1/0


@xfail
def test_add_default_fields(db_conn):
    1/0


@xfail
def test_validate_fields(db_conn):
    1/0


@xfail
def test_validate_unique_fields(db_conn):
    1/0


@xfail
def test_bundle_fields(db_conn):
    1/0


@xfail
def test_deliver_fields(db_conn):
    1/0
