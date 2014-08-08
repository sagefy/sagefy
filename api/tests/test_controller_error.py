def test_important_codes(app):
    """
    Expect most common codes present.
    400, 401, 403, 404, 405, 500, 502, 503.
    """
    assert False


def test_error_factory(app):
    """
    Expect the error response to return a function
    that handles responses for that error code.
    """
    assert False


def test_setup_errors(app):
    """
    Expect that each error code is handled by Flask jsonically.
    """
    assert False


def test_404(app):
    """
    Expect the right format for a 404 response.
    """
    assert False
