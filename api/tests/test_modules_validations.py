from modules.validations import is_required, is_boolean, is_string, \
    is_number, is_language, is_list, is_email, has_min_length, is_one_of, \
    is_entity_dict, is_entity_list_dict, is_list_of_strings, is_url


def test_require(app, db_conn):
    """
    Expect a validation to require a field.
    """
    assert is_required('test') is None
    assert is_required(None)


def test_email(app, db_conn):
    """
    Expect a validation to validate email format.
    """
    assert is_email('test@example.com') is None
    assert is_email('other')


def test_url(app, db_conn):
    """
    Expect a valid URL.
    """
    assert is_url('https://t.c') is None
    assert is_url('http://t.c/t.html?t=b#s') is None
    assert is_url('//t.c') is None
    assert is_url('//t.c/t.html?t=b#s') is None
    assert is_url('https://t')
    assert is_url('http://t.')
    assert is_url('//t')
    assert is_url('//t.')


def test_minlength(app, db_conn):
    """
    Expect a validation to require a minimum length.
    """
    assert has_min_length('abcd1234', 8) is None
    assert has_min_length('a', 8)


def test_boolean(app, db_conn):
    """
    Expect a boolean.
    """
    assert is_boolean(False) is None
    assert is_boolean('a')


def test_string(app, db_conn):
    """
    Expect a string.
    """
    assert is_string('a') is None
    assert is_string(0)


def test_number(app, db_conn):
    """
    Expect a number.
    """
    assert is_number(0) is None
    assert is_number('1')


def test_language(app, db_conn):
    """
    Expect two-char language.
    """
    assert is_language('en') is None
    assert is_language('enf')


def test_list(app, db_conn):
    """
    Expect a list.
    """
    assert is_list([]) is None
    assert is_list({})


def test_one_of(app, db_conn):
    """
    Expect to be one of a list.
    """
    assert is_one_of('1', '1') is None
    assert is_one_of(1, '1')


def test_entity(app, db_conn):
    """
    Expect to reference an entity.
    """
    assert is_entity_dict({'id': 'a', 'kind': 'card'}) is None
    assert is_entity_dict({'id': 'a', 'kind': 'Card'})


def test_list_entity(app, db_conn):
    """
    Expect a list of entity references.
    """
    assert is_entity_list_dict([{'id': 'a', 'kind': 'card'}]) is None
    assert is_entity_list_dict([{'id': 'a', 'kind': 'Card'}])


def test_list_string(app, db_conn):
    """
    Expect a list of strings.
    """
    assert is_list_of_strings(['a']) is None
    assert is_list_of_strings([1])
