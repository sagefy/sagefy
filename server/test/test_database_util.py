import pytest
import rethinkdb as r
from conftest import table
from test_config import config
import database.util as util
from modules.util import extend, pick
from schemas.index import schema as default
from modules.validations import is_required, is_string, \
    has_min_length, is_one_of


xfail = pytest.mark.xfail


def lowercase_and_strip(s):
    return s.lower().strip()


vases_schema = extend({}, default, {
    'tablename': 'vases',
    'fields': {
        'name': {
            'validate': (is_required, is_string,),
            'bundle': lowercase_and_strip,
            'unique': True,
        },
        'plants': {
            'validate': (is_required, (has_min_length, 1,),),
            'default': [],
            'embed_many': {
                'species': {
                }
            },
        },
        'soil': {
            'validate': (is_required,),
            'default': {},
            'access': ('private',),
            'embed': {
                'color': {
                    'default': 'brown',
                    'validate': (is_required, (is_one_of,
                                               'brown',
                                               'black',
                                               'gray',
                                               'clay',
                                               ))
                }
            },
        }
    },
})


@pytest.fixture
def vases_table(request, db_conn):
    tablename = 'vases'
    tables = r.db(config['rdb_db']).table_list().run(db_conn)
    if tablename and tablename not in tables:
        (r.db(config['rdb_db'])
          .table_create(tablename)
          .run(db_conn))
    return table(tablename, request, db_conn)


def test_insert_document(db_conn):
    schema = vases_schema
    data = {
        'id': 'haxxor',
        'name': 'celestial',
        'plants': [
            {'species': 'zzplant'},
            {'species': 'rubbertree'},
        ],
        'soil': {'color': 'black'}
    }
    document, errors = util.insert_document(schema, data, db_conn)
    subdoc = pick(document, ('name', 'plants', 'soil'))
    subdata = pick(data, ('name', 'plants', 'soil'))
    assert document['id'] != data['id']
    assert len(errors) == 0
    assert subdoc == subdata


@xfail
def test_update_document(db_conn):
    1/0


def test_save_document(db_conn, vases_table):
    schema = vases_schema
    data = {
        'name': 'celestial',
        'plants': [
            {'species': 'zzplant'},
            {'species': 'rubbertree'},
        ],
        'soil': {'color': 'black'}
    }
    document, errors = util.save_document(schema, data, db_conn)
    subdoc = pick(document, ('name', 'plants', 'soil'))
    assert len(errors) == 0
    assert subdoc == data


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
def test_recurse_embeds():
    1/0


@xfail
def test_prepare_document(db_conn):
    1/0


@xfail
def test_tidy_fields():
    1/0


@xfail
def test_add_default_fields():
    1/0


@xfail
def test_validate_fields():
    1/0


@xfail
def test_validate_unique_fields(db_conn):
    1/0


@xfail
def test_bundle_fields():
    1/0


@xfail
def test_deliver_fields():
    1/0
