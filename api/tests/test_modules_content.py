from modules import content


def test_get():
    # Expect to get content in the right language
    assert content.get('error', 'required') == 'Required.'
    assert content.get('error', 'required', 'eo') == 'Postulo.'
