from models.user_sets import UserSets
import pytest

xfail = pytest.mark.xfail


def test_user(app, db_conn, users_sets_table):
    """
    Expect to require a user ID.
    """

    user_sets, errors = UserSets.insert({
        'set_ids': [
            'A',
            'B',
        ],
    })
    assert len(errors) == 1
    user_sets['user_id'] = 'A'
    user_sets, errors = user_sets.save()
    assert len(errors) == 0


def test_sets(app, db_conn, users_sets_table):
    """
    Expect to require a list of set IDs.
    """

    user_sets, errors = UserSets.insert({
        'user_id': 'A'
    })
    assert len(errors) == 1
    user_sets['set_ids'] = [
        'A',
        'B',
    ]
    user_sets, errors = user_sets.save()
    assert len(errors) == 0


@xfail
def test_list_sets(app, db_conn, users_sets_table, sets_table):
    """
    Expect to list sets a user subscribes to.
    """

    assert False
