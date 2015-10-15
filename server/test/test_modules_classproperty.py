from modules.classproperty import classproperty


def test_class_property():
    """
    Unit tests
    """

    def _(o):
        return True

    c = classproperty(_)
    assert c.fn is _

    try:
        c.fn = True
        assert False
    except:
        assert True

    try:
        del c.fn
        assert False
    except:
        assert True
