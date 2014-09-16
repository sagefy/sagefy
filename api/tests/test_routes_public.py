

def test_welcome(app):
    """
    Ensure the API returns a welcome message.
    """
    response = app.test_client().get('/api/')
    assert 'Welcome' in response.data.decode('utf-8')
