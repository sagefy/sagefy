import routes.error as error


def test_important_codes(app):
    """
    Expect most common codes present.
    """
    for code in (400, 401, 403, 404, 405, 409, 500, 502, 503):
        assert code in error.codes


def test_error_factory(app):
    """
    Expect the error response to return a function
    that handles responses for that error code.
    """
    response_fn = error.error_response(404)
    assert hasattr(response_fn, '__call__')


def test_404(app):
    """
    Expect the right format for a 404 response.
    """
    error.setup_errors(app)
    response = app.test_client().get('/api/afds')
    assert '404' in response.data.decode('utf-8')
