import database.util as util
from modules.util import extend, pick, omit
from schemas.index import schema as default
from modules.validations import is_required, is_string, \
    has_min_length, is_one_of


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
                    'bundle': lowercase_and_strip,
                },
                'quantity': {
                    'default': 1,
                    'access': ('private',)
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
                    'bundle': lowercase_and_strip,
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


def test_insert_document(db_conn, vases_table):
    schema = vases_schema
    data = {
        'id': 'haxxor',
        'name': 'celestial',
        'plants': [
            {'species': 'zzplant', 'quantity': 2},
            {'species': 'rubbertree', 'quantity': 1},
        ],
        'soil': {'color': 'black'}
    }
    document, errors = util.insert_document(db_conn, schema, data)
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
            {'species': 'zzplant', 'quantity': 2},
            {'species': 'rubbertree', 'quantity': 1},
        ],
        'soil': {'color': 'black'}
    }
    document1, errors1 = util.insert_document(db_conn, schema, data1)
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
            {'species': 'zzplant', 'quantity': 2},
            {'species': 'rubbertree', 'quantity': 1},
        ],
        'soil': {'color': 'black'}
    }
    document, errors = util.save_document(db_conn, schema, data)
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
            {'species': 'zzplant', 'quantity': 2},
            {'species': 'rubbertree', 'quantity': 1},
        ],
        'soil': {'color': 'black'}
    }, {
        'name': 'kitch',
        'shape': 'round',
        'plants': [
            {'species': 'sunflower', 'quantity': 1},
            {'species': 'geranium', 'quantity': 3},
        ],
        'soil': {'color': 'brown'}
    }, {
        'name': 'modern',
        'shape': 'square',
        'plants': [
            {'species': 'fiddle-leaf-fig', 'quantity': 1},
            {'species': 'rubbertree', 'quantity': 3},
        ],
        'soil': {'color': 'black'}
    }]
    errors = []
    docs = []
    for d in data:
        doc, e = util.insert_document(db_conn, schema, d)
        if e:
            errors.append(e)
        docs.append(doc)
    assert not errors
    return docs


def test_get_document(db_conn, vases_table):
    tablename = 'vases'
    create_test_data_set(db_conn, vases_table)
    params = {'name': 'modern'}
    document = util.get_document(db_conn, tablename, params)
    assert document['name'] == 'modern'
    assert document['soil'] == {'color': 'black'}


def test_list_documents(db_conn, vases_table):
    tablename = 'vases'
    create_test_data_set(db_conn, vases_table)
    params = {'shape': 'round'}
    documents = list(db_conn, util.list_documents(tablename, params))
    assert len(documents) == 2


def test_delete_document(db_conn, vases_table):
    tablename = 'vases'
    documents = create_test_data_set(db_conn, vases_table)
    assert len(documents) == 3
    util.delete_document(db_conn, tablename, documents[0]['id'])
    params = {}
    documents = list(db_conn, util.list_documents(tablename, params))
    assert len(documents) == 2


###############################################################################


def test_recurse_embeds():
    o = {}

    def _(data, field_name, field_schema, prefix):
        o[prefix + field_name] = data.get(field_name)

    schema = vases_schema
    data = {
        'name': 'celestial',
        'shape': 'round',
        'plants': [
            {'species': 'zzplant'},
            {'species': 'rubbertree'},
        ],
        'soil': {'color': 'black'}
    }
    util.recurse_embeds(_, data, schema['fields'])
    assert o == {
        'created': None,
        'id': None,
        'modified': None,
        'name': 'celestial',
        'plants': [{'species': 'zzplant'}, {'species': 'rubbertree'}],
        'plants.0.species': 'zzplant',
        'plants.0.quantity': None,
        'plants.1.species': 'rubbertree',
        'plants.1.quantity': None,
        'shape': 'round',
        'soil': {'color': 'black'},
        'soil.color': 'black'
    }


def test_prepare_document(db_conn, vases_table):
    schema = vases_schema
    create_test_data_set(db_conn, vases_table)
    data = {
        'id': 'ZdhhJQ9U9YJaanmfMEpm05qc',
        'name': ' celestial ',
        'shape': 'round',
        'plants': [
            {'species': 'zzplant', 'quantity': 2},
            {'species': 'rubbertree', 'quantity': 1},
        ],
        'soil': {'color': 'black'}
    }
    result, errors = util.prepare_document(db_conn, schema, data)
    assert not errors
    result = omit(result, ('id', 'modified', 'created',))
    assert result == omit(data, ('id',))


def test_tidy_fields():
    schema = vases_schema
    data = {
        'shiny': True,
        'name': 'celestial',
        'shape': 'round',
        'plants': [
            {'species': 'zzplant', 'quantity': 2},
            {'species': 'rubbertree', 'leaves': 90},
        ],
        'soil': {'color': 'black', 'texture': 'gritty'}
    }
    data2 = util.tidy_fields(schema, data)
    assert data2 == {
        'name': 'celestial',
        'shape': 'round',
        'plants': [
            {'species': 'zzplant', 'quantity': 2},
            {'species': 'rubbertree'},
        ],
        'soil': {'color': 'black'}
    }


def test_add_default_fields():
    schema = vases_schema
    data = {}
    data2 = util.add_default_fields(schema, data)
    data2 = omit(data2, ('id', 'created', 'modified',))
    assert data2 == {
        'plants': [],
        'shape': 'round',
        'soil': {'color': 'brown'},
    }


def test_validate_fields():
    schema = vases_schema
    data = {
        'name': 43,
        'shape': 'turkey',
        'plants': [],
        'soil': {'color': 'green'}
    }
    errors = util.validate_fields(schema, data)
    assert len(errors) == 4

    def find(fn, l):
        return list(filter(fn, l))[0]

    name_error = find(lambda e: e['name'] == 'name', errors)
    assert name_error['message'] == 'Must be a string.'
    soil_error = find(lambda e: e['name'] == 'soil.color', errors)
    assert soil_error['message'] == 'Must be one of brown, black, gray, clay.'
    plants_error = find(lambda e: e['name'] == 'plants', errors)
    assert plants_error['message'] == 'Must have minimum length of 1.'
    shape_error = find(lambda e: e['name'] == 'shape', errors)
    assert shape_error['message'] == 'Must be one of round, square, triangle.'


def test_validate_unique_fields(db_conn, vases_table):
    create_test_data_set(db_conn, vases_table)
    schema = vases_schema
    data = {
        'id': 'ZdhhJQ9U9YJaanmfMEpm05qc',
        'name': 'celestial',
        'shape': 'round',
        'plants': [
            {'species': 'zzplant', 'quantity': 2},
            {'species': 'rubbertree', 'quantity': 1},
        ],
        'soil': {'color': 'black'}
    }
    errors = util.validate_unique_fields(db_conn, schema, data)
    assert len(errors) == 1
    assert errors == [{'message': 'Must be unique.', 'name': 'name'}]
    data['name'] = 'starry'
    errors = util.validate_unique_fields(db_conn, schema, data)
    assert len(errors) == 0


def test_bundle_fields():
    schema = vases_schema
    data = {
        'id': 'ZdhhJQ9U9YJaanmfMEpm05qc',
        'name': ' cElEstial ',
        'shape': 'round',
        'plants': [
            {'species': '  zzplant', 'quantity': 2},
            {'species': 'rubbertree', 'quantity': 1},
        ],
        'soil': {'color': '  BLACK  '}
    }
    bundle = util.bundle_fields(schema, data)
    assert bundle == {
        'id': 'ZdhhJQ9U9YJaanmfMEpm05qc',
        'name': 'celestial',
        'shape': 'round',
        'plants': [
            {'species': 'zzplant', 'quantity': 2},
            {'species': 'rubbertree', 'quantity': 1},
        ],
        'soil': {'color': 'black'}
    }


def test_deliver_fields():
    schema = vases_schema
    data = {
        'id': 'ZdhhJQ9U9YJaanmfMEpm05qc',
        'name': ' cElEstial ',
        'shape': 'round',
        'plants': [
            {'species': '  zzplant', 'quantity': 2},
            {'species': 'rubbertree', 'quantity': 1},
        ],
        'soil': {'color': '  BLACK  '}
    }
    assert util.deliver_fields(schema, data, 'private') == {
        'id': 'ZdhhJQ9U9YJaanmfMEpm05qc',
        'name': ' cElEstial ',
        'shape': 'round',
        'plants': [
            {'species': '  zzplant', 'quantity': 2},
            {'species': 'rubbertree', 'quantity': 1},
        ],
        'soil': {'color': '  BLACK  '}
    }
    assert util.deliver_fields(schema, data) == {
        'id': 'ZdhhJQ9U9YJaanmfMEpm05qc',
        'name': ' cElEstial ',
        'shape': 'round',
        'plants': [
            {'species': '  zzplant'},
            {'species': 'rubbertree'},
        ],
        'soil': {}
    }
