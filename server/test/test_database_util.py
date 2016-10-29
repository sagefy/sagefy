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
        'shape': {
            'validate': ((is_one_of, 'round', 'square', 'triangle'),),
            'default': 'round'
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


def test_insert_document(db_conn, vases_table):
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


def test_update_document(db_conn):
    schema = vases_schema
    data1 = {
        'name': 'celestial',
        'plants': [
            {'species': 'zzplant'},
            {'species': 'rubbertree'},
        ],
        'soil': {'color': 'black'}
    }
    document1, errors1 = util.insert_document(schema, data1, db_conn)
    subdoc1 = pick(document1, ('name', 'plants', 'soil'))
    subdata1 = pick(data1, ('name', 'plants', 'soil'))
    data2 = {
        'id': 'haxxor',
        'name': 'zen',
    }
    document2, errors2 = util.update_document(schema,
                                              document1, data2, db_conn)
    subdoc2 = pick(document2, ('name', 'plants', 'soil'))
    subdata2 = pick(data2, ('name', 'plants', 'soil'))
    assert len(errors1) == 0
    assert subdoc1 == subdata1
    assert document1['id'] == document2['id']
    assert len(errors2) == 0
    assert subdoc2 == extend({}, subdata1, subdata2)


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


def create_test_data_set(db_conn, vases_table):
    """
    Create a set of fake data.
    """

    schema = vases_schema
    data = [{
        'name': 'celestial',
        'shape': 'round',
        'plants': [
            {'species': 'zzplant'},
            {'species': 'rubbertree'},
        ],
        'soil': {'color': 'black'}
    }, {
        'name': 'kitch',
        'shape': 'round',
        'plants': [
            {'species': 'sunflower'},
            {'species': 'geranium'},
        ],
        'soil': {'color': 'brown'}
    }, {
        'name': 'modern',
        'shape': 'square',
        'plants': [
            {'species': 'fiddle-leaf-fig'},
            {'species': 'rubbertree'},
        ],
        'soil': {'color': 'black'}
    }]
    errors = []
    docs = []
    for d in data:
        doc, e = util.insert_document(schema, d, db_conn)
        if e:
            errors.append(e)
        docs.append(doc)
    assert not errors
    return docs


def test_get_document(db_conn, vases_table):
    tablename = 'vases'
    create_test_data_set(db_conn, vases_table)
    params = {'name': 'modern'}
    document = util.get_document(tablename, params, db_conn)
    assert document['name'] == 'modern'
    assert document['soil'] == {'color': 'black'}


def test_list_documents(db_conn, vases_table):
    tablename = 'vases'
    create_test_data_set(db_conn, vases_table)
    params = {'shape': 'round'}
    documents = list(util.list_documents(tablename, params, db_conn))
    assert len(documents) == 2


def test_delete_document(db_conn, vases_table):
    tablename = 'vases'
    documents = create_test_data_set(db_conn, vases_table)
    assert len(documents) == 3
    util.delete_document(tablename, documents[0]['id'], db_conn)
    params = {}
    documents = list(util.list_documents(tablename, params, db_conn))
    assert len(documents) == 2


###############################################################################


@xfail
def test_recurse_embeds():
    1/0


@xfail
def test_prepare_document(db_conn, vases_table):
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
def test_validate_unique_fields(db_conn, vases_table):
    1/0


@xfail
def test_bundle_fields():
    1/0


@xfail
def test_deliver_fields():
    1/0
