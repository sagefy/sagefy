from modules import content
import pytest

xfail = pytest.mark.xfail


def test_get():
    # Expect to get content in the right language
    assert content.get('error', 'required') == 'Required.'
    assert content.get('error', 'required', 'eo') == 'Postulo.'


@xfail
def test_get_default():
    # Expect to show English if language isn't available.
    return False


@xfail
def test_get_no_country():
    # Expect to show base language if missing country-specific.
    return False
