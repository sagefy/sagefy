from modules.validations import is_required, is_boolean, is_string, \
    is_number, is_language, is_list, is_email, has_min_length, is_one_of, \
    is_list_of_strings, is_url, is_string_or_number, is_integer, \
    has_max_length, is_dict


def test_require(db_conn):
    """
    Expect a validation to require a field.
    """
    assert is_required('test') is None
    assert is_required(None)


def test_email(db_conn):
    """
    Expect a validation to validate email format.
    """
    assert is_email('test@example.com') is None
    assert is_email('other')


def test_url(db_conn):
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


def test_minlength(db_conn):
    """
    Expect a validation to require a minimum length.
    """
    assert has_min_length('abcd1234', 8) is None
    assert has_min_length('a', 8)


def test_maxlength(db_conn):
    """
    Expect a validation to require a maximum length.
    """
    assert has_max_length('abcd1234', 2)
    assert has_max_length('a', 2) is None


def test_boolean(db_conn):
    """
    Expect a boolean.
    """
    assert is_boolean(False) is None
    assert is_boolean('a')


def test_string(db_conn):
    """
    Expect a string.
    """
    assert is_string('a') is None
    assert is_string(0)


def test_number(db_conn):
    """
    Expect a number.
    """
    assert is_number(0) is None
    assert is_number('1')


def test_integer(db_conn):
    """
    Expect a number.
    """
    assert is_integer(0) is None
    assert is_integer(1.1)
    assert is_integer('1')


def test_string_or_number(db_conn):
    """
    Expect a string or number.
    """
    assert is_string_or_number(1) is None
    assert is_string_or_number(1.1) is None
    assert is_string_or_number('1.1') is None
    assert is_string_or_number([])


def test_language(db_conn):
    """
    Expect two-char language.
    """
    assert is_language('en') is None
    assert is_language('enf')


def test_list(db_conn):
    """
    Expect a list.
    """
    assert is_list([]) is None
    assert is_list({})


def test_dict(db_conn):
    """
    Expect a dict.
    """
    assert is_dict({}) is None
    assert is_dict([])


def test_one_of(db_conn):
    """
    Expect to be one of a list.
    """
    assert is_one_of('1', '1') is None
    assert is_one_of(1, '1')


def test_list_string(db_conn):
    """
    Expect a list of strings.
    """
    assert is_list_of_strings(['a']) is None
    assert is_list_of_strings([1])
